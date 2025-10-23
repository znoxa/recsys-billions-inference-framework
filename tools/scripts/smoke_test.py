import requests, time, json, sys

def main():
    for _ in range(3):
        r = requests.post("http://localhost:8080/recommend", json={"user_id":"u1","topk":5,"context":{}})
        print(r.status_code, r.json())
        time.sleep(0.2)

if __name__ == "__main__":
    main()
