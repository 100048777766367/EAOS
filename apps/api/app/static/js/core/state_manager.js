class StateManager {
    constructor() {
        this.state = {
            activeFile: 'apps/api/app/routers/chat.py',
            activeBranch: 'main',
            selectedModel: 'claude-3-5-sonnet',
            selectedAgentRole: 'coder',
            isExecuting: false,
            patchDiff: ''
        };
        this.listeners = new Map();
    }

    subscribe(key, callback) {
        if (!this.listeners.has(key)) this.listeners.set(key, []);
        this.listeners.get(key).push(callback);
    }

    setState(key, value) {
        this.state[key] = value;
        if (this.listeners.has(key)) {
            this.listeners.get(key).forEach(cb => cb(value));
        }
    }

    getState(key) { return this.state[key]; }
}

export const ideState = new StateManager();
