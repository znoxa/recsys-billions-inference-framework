# Benchmark Plan

We evaluate **latency–throughput** and **tail-latency** under varying batch sizes, cache hit rates, and service fanout.

## Metrics
- p50/p95/p99 latency per stage + end-to-end.
- Throughput (RPS), CPU/GPU util (if applicable).
- Error budget burn rate.

## Load Generation
`tools/loadgen/locustfile.py` simulates user traffic with configurable distributions (Poisson bursty, Zipf user repetition).

## Experiments
1. **Batch Size Sweep**: 16 → 128, record latency/TPS.
2. **Timeouts & Fallbacks**: feature timeouts from 2ms → 20ms.
3. **Cache Ablation**: hit rate from 0% → 90%.
4. **A/B Batching**: control vs tuned settings (`configs/ab_scenarios.yaml`).

## Output
- CSV logs under `artifacts/` (created by scripts).
- Prometheus histograms for dashboards.
