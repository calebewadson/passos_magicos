import numpy as np, pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

PEDRA_ORDER={'Quartzo':1,'Ágata':2,'Agata':2,'Ametista':3,'Topázio':4,'Topazio':4}

def yes_no_to_int(value):
    if pd.isna(value): return np.nan
    v=str(value).strip().lower()
    if v in {'sim','yes','true'}: return 1.0
    if v in {'não','nao','no','false'}: return 0.0
    return np.nan

class FeatureBuilder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self

    def transform(self, X):
        frame=X.copy()
        frame['tempo_programa']=frame['ano_referencia']-frame['ano_ingresso']
        frame['idade_x_tempo_programa']=frame['idade']*frame['tempo_programa']
        frame['flag_possui_ingles']=frame['ingles'].notna().astype(int)
        frame['flag_tem_rec_psicologia']=frame['rec_psicologia'].notna().astype(int)
        frame['flag_indicado']=frame['indicado'].map(yes_no_to_int)
        frame['flag_atingiu_pv']=frame['atingiu_pv'].map(yes_no_to_int)
        frame['media_notas_idioma']=frame[['portugues','ingles']].mean(axis=1)
        frame['media_academica']=frame[['matematica','portugues','ingles','ida']].mean(axis=1)
        frame['desvio_academico']=frame[['matematica','portugues','ingles','ida']].std(axis=1)
        frame['indice_engajamento_aprendizado']=frame[['ieg','ida','ipv']].mean(axis=1)
        frame['historico_inde_delta']=frame['inde_atual']-frame['inde_2022_historico']
        frame['historico_inde_delta_recente']=frame['inde_atual']-frame['inde_2023_historico']
        frame['pedra_atual_ord']=frame['pedra_atual'].map(PEDRA_ORDER)
        frame['pedra_2022_ord']=frame['pedra_2022'].map(PEDRA_ORDER)
        frame['evolucao_pedra']=frame['pedra_atual_ord']-frame['pedra_2022_ord']
        frame['missing_count']=frame.isna().sum(axis=1)

        categorical_columns=[
            'fase','turma','genero','instituicao_ensino','pedra_2020','pedra_2021',
            'pedra_2022','pedra_2023_historico','pedra_atual','fase_ideal',
            'rec_psicologia','status_matricula'
        ]
        for col in categorical_columns:
            if col in frame.columns:
                frame[col]=frame[col].where(frame[col].isna(), frame[col].astype(str))

        if 'fase_ideal' in frame.columns and 'fase' in frame.columns:
            frame['flag_fase_textualmente_compativel']=frame.apply(
                lambda r: int(str(r.get('fase','')) in str(r.get('fase_ideal','')))
                if pd.notna(r.get('fase')) and pd.notna(r.get('fase_ideal')) else 0,
                axis=1
            )
        return frame