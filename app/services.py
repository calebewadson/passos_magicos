import json
from src.predict import Predictor
from src.settings import PREDICTIONS_LOG_PATH
from src.utils import now_utc_iso

def request_to_model_input(payload):
    return {
        'ano_referencia':payload.get('ano_referencia',2024),
        'fase':payload.get('Fase'),
        'turma':payload.get('Turma'),
        'idade':payload.get('Idade'),
        'genero':payload.get('Gênero'),
        'ano_ingresso':payload.get('Ano ingresso'),
        'instituicao_ensino':payload.get('Instituição de ensino'),
        'pedra_2020':payload.get('Pedra 20'),
        'pedra_2021':payload.get('Pedra 21'),
        'pedra_2022':payload.get('Pedra 22'),
        'pedra_2023_historico':payload.get('Pedra 23'),
        'pedra_atual':payload.get('Pedra 2024'),
        'inde_2022_historico':payload.get('INDE 22'),
        'inde_2023_historico':payload.get('INDE 23'),
        'inde_atual':payload.get('INDE 2024'),
        'cg':payload.get('Cg'),
        'cf':payload.get('Cf'),
        'ct':payload.get('Ct'),
        'num_avaliacoes':payload.get('Nº Av'),
        'iaa':payload.get('IAA'),
        'ieg':payload.get('IEG'),
        'ips':payload.get('IPS'),
        'ipp':payload.get('IPP'),
        'ida':payload.get('IDA'),
        'matematica':payload.get('Mat'),
        'portugues':payload.get('Por'),
        'ingles':payload.get('Ing'),
        'indicado':payload.get('Indicado'),
        'atingiu_pv':payload.get('Atingiu PV'),
        'ipv':payload.get('IPV'),
        'ian':payload.get('IAN'),
        'fase_ideal':payload.get('Fase Ideal'),
        'rec_psicologia':payload.get('Rec Psicologia'),
        'status_matricula':payload.get('Ativo/ Inativo')
    }

class PredictionService:
    def __init__(self): self.predictor=Predictor()

    def predict(self, payload):
        result=self.predictor.predict_one(request_to_model_input(payload))
        result['inference_timestamp']=now_utc_iso()
        result['status']='success'
        PREDICTIONS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with PREDICTIONS_LOG_PATH.open('a', encoding='utf-8') as fp:
            fp.write(json.dumps({'request':payload,'response':result}, ensure_ascii=False)+'\n')
        return result