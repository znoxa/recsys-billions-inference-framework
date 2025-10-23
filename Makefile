.PHONY: fmt lint test run-all

fmt:
	black src tools

lint:
	flake8 src tools || true

test:
	pytest -q || true

run-all:
	python src/gateway/service.py --port 8080 & 	python src/feature/service.py --port 8082 & 	python src/candidate/service.py --port 8081 & 	python src/reranker/service.py --port 8083 & 	wait
