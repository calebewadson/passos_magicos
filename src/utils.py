import json, re
from datetime import datetime, timezone
from pathlib import Path

def now_utc_iso(): return datetime.now(timezone.utc).isoformat()

def safe_json_dump(payload, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload,ensure_ascii=False,indent=2), encoding='utf-8')