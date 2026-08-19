import { observeGateway } from './gateway.js';
import { readBootstrapState } from './state.js';
import { describeWebSocketContract } from './websocket.js';
import { mountAgentStatus } from '../agent/status.js';
import { submitGatewayTask } from '../agent/tasks.js';
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
const editor = mountEditor(document.getElementById('monaco-editor'), document.getElementById('editor-tabs'));
const explorer = mountExplorer(document.getElementById('workspace-tree'));
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

observeGateway().then((probe) => {
  document.getElementById('health-state').textContent = `● Gateway ${probe.status}: ${probe.detail}`;
});

loadGatewaySnapshot().then((items) => {
  window.EAOS_AIDE.gatewaySnapshot = items;
});

loadGatewayContracts().then((items) => {
  window.EAOS_AIDE.gatewayContracts = items;
});

window.EAOS_AIDE = { agent, chat, commands, editor, explorer, git, github, inspector, layout, runtime, telemetry, terminal, websocket, submitGatewayTask };
