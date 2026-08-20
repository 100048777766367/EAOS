import { observeGateway } from './gateway.js';
import { readBootstrapState } from './state.js';
import { connectTaskLifecycle, describeWebSocketContract } from './websocket.js';
import { mountAgentStatus } from '../agent/status.js';
import { mountTaskUx, readGatewayTask, renderTaskState, submitGatewayTask } from '../agent/tasks.js';
import { mountChat } from '../chat/chat.js';
import { mountEditor } from '../editor/monaco.js';
import { mountExplorer } from '../explorer/tree.js';
import { mountGit } from '../git/git.js';
import { githubContract } from '../github/github.js';
import { registerCommands } from '../ide/commands.js';
import { mountInspector, updateTaskInspector } from '../ide/inspector.js';
import { loadCapabilityRegistry, loadGatewayContracts, loadGatewaySnapshot } from '../runtime/contracts.js';
import { renderCapabilityRegistry } from '../runtime/capabilities.js';
import { mountRuntime } from '../runtime/runtime.js';
import { telemetryContract } from '../telemetry/telemetry.js';
import { mountTerminal } from '../terminal/terminal.js';
import { enableWorkspaceLayout } from '../workspace/layout.js';

const state = readBootstrapState();
const shell = document.querySelector('[data-testid="aide-shell"]');
const runtime = mountRuntime(document.getElementById('health-state'), state);
const editor = mountEditor(document.getElementById('monaco-editor'), document.getElementById('editor-tabs'), document.getElementById('editor-status'));
const explorer = mountExplorer(document.getElementById('workspace-tree'), { onSelect: editor.openFile });
const terminal = mountTerminal(document.getElementById('terminal-output'));

const agent = mountAgentStatus(document.getElementById('agent-status'));
const git = mountGit(document.getElementById('git-state'));
const github = githubContract(state);
const inspector = mountInspector(document.getElementById('inspector'), state.capabilities || []);
const websocket = describeWebSocketContract(state);
const telemetry = telemetryContract(state);
const commands = registerCommands();
const layout = enableWorkspaceLayout(shell);
const inspectorNodes = {
  task: document.getElementById('inspect-task'),
  lifecycle: document.getElementById('inspect-lifecycle'),
  governance: document.getElementById('inspect-governance'),
  verification: document.getElementById('inspect-verification'),
  evidence: document.getElementById('inspect-evidence'),
  runtime: document.getElementById('inspect-runtime'),
  correlation: document.getElementById('inspect-correlation'),
};
const runtimeNodes = {
  health: document.getElementById('health-state'),
  ws: document.getElementById('ws-state'),
  task: document.getElementById('task-state'),
};
const capabilitiesNode = document.getElementById('capability-registry');
const taskUx = mountTaskUx(
  {
    form: document.getElementById('task-form'),
    commandInput: document.getElementById('task-command'),
    taskId: document.getElementById('task-id'),
    currentState: document.getElementById('current-lifecycle'),
    governance: document.getElementById('governance-result'),
    verification: document.getElementById('verification-result'),
    evidence: document.getElementById('evidence-ref'),
    error: document.getElementById('task-error'),
    correlation: document.getElementById('correlation-id'),
    timeline: document.getElementById('event-timeline'),
    footerTask: document.getElementById('task-state'),
    wsState: document.getElementById('ws-state'),
  },
  connectTaskLifecycle,
  state,
  {
    onTaskState(payload) {
      runtime.task = payload.lifecycleState || payload.lifecycle_state || 'idle';
      runtimeNodes.task.textContent = `Task ${(runtime.task || 'idle').toUpperCase()}`;
      updateTaskInspector(inspectorNodes, payload.lastPayload || payload);
    },
    onWebSocketState(nextState) {
      runtime.websocket = nextState;
      runtimeNodes.ws.textContent = `WS ${nextState.toUpperCase()}`;
    },
  },
);
const chat = mountChat(document.getElementById('chat-form'), document.getElementById('chat-log'), state, {
  onSubmitCommand(command) {
    taskUx.submit(command);
  },
});

observeGateway().then((probe) => {
  runtime.gateway = probe.status === 'observed' ? 'AVAILABLE' : probe.status === 'degraded' ? 'DEGRADED' : 'UNAVAILABLE';
  document.getElementById('health-state').textContent = `● Gateway ${runtime.gateway}: ${probe.detail}`;
});

loadGatewaySnapshot().then((items) => {
  window.EAOS_AIDE.gatewaySnapshot = items;
});

loadGatewayContracts().then((items) => {
  window.EAOS_AIDE.gatewayContracts = items;
});

loadCapabilityRegistry().then((envelope) => {
  window.EAOS_AIDE.capabilityRegistry = envelope;
  renderCapabilityRegistry(capabilitiesNode, envelope);
});

window.EAOS_AIDE = { agent, chat, commands, connectTaskLifecycle, editor, explorer, git, github, inspector, layout, readGatewayTask, renderTaskState, runtime, taskUx, telemetry, terminal, websocket, submitGatewayTask };
