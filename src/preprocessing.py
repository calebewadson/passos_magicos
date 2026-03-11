from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_FEATURES=[
    'ano_referencia','fase','turma','idade','genero','ano_ingresso','instituicao_ensino',
    'pedra_2020','pedra_2021','pedra_2022','pedra_2023_historico','pedra_atual',
    'inde_2022_historico','inde_2023_historico','inde_atual','cg','cf','ct',
    'num_avaliacoes','iaa','ieg','ips','ipp','ida','matematica','portugues','ingles',
    'indicado','atingiu_pv','ipv','ian','fase_ideal','rec_psicologia','status_matricula'
]

ENG=[
    'tempo_programa','idade_x_tempo_programa','flag_possui_ingles','flag_tem_rec_psicologia',
    'flag_indicado','flag_atingiu_pv','media_notas_idioma','media_academica',
    'desvio_academico','indice_engajamento_aprendizado','historico_inde_delta',
    'historico_inde_delta_recente','pedra_atual_ord','pedra_2022_ord',
    'evolucao_pedra','missing_count','flag_fase_textualmente_compativel'
]

NUM=[
    'ano_referencia','idade','ano_ingresso','inde_2022_historico','inde_2023_historico',
    'inde_atual','cg','cf','ct','num_avaliacoes','iaa','ieg','ips','ipp','ida',
    'matematica','portugues','ingles','ipv','ian',*ENG
]

CAT=[
    'fase','turma','genero','instituicao_ensino','pedra_2020','pedra_2021',
    'pedra_2022','pedra_2023_historico','pedra_atual','fase_ideal',
    'rec_psicologia','status_matricula'
]

def build_preprocessor():
    num=Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())])
    cat=Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('encoder',OneHotEncoder(handle_unknown='ignore'))])
    return ColumnTransformer([('num',num,NUM),('cat',cat,CAT)], remainder='drop')

def required_input_columns(): return list(dict.fromkeys(BASE_FEATURES))