from pathlib import Path

from fastapi.testclient import TestClient

import app.main as main_module
from app.services import request_to_model_input
from src.monitor import compute_drift_report, population_stability_index
from src.predict import Predictor
from src.train import build_candidates


def test_build_candidates():
    candidates = build_candidates()
    assert set(candidates) == {"logistic_regression", "random_forest", "gradient_boosting"}


def test_predictor_real_model():
    predictor = Predictor()
    payload = {
        "ano_referencia": 2024,
        "fase": "ALFA",
        "turma": "ALFA A - G0/G1",
        "idade": 8,
        "genero": "Feminino",
        "ano_ingresso": 2024,
        "instituicao_ensino": "Pública",
        "pedra_atual": "Ametista",
        "inde_atual": 7.6,
        "num_avaliacoes": 3,
        "iaa": 10.0,
        "ieg": 8.6,
        "ips": 6.2,
        "ipp": 5.6,
        "ida": 8.0,
        "matematica": 10.0,
        "portugues": 6.0,
        "ingles": None,
        "ipv": 5.4,
        "ian": 10,
        "fase_ideal": "ALFA (1° e 2° ano)",
        "status_matricula": "Cursando",
    }
    result = predictor.predict_one(payload)
    assert 0.0 <= result["risk_score"] <= 1.0
    assert result["risk_band"] in {"baixo_risco", "medio_risco", "alto_risco"}


def test_population_stability_index():
    psi = population_stability_index([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    assert psi >= 0.0


def test_compute_drift_report(sample_workbook):
    path = compute_drift_report(str(sample_workbook))
    assert Path(path).exists()


def test_version_endpoint():
    client = TestClient(main_module.app)
    response = client.get("/version")
    assert response.status_code == 200
    payload = response.json()
    assert "model_version" in payload and "best_model_name" in payload


def test_request_to_model_input_mapping():
    payload = {
        "Fase": "ALFA",
        "Ano ingresso": 2024,
        "Instituição de ensino": "Pública",
        "INDE 2024": 8.1,
        "Atingiu PV": "Sim",
        "Ativo/ Inativo": "Cursando",
    }
    mapped = request_to_model_input(payload)
    assert mapped["fase"] == "ALFA"
    assert mapped["ano_ingresso"] == 2024
    assert mapped["instituicao_ensino"] == "Pública"
    assert mapped["inde_atual"] == 8.1
    assert mapped["atingiu_pv"] == "Sim"
    assert mapped["status_matricula"] == "Cursando"