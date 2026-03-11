from pathlib import Path
import pandas as pd, streamlit as st
ROOT=Path(__file__).resolve().parent; drift_path=ROOT/'artifacts'/'drift'/'drift_report.csv'; pred_path=ROOT/'artifacts'/'predictions.jsonl'
st.set_page_config(page_title='Passos Mágicos Monitoring', layout='wide'); st.title('Passos Mágicos - Monitoramento')
if drift_path.exists(): st.subheader('Drift report'); st.dataframe(pd.read_csv(drift_path), use_container_width=True)
else: st.info('Execute `python -m src.monitor` para gerar o relatório de drift.')
if pred_path.exists(): st.subheader('Predições registradas'); st.dataframe(pd.read_json(pred_path, lines=True).tail(100), use_container_width=True)
else: st.info('Nenhuma predição registrada ainda.')