# ADR 0001: Service Decomposition & Micro-Batching

- **Context**: We need to meet p99 ≤ 200ms with bursty traffic.
- **Decision**: Use stateless microservices per stage and a gateway that implements micro-batching and admission control.
- **Consequences**: Easier horizontal scaling, clear SLOs per stage, decoupled evolution, and safer canaries.
