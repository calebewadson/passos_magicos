import argparse, numpy as np, pandas as pd, joblib
from dataclasses import dataclass
from sklearn.base import clone
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from src.data_loader import data_quality_report, load_dataset_bundle
from src.evaluate import evaluate_predictions, persist_metrics, save_feature_report
from src.feature_engineering import FeatureBuilder
from src.logging_utils import get_logger, setup_logging
from src.preprocessing import build_preprocessor, required_input_columns
from src.settings import METADATA_PATH, MODEL_PATH, MODEL_VERSION, RANDOM_SEED, RAW_DATA_PATH, TARGET_NAME
from src.utils import safe_json_dump

setup_logging()
logger=get_logger(__name__)

@dataclass
class TrainingArtifacts:
    best_model_name:str
    best_metrics:dict
    metadata:dict

def build_candidates():
    return {
        'logistic_regression':LogisticRegression(max_iter=1000,class_weight='balanced',random_state=RANDOM_SEED),
        'random_forest':RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=RANDOM_SEED,
            n_jobs=-1
        ),
        'gradient_boosting':GradientBoostingClassifier(
            learning_rate=0.05,
            n_estimators=200,
            random_state=RANDOM_SEED
        )
    }

def build_pipeline(model):
    return Pipeline([
        ('feature_builder',FeatureBuilder()),
        ('preprocessor',build_preprocessor()),
        ('model',model)
    ])

def split_temporal(df):
    train_df=df[df['ano_referencia']==df['ano_referencia'].min()].copy()
    valid_df=df[df['ano_referencia']==df['ano_referencia'].max()].copy()
    return train_df, valid_df

def train_and_select_model(workbook_path=str(RAW_DATA_PATH)):
    bundle=load_dataset_bundle(workbook_path)
    supervised=bundle.supervised.copy()
    feature_columns=required_input_columns()
    train_df,valid_df=split_temporal(supervised)

    X_train=train_df.reindex(columns=feature_columns)
    y_train=train_df[TARGET_NAME]
    X_valid=valid_df.reindex(columns=feature_columns)
    y_valid=valid_df[TARGET_NAME]

    logger.info('Treinando modelos candidatos', extra={'train_shape':X_train.shape,'valid_shape':X_valid.shape})

    results={}
    candidates=build_candidates()

    for model_name, estimator in candidates.items():
        pipeline=build_pipeline(estimator)
        pipeline.fit(X_train,y_train)
        y_score=pipeline.predict_proba(X_valid)[:,1] if hasattr(pipeline,'predict_proba') else pipeline.predict(X_valid)
        y_pred=(y_score>=0.5).astype(int)
        metrics=evaluate_predictions(y_valid,y_pred,y_score)
        persist_metrics(model_name, metrics)
        results[model_name]=metrics
        logger.info('Modelo avaliado', extra={
            'model_name':model_name,
            'recall_risco':metrics['recall_risco'],
            'f1_risco':metrics['f1_risco']
        })

    best_model_name=sorted(
        results,
        key=lambda n:(results[n]['recall_risco'],results[n]['f1_risco'],results[n]['pr_auc']),
        reverse=True
    )[0]

    final_pipeline=build_pipeline(clone(candidates[best_model_name]))
    final_pipeline.fit(supervised.reindex(columns=feature_columns), supervised[TARGET_NAME])
    joblib.dump(final_pipeline, MODEL_PATH)

    data_quality_report(supervised).to_csv(
        MODEL_PATH.parents[2]/'artifacts'/'reports'/'data_quality_report.csv',
        index=False
    )

    feature_names=list(final_pipeline.named_steps['preprocessor'].get_feature_names_out())
    model_step=final_pipeline.named_steps['model']
    if hasattr(model_step,'feature_importances_'):
        save_feature_report(best_model_name, feature_names, model_step.feature_importances_)
    elif hasattr(model_step,'coef_'):
        save_feature_report(best_model_name, feature_names, np.abs(model_step.coef_[0]))

    metadata={
        'model_version':MODEL_VERSION,
        'best_model_name':best_model_name,
        'best_metrics_holdout':results[best_model_name],
        'all_model_metrics_holdout':results,
        'feature_columns':feature_columns,
        'train_window_years':[int(train_df['ano_referencia'].min()), int(train_df['ano_target'].max())],
        'validation_window_years':[int(valid_df['ano_referencia'].min()), int(valid_df['ano_target'].max())],
        'target_definition':'1 quando a defasagem do ano seguinte é negativa; 0 caso contrário.',
        'target_column_source':'Defas (2022) / Defasagem (2023, 2024), sempre deslocada para o próximo ano.',
        'n_labeled_rows':int(supervised.shape[0])
    }
    safe_json_dump(metadata, METADATA_PATH)
    return TrainingArtifacts(best_model_name, results[best_model_name], metadata)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workbook-path', default=str(RAW_DATA_PATH))
    args=parser.parse_args()
    art=train_and_select_model(args.workbook_path)
    logger.info('Treinamento concluído', extra={'best_model_name':art.best_model_name,'metrics':art.best_metrics})

if __name__=='__main__':
    main()