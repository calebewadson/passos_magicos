import pandas as pd
from src.feature_engineering import FeatureBuilder

def test_feature_builder_creates_columns():
    frame=pd.DataFrame({
        'ano_referencia':[2023],
        'ano_ingresso':[2020],
        'idade':[12],
        'ingles':[7.0],
        'rec_psicologia':[None],
        'indicado':['Sim'],
        'atingiu_pv':['Não'],
        'portugues':[8.0],
        'matematica':[7.0],
        'ida':[6.0],
        'ieg':[8.0],
        'ipv':[7.5],
        'inde_atual':[7.0],
        'inde_2022_historico':[6.0],
        'inde_2023_historico':[6.5],
        'pedra_atual':['Topázio'],
        'pedra_2022':['Ágata'],
        'fase_ideal':['ALFA'],
        'fase':['ALFA']
    })
    transformed=FeatureBuilder().fit_transform(frame)
    assert transformed.loc[0,'tempo_programa']==3
    assert transformed.loc[0,'flag_possui_ingles']==1
    assert transformed.loc[0,'flag_fase_textualmente_compativel']==1