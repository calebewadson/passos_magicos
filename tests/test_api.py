from fastapi.testclient import TestClient
import app.main as main_module

class DummyService:
    def predict(self, payload):
        return {
            'prediction':1,
            'risk_score':0.82,
            'risk_band':'alto_risco',
            'model_version':'test',
            'inference_timestamp':'2026-03-10T00:00:00+00:00',
            'status':'success'
        }

def test_health():
    client=TestClient(main_module.app)
    response=client.get('/health')
    assert response.status_code==200 and response.json()['status']=='ok'

def test_predict(monkeypatch):
    monkeypatch.setattr(main_module, 'get_service', lambda: DummyService())
    client=TestClient(main_module.app)
    response=client.post('/predict', json={'Fase':'ALFA','Ano ingresso':2024,'INDE 2024':8.2})
    assert response.status_code==200
    assert response.json()['prediction']==1