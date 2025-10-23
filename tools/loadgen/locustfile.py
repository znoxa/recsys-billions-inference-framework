from locust import HttpUser, task, between
import random, time, json

class RecUser(HttpUser):
    wait_time = between(0.01, 0.2)

    @task
    def recommend(self):
        uid = f"u{random.randint(1, 10_000_000)}"
        payload = {"user_id": uid, "topk": random.choice([10,20,50]), "context": {"ts": int(time.time())}}
        self.client.post("/recommend", json=payload, name="recommend")
