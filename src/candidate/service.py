import argparse, time, random
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from src.common.metrics import ensure_metrics, REQS, LAT

app = FastAPI()

class CandReq(BaseModel):
    user_id: str
    topk: int = 200

@app.post("/candidates")
async def candidates(req: CandReq):
    REQS.labels('candidate','candidates','in').inc()
    t0 = time.time()
    # Simulate ANN lookup and business filtering
    time.sleep(0.003 + random.random()*0.006)
    pool = [{"item_id": f"i{random.randint(1, 10_000_000)}", "score": random.random()} for _ in range(req.topk)]
    LAT.labels('candidate','candidates').observe(time.time()-t0)
    REQS.labels('candidate','candidates','ok').inc()
    return pool

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8081)
    args = parser.parse_args()
    ensure_metrics(9001)
    logger.info("Candidate service on {}", args.port)
    import uvicorn
    uvicorn.run("src.candidate.service:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
