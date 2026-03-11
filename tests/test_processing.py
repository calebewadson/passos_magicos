from src.preprocessing import build_preprocessor, required_input_columns

def test_required_input_columns_has_key_fields():
    cols=required_input_columns()
    assert 'fase' in cols and 'idade' in cols and 'inde_atual' in cols

def test_build_preprocessor():
    assert build_preprocessor() is not None