import argparse, time, random, math
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from src.common.metrics import ensure_metrics, REQS, LAT

app = FastAPI()

class ReRankReq(BaseModel):
    user_features: dict
    candidates: list
    topk: int = 10

def mock_score(uf, item):
    # Cheap interaction score; placeholder for quantized transformer MLP head
    s = sum(uf.get("embedding", [0])*0 + (hash(item['item_id']) % 997) / 997.0)  # constant-ish seed
    return (hash(item['item_id']) % 1000)/1000.0 + random.random()*0.05

@app.post("/rerank")
async def rerank(req: ReRankReq):
    REQS.labels('reranker','rerank','in').inc()
    t0 = time.time()
    ranked = sorted(req.candidates, key=lambda it: mock_score(req.user_features, it), reverse=True)[: req.topk]
    # Attach explanations (placeholder) for debuggability
    for i, it in enumerate(ranked):
        it['explain'] = {'features': ['popularity','freshness','similarity'], 'rank': i+1}
    LAT.labels('reranker','rerank').observe(time.time()-t0)
    REQS.labels('reranker','rerank','ok').inc()
    return ranked

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8083)
    args = parser.parse_args()
    ensure_metrics(9003)
    logger.info("Re-ranker service on {}", args.port)
    import uvicorn
    uvicorn.run("src.reranker.service:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
