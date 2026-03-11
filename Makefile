install:
	python -m pip install -r requirements.txt

train:
	python -m src.train

drift:
	python -m src.monitor

api:
	uvicorn app.main:app --reload

dashboard:
	streamlit run monitoring_dashboard.py

test:
	pytest

coverage:
	pytest --cov=app --cov=src --cov-report=term-missing --cov-report=html