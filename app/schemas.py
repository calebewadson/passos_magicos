from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PredictRequest(BaseModel):
    model_config=ConfigDict(populate_by_name=True, extra='ignore')
    ano_referencia:int=Field(2024, alias='ano_referencia')
    Fase:str
    Turma:Optional[str]=None
    Idade:Optional[float]=None
    Gênero:Optional[str]=None
    Ano_ingresso:Optional[int]=Field(None, alias='Ano ingresso')
    Instituição_de_ensino:Optional[str]=Field(None, alias='Instituição de ensino')
    Pedra_2020:Optional[str]=Field(None, alias='Pedra 20')
    Pedra_2021:Optional[str]=Field(None, alias='Pedra 21')
    Pedra_2022:Optional[str]=Field(None, alias='Pedra 22')
    Pedra_23:Optional[str]=Field(None, alias='Pedra 23')
    Pedra_atual:Optional[str]=Field(None, alias='Pedra 2024')
    INDE_22:Optional[float]=Field(None, alias='INDE 22')
    INDE_23:Optional[float]=Field(None, alias='INDE 23')
    INDE_atual:Optional[float]=Field(None, alias='INDE 2024')
    Cg:Optional[float]=None
    Cf:Optional[float]=None
    Ct:Optional[float]=None
    Numero_Av:Optional[float]=Field(None, alias='Nº Av')
    IAA:Optional[float]=None
    IEG:Optional[float]=None
    IPS:Optional[float]=None
    IPP:Optional[float]=None
    IDA:Optional[float]=None
    Mat:Optional[float]=Field(None, alias='Mat')
    Por:Optional[float]=Field(None, alias='Por')
    Ing:Optional[float]=Field(None, alias='Ing')
    Indicado:Optional[str]=None
    Atingiu_PV:Optional[str]=Field(None, alias='Atingiu PV')
    IPV:Optional[float]=None
    IAN:Optional[float]=None
    Fase_Ideal:Optional[str]=Field(None, alias='Fase Ideal')
    Rec_Psicologia:Optional[str]=Field(None, alias='Rec Psicologia')
    Ativo_Inativo:Optional[str]=Field(None, alias='Ativo/ Inativo')

class PredictResponse(BaseModel):
    prediction:int
    risk_score:float
    risk_band:str
    model_version:str
    inference_timestamp:str
    status:str