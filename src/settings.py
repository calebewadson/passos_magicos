from pathlib import Path

PROJECT_ROOT=Path(__file__).resolve().parents[1]
DATA_DIR=PROJECT_ROOT/'data'
RAW_DATA_PATH=DATA_DIR/'raw'/'passos_magicos.xlsx'
ARTIFACTS_DIR=PROJECT_ROOT/'artifacts'
REPORTS_DIR=ARTIFACTS_DIR/'reports'
METRICS_DIR=ARTIFACTS_DIR/'metrics'
DRIFT_DIR=ARTIFACTS_DIR/'drift'
LOG_DIR=ARTIFACTS_DIR/'logs'
MODEL_DIR=PROJECT_ROOT/'app'/'model'
MODEL_PATH=MODEL_DIR/'model.joblib'
METADATA_PATH=MODEL_DIR/'metadata.json'
PREDICTIONS_LOG_PATH=ARTIFACTS_DIR/'predictions.jsonl'
RANDOM_SEED=42
MODEL_VERSION='1.0.0'
TARGET_NAME='target_risco_defasagem_proximo_ano'

for folder in [REPORTS_DIR,METRICS_DIR,DRIFT_DIR,LOG_DIR,MODEL_DIR]:
    folder.mkdir(parents=True,exist_ok=True)