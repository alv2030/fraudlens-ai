.PHONY: setup data train seed-model api dashboard test docker-up docker-down spark-dry-run

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

data:
	python -m src.data.load_data --generate-demo

train:
	python -m src.models.train_model

seed-model:
	python -m src.models.seed_model

api:
	uvicorn src.api.main:app --reload --port 8000

dashboard:
	streamlit run src/dashboard/app.py

test:
	pytest -q

docker-up:
	docker compose up -d

docker-down:
	docker compose down


spark-dry-run:
	python -m src.streaming.spark_streaming_job --dry-run
