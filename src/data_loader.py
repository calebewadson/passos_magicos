import re
from dataclasses import dataclass
import pandas as pd
from src.settings import TARGET_NAME

@dataclass(frozen=True)
class DatasetBundle:
    raw_sheets: dict
    normalized_sheets: dict
    supervised: pd.DataFrame

COLUMN_MAP_BY_YEAR={
    2022:{
        'Nome':'nome_anonimizado',
        'Ano nasc':'ano_nascimento',
        'Idade 22':'idade',
        'Pedra 22':'pedra_atual',
        'INDE 22':'inde_atual',
        'Matem':'matematica',
        'Portug':'portugues',
        'Inglês':'ingles',
        'Fase ideal':'fase_ideal',
        'Defas':'defasagem'
    },
    2023:{
        'Nome Anonimizado':'nome_anonimizado',
        'Data de Nasc':'data_nascimento',
        'Pedra 2023':'pedra_atual',
        'INDE 2023':'inde_atual',
        'Mat':'matematica',
        'Por':'portugues',
        'Ing':'ingles',
        'Fase Ideal':'fase_ideal',
        'Defasagem':'defasagem'
    },
    2024:{
        'Nome Anonimizado':'nome_anonimizado',
        'Data de Nasc':'data_nascimento',
        'Pedra 2024':'pedra_atual',
        'INDE 2024':'inde_atual',
        'Mat':'matematica',
        'Por':'portugues',
        'Ing':'ingles',
        'Fase Ideal':'fase_ideal',
        'Defasagem':'defasagem',
        'Escola':'escola_nome',
        'Ativo/ Inativo':'status_matricula',
        'Ativo/ Inativo.1':'status_matricula_duplicado'
    }
}

COMMON_MAP={
    'RA':'ra',
    'Fase':'fase',
    'Turma':'turma',
    'Idade':'idade',
    'Gênero':'genero',
    'Ano ingresso':'ano_ingresso',
    'Instituição de ensino':'instituicao_ensino',
    'Pedra 20':'pedra_2020',
    'Pedra 21':'pedra_2021',
    'Pedra 22':'pedra_2022',
    'Pedra 23':'pedra_2023_historico',
    'INDE 22':'inde_2022_historico',
    'INDE 23':'inde_2023_historico',
    'Cg':'cg',
    'Cf':'cf',
    'Ct':'ct',
    'Nº Av':'num_avaliacoes',
    'Avaliador1':'avaliador_1',
    'Avaliador2':'avaliador_2',
    'Avaliador3':'avaliador_3',
    'Avaliador4':'avaliador_4',
    'Avaliador5':'avaliador_5',
    'Avaliador6':'avaliador_6',
    'Rec Av1':'recomendacao_av1',
    'Rec Av2':'recomendacao_av2',
    'Rec Av3':'recomendacao_av3',
    'Rec Av4':'recomendacao_av4',
    'IAA':'iaa',
    'IEG':'ieg',
    'IPS':'ips',
    'IPP':'ipp',
    'Rec Psicologia':'rec_psicologia',
    'IDA':'ida',
    'Indicado':'indicado',
    'Atingiu PV':'atingiu_pv',
    'IPV':'ipv',
    'IAN':'ian',
    'Destaque IEG':'destaque_ieg',
    'Destaque IDA':'destaque_ida',
    'Destaque IPV':'destaque_ipv'
}

def infer_year(sheet_name:str)->int:
    m=re.search(r'(20\d{2})',sheet_name)
    if not m: raise ValueError(f'Não foi possível inferir o ano da aba: {sheet_name}')
    return int(m.group(1))

def load_raw_sheets(workbook_path:str)->dict:
    excel_file=pd.ExcelFile(workbook_path)
    return {s:pd.read_excel(workbook_path,sheet_name=s) for s in excel_file.sheet_names}

def normalize_sheet(df:pd.DataFrame, year:int)->pd.DataFrame:
    renamed=df.rename(columns={**COMMON_MAP, **COLUMN_MAP_BY_YEAR.get(year,{})}).copy()
    renamed['ano_referencia']=year
    if 'data_nascimento' in renamed.columns:
        renamed['data_nascimento']=pd.to_datetime(renamed['data_nascimento'], errors='coerce')
    if 'ano_nascimento' in renamed.columns and 'idade' not in renamed.columns:
        renamed['idade']=year-pd.to_numeric(renamed['ano_nascimento'], errors='coerce')

    nums=[
        'idade','ano_ingresso','inde_atual','inde_2022_historico','inde_2023_historico',
        'iaa','ieg','ips','ipp','ida','ipv','ian','matematica','portugues','ingles',
        'num_avaliacoes','defasagem','cg','cf','ct'
    ]
    for c in nums:
        if c in renamed.columns:
            renamed[c]=pd.to_numeric(renamed[c], errors='coerce')

    renamed=renamed.drop_duplicates(subset=['ra']).reset_index(drop=True)
    return renamed

def normalize_all_sheets(raw_sheets):
    return {infer_year(k): normalize_sheet(v, infer_year(k)) for k,v in raw_sheets.items()}

def build_supervised_dataset(normalized_sheets):
    windows=[]
    years=sorted(normalized_sheets)
    for cur,nxt in zip(years[:-1], years[1:]):
        cur_df=normalized_sheets[cur].copy()
        nxt_df=normalized_sheets[nxt][['ra','defasagem']].rename(columns={'defasagem':'defasagem_proximo_ano'})
        merged=cur_df.merge(nxt_df,on='ra',how='inner')
        merged[TARGET_NAME]=(merged['defasagem_proximo_ano']<0).astype(int)
        merged['target_ordinal_proximo_ano']=merged['defasagem_proximo_ano']
        merged['ano_target']=nxt
        windows.append(merged)
    return pd.concat(windows, ignore_index=True)

def data_quality_report(df, top_n=20):
    report=pd.DataFrame({
        'coluna':df.columns,
        'dtype':[str(df[c].dtype) for c in df.columns],
        'nulos':[int(df[c].isna().sum()) for c in df.columns],
        'pct_nulos':[float(df[c].isna().mean()) for c in df.columns],
        'unicos':[int(df[c].nunique(dropna=True)) for c in df.columns]
    })
    return report.sort_values(['pct_nulos','unicos'], ascending=[False,False]).head(top_n).reset_index(drop=True)

def load_dataset_bundle(workbook_path:str)->DatasetBundle:
    raw=load_raw_sheets(workbook_path)
    normalized=normalize_all_sheets(raw)
    supervised=build_supervised_dataset(normalized)
    return DatasetBundle(raw, normalized, supervised)