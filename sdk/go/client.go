package eaos_sdk

import (
    "context"
    "fmt"
)

type Client struct {
    Endpoint string
}

func NewClient(endpoint string) *Client {
    return &Client{Endpoint: endpoint}
}

func (c *Client) Ping(ctx context.Context) (string, error) {
    return fmt.Sprintf("Pong from EAOS Go SDK at %s", c.Endpoint), nil
}
