# Tracing & SLOs

- Use distributed trace IDs propagated via `x-trace-id`.
- Record stage timings; correlate with histograms.
- Define SLOs as Prometheus burn rates; alert when error budget is consumed faster than threshold (e.g., 2%/hour).
