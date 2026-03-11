import argparse
import math
from collections.abc import Iterable

import numpy as np
import pandas as pd

from src.data_loader import load_dataset_bundle
from src.settings import DRIFT_DIR, RAW_DATA_PATH
from src.utils import safe_json_dump


EPSILON = 1e-6
MAX_PSI = 999.0


def _to_numeric_series(values: Iterable) -> pd.Series:
    series = values if isinstance(values, pd.Series) else pd.Series(list(values))
    return pd.to_numeric(series, errors="coerce").dropna()


def _sanitize_float(value: float | int | None) -> float | None:
    if value is None:
        return None
    value = float(value)
    if math.isnan(value) or math.isinf(value):
        return None
    return value


def population_stability_index(reference, current, bins: int = 10) -> float:
    ref = _to_numeric_series(reference)
    cur = _to_numeric_series(current)

    if ref.empty or cur.empty:
        return float("nan")

    quantiles = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(quantiles) < 3:
        return 0.0

    ref_bins = pd.cut(ref, bins=quantiles, include_lowest=True, duplicates="drop")
    cur_bins = pd.cut(cur, bins=quantiles, include_lowest=True, duplicates="drop")

    ref_dist = ref_bins.value_counts(normalize=True, sort=False)
    cur_dist = cur_bins.value_counts(normalize=True, sort=False).reindex(ref_dist.index, fill_value=0.0)

    ref_dist = ref_dist.astype(float).clip(lower=EPSILON)
    cur_dist = cur_dist.astype(float).clip(lower=EPSILON)

    psi = ((cur_dist - ref_dist) * np.log(cur_dist / ref_dist)).sum()

    if not np.isfinite(psi):
        return MAX_PSI

    return float(min(psi, MAX_PSI))


def compute_drift_report(workbook_path: str = str(RAW_DATA_PATH)):
    bundle = load_dataset_bundle(workbook_path)
    reference = bundle.normalized_sheets[min(bundle.normalized_sheets)]
    current = bundle.normalized_sheets[max(bundle.normalized_sheets)]

    numeric = [
        "idade",
        "iaa",
        "ieg",
        "ips",
        "ipp",
        "ida",
        "ipv",
        "ian",
        "inde_atual",
        "matematica",
        "portugues",
        "ingles",
    ]

    rows = []
    for col in numeric:
        if col in reference.columns and col in current.columns:
            psi = population_stability_index(reference[col], current[col])

            row = {
                "feature": col,
                "psi": _sanitize_float(psi),
                "missing_ref": _sanitize_float(reference[col].isna().mean()),
                "missing_cur": _sanitize_float(current[col].isna().mean()),
                "mean_ref": _sanitize_float(pd.to_numeric(reference[col], errors="coerce").mean()),
                "mean_cur": _sanitize_float(pd.to_numeric(current[col], errors="coerce").mean()),
            }
            rows.append(row)

    report_df = pd.DataFrame(rows)

    if not report_df.empty:
        report_df = report_df.sort_values("psi", ascending=False, na_position="last").reset_index(drop=True)

    report_df.to_csv(DRIFT_DIR / "drift_report.csv", index=False)
    safe_json_dump({"rows": report_df.to_dict(orient="records")}, DRIFT_DIR / "drift_report.json")

    html_rows = "\n".join(
        f"<tr><td>{r.feature}</td><td>{r.psi if r.psi is not None else 'N/A'}</td>"
        f"<td>{r.mean_ref if r.mean_ref is not None else 'N/A'}</td>"
        f"<td>{r.mean_cur if r.mean_cur is not None else 'N/A'}</td></tr>"
        for r in report_df.itertuples()
    )

    html = (
        "<html><body><h1>Relatório simples de drift</h1>"
        "<p>PSI acima de 0.2 sugere drift relevante; acima de 0.3 sugere drift forte.</p>"
        "<table border='1' cellpadding='6' cellspacing='0'>"
        "<tr><th>Feature</th><th>PSI</th><th>Média Referência</th><th>Média Atual</th></tr>"
        f"{html_rows}</table></body></html>"
    )

    out = DRIFT_DIR / "drift_report.html"
    out.write_text(html, encoding="utf-8")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook-path", default=str(RAW_DATA_PATH))
    args = parser.parse_args()
    print(compute_drift_report(args.workbook_path))


if __name__ == "__main__":
    main()