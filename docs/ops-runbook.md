# Ops Runbook

## SLOs
- E2E: p50 ≤ 50ms; p99 ≤ 200ms.
- Availability: ≥ 99.95% monthly.

## Common Issues
- **Tail-latency spikes** → check saturation, thundering herd, cache miss storms.
- **HPA thrashing** → stabilize with longer windows, pod anti-affinity.
- **Cold starts (serverless)** → pre-warm pools, keep-alive connections.

## Playbooks
- **Canary roll**: route 1% via header `x-exp: canary` → expand to 10% → 100%.
- **Shadow deploy**: header `x-exp: shadow-r2` (treated as shadow).

## Dashboards
- RED: request rate, errors, duration.
- USE: utilization, saturation, errors.
