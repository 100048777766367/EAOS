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
import { mountInspector } from '../ide/inspector.js';
import { loadGatewayContracts, loadGatewaySnapshot } from '../runtime/contracts.js';
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
const chat = mountChat(document.getElementById('chat-form'), document.getElementById('chat-log'), state);
const agent = mountAgentStatus(document.getElementById('agent-status'));
const git = mountGit(document.getElementById('git-state'));
const github = githubContract(state);
const inspector = mountInspector(document.getElementById('inspector'), state.capabilities || []);
const websocket = describeWebSocketContract(state);
const telemetry = telemetryContract(state);
const commands = registerCommands();
const layout = enableWorkspaceLayout(shell);
const taskUx = mountTaskUx(
  {
    taskId: document.getElementById('task-id'),
    currentState: document.getElementById('current-lifecycle'),
    governance: document.getElementById('governance-result'),
    evidence: document.getElementById('evidence-ref'),
    error: document.getElementById('task-error'),
    correlation: document.getElementById('correlation-id'),
    timeline: document.getElementById('event-timeline'),
    footerTask: document.getElementById('task-state'),
    wsState: document.getElementById('ws-state'),
  },
  connectTaskLifecycle,
  state,
);

observeGateway().then((probe) => {
  runtime.gateway = probe.status;
  document.getElementById('health-state').textContent = `● Gateway ${probe.status}: ${probe.detail}`;
});

loadGatewaySnapshot().then((items) => {
  window.EAOS_AIDE.gatewaySnapshot = items;
});

loadGatewayContracts().then((items) => {
  window.EAOS_AIDE.gatewayContracts = items;
});

window.EAOS_AIDE = { agent, chat, commands, connectTaskLifecycle, editor, explorer, git, github, inspector, layout, readGatewayTask, renderTaskState, runtime, taskUx, telemetry, terminal, websocket, submitGatewayTask };
