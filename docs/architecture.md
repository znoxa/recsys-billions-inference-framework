# System Architecture

**Goal:** Real-time recommendation inference at billion-user scale with strict latency SLOs (p50 ≤ 50ms, p99 ≤ 200ms end-to-end).

## Components
- **Gateway**: request admission control, **micro-batching**, deadline-aware fanout, AB/shadow routing.
- **Feature Service**: async retrieval from feature store; supports **fallback defaults** on timeout.
- **Candidate Service**: ANN-based candidate gen (interface for FAISS/ScaNN/HNSW), business rules.
- **Re-Ranker**: calibrated scoring; supports **quantization** and **distilled** small models for cost efficiency.

## Data Flow
1. Gateway receives request with latency budget.
2. Parallel async calls to Feature + Candidate; short-circuit on timeouts with fallbacks.
3. Re-Ranker computes final top-K.
4. Observability hooks collect latency histograms; dashboards compute SLOs (RED/USE).

## Scale Strategies
- **Dynamic Micro-Batching** to amortize compute.
- **Priority Lanes** for interactive sessions.
- **Edge Cache** for repeated sessions.
- **Shard-by-User** to maximize locality (sticky hashing).
- **Stateless Workers** behind HPA with QPS‑based scaling.
