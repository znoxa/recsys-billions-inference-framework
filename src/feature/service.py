import argparse, time, random
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from src.common.metrics import ensure_metrics, REQS, LAT

app = FastAPI()

class FeatureReq(BaseModel):
    user_id: str
    context: dict = {}

@app.post("/features")
async def features(req: FeatureReq):
    REQS.labels('feature','features','in').inc()
    t0 = time.time()
    # Simulate feature fetch with deadlines & fallbacks
    time.sleep(0.002 + random.random()*0.004)
    feats = {
        "age_bucket": random.choice(["18-24","25-34","35-44","45-54"]),
        "country": random.choice(["US","IN","BR","ID","DE","FR"]),
        "embedding": [random.random() for _ in range(32)],
        "freshness_s": random.randint(0, 3600)
    }
    LAT.labels('feature','features').observe(time.time()-t0)
    REQS.labels('feature','features','ok').inc()
    return feats

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8082)
    args = parser.parse_args()
    ensure_metrics(9002)
    logger.info("Feature service on {}", args.port)
    import uvicorn
    uvicorn.run("src.feature.service:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
