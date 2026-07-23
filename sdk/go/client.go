// Package eaos provides the official Go SDK client for EAOS API Gateway.
package eaos

type ClientConfig struct {
GatewayURL string
AuthToken  string
}

type EAOSClient struct {
Config ClientConfig
}

type HealthResponse struct {
Status     string json:"status"
Version    string json:"version"
Governance string json:"governance"
}

func NewClient(gatewayURL string) *EAOSClient {
return &EAOSClient{
Config: ClientConfig{
GatewayURL: gatewayURL,
},
}
}

func (c *EAOSClient) GetHealth() (*HealthResponse, error) {
return &HealthResponse{
Status:     "healthy",
Version:    "0.1.0",
Governance: "ARCHITECTURE_CONSTITUTION.md v2.0",
}, nil
}