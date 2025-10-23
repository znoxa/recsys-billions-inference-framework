# Distributed Inference Frameworks for Real-Time Recommendation Systems under Billion-User Scale

**Short description:** Reference framework for **distributed, real‑time recommendation inference** at **billion‑user** scale. Includes architecture, microservices (gateway, feature service, candidate gen, re-ranker), **dynamic micro-batching**, **vector retrieval**, **asynchronous caching**, **A/B testing hooks**, **observability**, **benchmark harness**, and **Kubernetes** deployment examples.

> This is a research/teaching reference. The code runs locally in simulated mode; cloud and vendor hooks are pluggable.

---

## Highlights
- **Gateway** with latency budgets, **token-bucket QPS control**, **micro-batching**, and **priority lanes**.
- **Candidate Generation** with pluggable ANN backends (mock + interface for FAISS, ScaNN, HNSW).
- **Re-Ranker** with quantization-ready scoring (mock transformer) and **distillation** placeholders.
- **Async feature fetch** (mock feature store) with deadline-aware fallbacks and default profiles.
- **A/B & Shadow traffic** via headers and deterministic hashing.
- **Observability**: Prometheus-style metrics, structured logs, request tracing, RED/USE SLOs.
- **Benchmarks**: Load generation (locust), latency–throughput curves, tail-latency diagnostics, cache ablations.
- **Ops**: Dockerfiles, K8s manifests, GitHub Actions CI, Makefile, config profiles (dev/stage/prod).

---

## Quick Start (local, simulated)
```bash
# 1) Create and activate a virtualenv (recommended)
python3 -m venv .venv && source .venv/bin/activate

# 2) Install minimal deps
pip install -r requirements.txt

# 3) Run services (each in its own shell)
python src/gateway/service.py --port 8080
python src/candidate/service.py --port 8081
python src/feature/service.py --port 8082
python src/reranker/service.py --port 8083

# 4) Send a test request
curl -s -X POST "http://localhost:8080/recommend" -H "Content-Type: application/json"   -d '{"user_id":"u123","topk":10,"context":{"device":"ios","ts":1699999999}}' | jq
```

> The mock services are intentionally lightweight (no external infra needed). Replace adapters under `src/*/adapters/` to integrate with your stack.

---

## Repository Layout
```
.
├── README.md
├── LICENSE
├── Makefile
├── requirements.txt
├── pyproject.toml
├── configs/
│   ├── dev.yaml
│   ├── prod.yaml
│   └── ab_scenarios.yaml
├── src/
│   ├── common/...
│   ├── gateway/...
│   ├── candidate/...
│   ├── feature/...
│   └── reranker/...
├── docs/
│   ├── architecture.md
│   ├── adr/0001-architecture-decisions.md
│   ├── ops-runbook.md
│   ├── benchmarks.md
│   ├── ab-testing.md
│   └── tracing-and-slos.md
├── deploy/
│   ├── docker/
│   │   ├── Dockerfile.gateway
│   │   ├── Dockerfile.candidate
│   │   ├── Dockerfile.feature
│   │   └── Dockerfile.reranker
│   └── k8s/
│       ├── gateway.yaml
│       ├── candidate.yaml
│       ├── feature.yaml
│       └── reranker.yaml
├── tools/
│   ├── loadgen/locustfile.py
│   ├── scripts/smoke_test.py
│   └── dashboards/prometheus_rules.yaml
└── .github/workflows/ci.yml
```
See `docs/architecture.md` and `docs/benchmarks.md` for details.
