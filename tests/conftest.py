from pathlib import Path
import pandas as pd, pytest

@pytest.fixture()
def sample_workbook(tmp_path: Path):
    path=tmp_path/'sample.xlsx'
    df22=pd.DataFrame({
        'RA':['A','B','C'],
        'Fase':[1,2,3],
        'Turma':['A','B','C'],
        'Nome':['Aluno A','Aluno B','Aluno C'],
        'Ano nasc':[2012,2011,2010],
        'Idade 22':[10,11,12],
        'Gênero':['Menina','Menino','Menina'],
        'Ano ingresso':[2020,2021,2020],
        'Instituição de ensino':['Pública','Privada','Pública'],
        'Pedra 22':['Quartzo','Ágata','Topázio'],
        'INDE 22':[5.0,6.0,8.0],
        'Nº Av':[2,2,2],
        'IAA':[7.0,8.0,9.0],
        'IEG':[6.0,7.0,8.0],
        'IPS':[5.0,6.0,7.0],
        'IDA':[6.5,7.5,8.5],
        'Matem':[6.0,7.0,8.0],
        'Portug':[6.0,7.0,8.0],
        'Inglês':[5.0,6.0,7.0],
        'Atingiu PV':['Não','Sim','Não'],
        'IPV':[5.0,6.0,8.0],
        'IAN':[5,6,7],
        'Fase ideal':['Fase 1','Fase 2','Fase 3'],
        'Defas':[-1,0,1]
    })
    df23=pd.DataFrame({
        'RA':['A','B','C'],
        'Fase':['ALFA','BETA','GAMA'],
        'Turma':['A','B','C'],
        'Nome Anonimizado':['Aluno A','Aluno B','Aluno C'],
        'Data de Nasc':['2012-01-01','2011-01-01','2010-01-01'],
        'Idade':[11,12,13],
        'Gênero':['Feminino','Masculino','Feminino'],
        'Ano ingresso':[2020,2021,2020],
        'Instituição de ensino':['Pública','Privada','Pública'],
        'Pedra 2023':['Quartzo','Ágata','Topázio'],
        'INDE 2023':[5.5,6.5,8.5],
        'Nº Av':[2,2,2],
        'IAA':[7.5,8.5,9.5],
        'IEG':[6.5,7.5,8.5],
        'IPS':[5.5,6.5,7.5],
        'IPP':[5.2,6.2,7.2],
        'IDA':[6.7,7.7,8.7],
        'Mat':[6.2,7.2,8.2],
        'Por':[6.1,7.1,8.1],
        'Ing':[5.1,6.1,7.1],
        'Atingiu PV':['Não','Sim','Não'],
        'IPV':[5.3,6.3,8.3],
        'IAN':[5,6,7],
        'Fase Ideal':['ALFA','BETA','GAMA'],
        'Defasagem':[-1,0,1]
    })
    df24=pd.DataFrame({
        'RA':['A','B','C'],
        'Fase':['ALFA','BETA','GAMA'],
        'Turma':['A','B','C'],
        'Nome Anonimizado':['Aluno A','Aluno B','Aluno C'],
        'Data de Nasc':['2012-01-01','2011-01-01','2010-01-01'],
        'Idade':[12,13,14],
        'Gênero':['Feminino','Masculino','Feminino'],
        'Ano ingresso':[2020,2021,2020],
        'Instituição de ensino':['Pública','Privada','Pública'],
        'Pedra 2024':['Quartzo','Ágata','Topázio'],
        'INDE 2024':[5.8,6.8,8.8],
        'Nº Av':[3,3,3],
        'IAA':[7.8,8.8,9.8],
        'IEG':[6.8,7.8,8.8],
        'IPS':[5.8,6.8,7.8],
        'IPP':[5.4,6.4,7.4],
        'IDA':[6.9,7.9,8.9],
        'Mat':[6.4,7.4,8.4],
        'Por':[6.3,7.3,8.3],
        'Ing':[5.4,6.4,7.4],
        'Atingiu PV':['Não','Sim','Não'],
        'IPV':[5.5,6.5,8.5],
        'IAN':[5,6,7],
        'Fase Ideal':['ALFA','BETA','GAMA'],
        'Defasagem':[-1,0,1],
        'Ativo/ Inativo':['Cursando','Cursando','Cursando']
    })
    with pd.ExcelWriter(path) as writer:
        df22.to_excel(writer, sheet_name='PEDE2022', index=False)
        df23.to_excel(writer, sheet_name='PEDE2023', index=False)
        df24.to_excel(writer, sheet_name='PEDE2024', index=False)
    return path