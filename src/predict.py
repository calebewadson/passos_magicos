import json, joblib, pandas as pd
from src.settings import METADATA_PATH, MODEL_PATH

class Predictor:
    def __init__(self, model_path=str(MODEL_PATH), metadata_path=str(METADATA_PATH)):
        self.pipeline=joblib.load(model_path)
        self.metadata=json.loads(open(metadata_path,'r',encoding='utf-8').read())
        self.feature_columns=self.metadata['feature_columns']

    def predict_one(self, payload):
        frame=pd.DataFrame([payload]).reindex(columns=self.feature_columns)
        score=float(self.pipeline.predict_proba(frame)[:,1][0])
        pred=int(score>=0.5)
        band='alto_risco' if score>=0.7 else 'medio_risco' if score>=0.4 else 'baixo_risco'
        return {
            'prediction':pred,
            'risk_score':round(score,6),
            'risk_band':band,
            'model_version':self.metadata['model_version']
        }