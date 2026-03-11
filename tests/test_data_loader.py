from src.data_loader import infer_year, load_dataset_bundle

def test_infer_year():
    assert infer_year('PEDE2024')==2024

def test_load_dataset_bundle(sample_workbook):
    bundle=load_dataset_bundle(str(sample_workbook))
    assert set(bundle.normalized_sheets)=={2022,2023,2024}
    assert 'target_risco_defasagem_proximo_ano' in bundle.supervised.columns
    assert bundle.supervised.shape[0]==6