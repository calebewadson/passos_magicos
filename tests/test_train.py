from src.train import split_temporal
from src.data_loader import load_dataset_bundle

def test_split_temporal(sample_workbook):
    bundle=load_dataset_bundle(str(sample_workbook))
    train_df,valid_df=split_temporal(bundle.supervised)
    assert train_df['ano_referencia'].nunique()==1
    assert valid_df['ano_referencia'].nunique()==1
    assert train_df['ano_referencia'].iloc[0] < valid_df['ano_referencia'].iloc[0]