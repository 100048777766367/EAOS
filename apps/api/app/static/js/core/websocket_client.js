/**
 * EAOS WebSocket client.
 *
 * Location:
 * apps/api/app/static/js/core/websocket_client.js
 */

export class WSClient {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.handlers = new Map();
        this.reconnectTimer = null;
        this.reconnectDelay = 3000;
        this.closedManually = false;
    }

    connect() {
        if (
            this.socket &&
            (
                this.socket.readyState === WebSocket.OPEN ||
                this.socket.readyState === WebSocket.CONNECTING
            )
        ) {
            return;
        }

        this.closedManually = false;

        try {
            this.socket = new WebSocket(this.url);
        } catch (error) {
            this.emit('error', {
                error,
                message: 'Unable to create WebSocket connection.',
            });
            this.scheduleReconnect();
            return;
        }

        this.socket.onopen = () => {
            this.reconnectDelay = 3000;

            this.emit('connection_changed', {
                connected: true,
                state: 'OPEN',
            });
        };

        this.socket.onmessage = (event) => {
            let payload;

            try {
                payload = JSON.parse(event.data);
            } catch (error) {
                this.emit('error', {
                    error,
                    message: 'Received invalid WebSocket JSON.',
                    raw: event.data,
                });
                return;
            }

            if (!payload || typeof payload !== 'object') {
                return;
            }

            const type = payload.type || 'message';
            this.emit(type, payload);
            this.emit('message', payload);
        };

        this.socket.onerror = (error) => {
            this.emit('error', {
                error,
                message: 'EAOS WebSocket error.',
            });
        };

        this.socket.onclose = (event) => {
            this.emit('connection_changed', {
                connected: false,
                state: 'CLOSED',
                code: event.code,
                reason: event.reason,
            });

            this.socket = null;

            if (!this.closedManually) {
                this.scheduleReconnect();
            }
        };
    }

    scheduleReconnect() {
        if (this.closedManually || this.reconnectTimer) {
            return;
        }

        this.reconnectTimer = window.setTimeout(() => {
            this.reconnectTimer = null;
            this.connect();
        }, this.reconnectDelay);
    }

    disconnect() {
        this.closedManually = true;

        if (this.reconnectTimer) {
            window.clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }

        if (this.socket) {
            this.socket.close(1000, 'Client shutdown');
            this.socket = null;
        }
    }

    isConnected() {
        return Boolean(
            this.socket &&
            this.socket.readyState === WebSocket.OPEN
        );
    }

    send(message) {
        if (!this.isConnected()) {
            this.emit('error', {
                message: 'WebSocket is not connected.',
            });
            return false;
        }

        try {
            this.socket.send(JSON.stringify(message));
            return true;
        } catch (error) {
            this.emit('error', {
                error,
                message: 'Failed to send WebSocket message.',
            });
            return false;
        }
    }

    on(type, callback) {
        if (!this.handlers.has(type)) {
            this.handlers.set(type, []);
        }

        this.handlers.get(type).push(callback);

        return () => this.off(type, callback);
    }

    off(type, callback) {
        const callbacks = this.handlers.get(type);

        if (!callbacks) {
            return;
        }

        const filtered = callbacks.filter(
            (registered) => registered !== callback
        );

        if (filtered.length === 0) {
            this.handlers.delete(type);
            return;
        }

        this.handlers.set(type, filtered);
    }

    emit(type, payload) {
        const callbacks = this.handlers.get(type);

        if (!callbacks) {
            return;
        }

        for (const callback of callbacks) {
            try {
                callback(payload);
            } catch (error) {
                console.error(
                    `[EAOS WS] Handler error for "${type}"`,
                    error
                );
            }
        }
    }
}
