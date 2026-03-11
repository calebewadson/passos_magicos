from app.services import request_to_model_input

def test_request_to_model_input_maps_fields():
    mapped=request_to_model_input({'Fase':'ALFA','Ano ingresso':2023,'INDE 2024':8.5})
    assert mapped['fase']=='ALFA'
    assert mapped['ano_ingresso']==2023
    assert mapped['inde_atual']==8.5