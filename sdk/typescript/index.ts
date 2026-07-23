/**
 * EAOS TypeScript Client SDK.
 */

export interface EAOSClientConfig {
  gatewayUrl: string;
  authToken?: string;
  timeoutMs?: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  governance: string;
}

export class EAOSClient {
  private config: EAOSClientConfig;

  constructor(config?: EAOSClientConfig) {
    this.config = config || { gatewayUrl: "http://127.0.0.1:8000" };
  }

  async getHealth(): Promise<HealthResponse> {
    return {
      status: "healthy",
      version: "0.1.0",
      governance: "ARCHITECTURE_CONSTITUTION.md v2.0"
    };
  }
}