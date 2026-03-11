from pathlib import Path
import matplotlib.pyplot as plt, numpy as np, pandas as pd
from sklearn.metrics import average_precision_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from src.settings import METRICS_DIR, REPORTS_DIR
from src.utils import safe_json_dump

def evaluate_predictions(y_true, y_pred, y_score):
    return {
        'recall_risco':float(recall_score(y_true,y_pred,pos_label=1)),
        'precision_risco':float(precision_score(y_true,y_pred,pos_label=1,zero_division=0)),
        'f1_risco':float(f1_score(y_true,y_pred,pos_label=1)),
        'roc_auc':float(roc_auc_score(y_true,y_score)),
        'pr_auc':float(average_precision_score(y_true,y_score)),
        'confusion_matrix':confusion_matrix(y_true,y_pred).tolist(),
        'classification_report':classification_report(y_true,y_pred,output_dict=True,zero_division=0)
    }

def persist_metrics(model_name, metrics):
    path=METRICS_DIR/f'{model_name}_metrics.json'
    safe_json_dump(metrics,path)
    return path

def save_feature_report(model_name, feature_names, importances):
    top=pd.DataFrame({'feature':feature_names,'importance':importances}).sort_values('importance', ascending=False).head(20)
    plt.figure(figsize=(10,7))
    plt.barh(top['feature'][::-1], top['importance'][::-1])
    plt.title(f'Top 20 features - {model_name}')
    plt.tight_layout()
    out=REPORTS_DIR/f'{model_name}_feature_importance.png'
    plt.savefig(out,dpi=150)
    plt.close()
    top.to_csv(REPORTS_DIR/f'{model_name}_feature_importance.csv', index=False)
    return out