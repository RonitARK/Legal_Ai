import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "labour_codes"

def load_rules_context() -> str:
    context_parts = []
    files = {
        "code_on_wages.json": "Code on Wages, 2019",
        "industrial_relations.json": "Industrial Relations Code, 2020",
        "social_security.json": "Social Security Code, 2020",
        "osh_code.json": "OSH Code, 2020",
    }
    for filename, label in files.items():
        path = DATA_DIR / filename
        if path.exists():
            data = json.loads(path.read_text())
            context_parts.append(f"=== {label} ===\n{json.dumps(data, indent=2)}")

    return "\n\n".join(context_parts)