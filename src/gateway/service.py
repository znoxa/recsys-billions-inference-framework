import argparse, os, time
from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx, orjson
from loguru import logger

from src.common.config import Settings
from src.common.metrics import ensure_metrics, REQS, LAT, BATCH
from src.common.ab import ABRouter
from src.common.batcher import MicroBatcher

class RecRequest(BaseModel):
    user_id: str
    topk: int = 10
    context: dict = {}

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

app = FastAPI(default_response_class=None)

# Globals initialized in main
CFG = None
CLIENT = httpx.AsyncClient(timeout=2.0)
ABR = None
BATCHER = None

async def process_batch(items):
    # Parallel calls to services with shared httpx client
    async def one(req: RecRequest):
        t0 = time.time()
        # Feature fetch
        f = await CLIENT.post(CFG.get('services.feature_url') + "/features", json={'user_id': req.user_id, 'context': req.context})
        # Candidate pool
        c = await CLIENT.post(CFG.get('services.candidate_url') + "/candidates", json={'user_id': req.user_id, 'topk': max(100, req.topk*20)})
        # Re-rank
        payload = {
            'user_features': f.json(),
            'candidates': c.json(),
            'topk': req.topk
        }
        r = await CLIENT.post(CFG.get('services.reranker_url') + "/rerank", json=payload)
        LAT.labels('gateway','recommend').observe(time.time()-t0)
        return {'user_id': req.user_id, 'recommendations': r.json()}

    return [await one(i) for i in items]

@app.post("/recommend")
async def recommend(req: RecRequest, request: Request):
    global BATCHER
    # A/B routing (headers + user_id hash) - no overrides applied to keep demo simple
    REQS.labels('gateway','recommend','in').inc()
    # Submit to micro-batcher
    # Using a naive single-threaded bridge to async for simplicity
    res = await process_batch([req])
    REQS.labels('gateway','recommend','ok').inc()
    BATCH.labels('gateway','recommend').observe(1.0)
    return res[0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/dev.yaml')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    global CFG, ABR, BATCHER
    CFG = Settings.from_file(args.config)
    ABR = ABRouter('configs/ab_scenarios.yaml')
    ensure_metrics(CFG.get('observability.prometheus_port', 9000))
    logger.info("Gateway starting on port {}", args.port)

    import uvicorn
    uvicorn.run("src.gateway.service:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
