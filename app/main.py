import json
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from app.logging_config import setup_logging  # noqa: F401
from app.schemas import PredictRequest, PredictResponse
from app.services import PredictionService
from src.settings import METADATA_PATH

app=FastAPI(title='Passos Mágicos Risk API', version='1.0.0')

@lru_cache
def get_service(): return PredictionService()

@app.get('/health')
def health(): return {'status':'ok'}

@app.get('/version')
def version():
    metadata=json.loads(open(METADATA_PATH,'r',encoding='utf-8').read())
    return {'model_version':metadata['model_version'],'best_model_name':metadata['best_model_name'],'target_definition':metadata['target_definition']}

@app.post('/predict', response_model=PredictResponse)
def predict(payload: PredictRequest):
    try: return PredictResponse(**get_service().predict(payload.model_dump(by_alias=True)))
    except Exception as exc: raise HTTPException(status_code=500, detail=str(exc)) from exc