import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise/PCN_screening")


def parse_articles(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    decisions = Counter()
    reasons = Counter()
    reason_combinations = Counter()
    missing_decision = []
    excluded_without_reason = []
    included_with_reason = []
    keys = Counter()

    for row in rows:
        note = row.get("notes", "") or ""
        m = re.search(r'RAYYAN-INCLUSION: \{"Anna"=>"([^"]+)"\}', note)
        decision = m.group(1) if m else "Missing"
        decisions[decision] += 1
        keys[row.get("key", "")] += 1

        rm = re.search(r"RAYYAN-EXCLUSION-REASONS: (.*?)(?: \| [A-Z][A-Z-]+:|$)", note)
        current_reasons = []
        if rm:
            current_reasons = [x.strip() for x in rm.group(1).split(";") if x.strip()]
            for reason in current_reasons:
                reasons[reason] += 1
            reason_combinations[tuple(current_reasons)] += 1

        if decision == "Missing":
            missing_decision.append({"key": row.get("key"), "title": row.get("title"), "notes": note})
        if decision == "Excluded" and not current_reasons:
            excluded_without_reason.append({"key": row.get("key"), "title": row.get("title"), "notes": note})
        if decision == "Included" and current_reasons:
            included_with_reason.append({"key": row.get("key"), "title": row.get("title"), "reasons": current_reasons})

    return {
        "file": str(path),
        "rows": len(rows),
        "fieldnames": list(rows[0].keys()) if rows else [],
        "decisions": dict(decisions),
        "exclusion_reason_mentions": dict(reasons),
        "reason_combinations": {"; ".join(k): v for k, v in reason_combinations.items()},
        "missing_decision": missing_decision,
        "excluded_without_reason": excluded_without_reason,
        "included_with_reason": included_with_reason,
        "duplicate_keys": [k for k, v in keys.items() if v > 1],
    }


def parse_log(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    key_counts = Counter(r["key"] for r in rows)
    articles = defaultdict(list)
    for row in rows:
        articles[row["article_id"]].append(row)
    return {
        "file": str(path),
        "rows": len(rows),
        "events_by_key": dict(key_counts),
        "distinct_articles": len(articles),
    }


result = {}
for folder in sorted(ROOT.iterdir()):
    if folder.is_dir():
        result[folder.name] = {
            "articles": parse_articles(folder / "articles.csv"),
            "log": parse_log(folder / "customizations_log.csv"),
        }

print(json.dumps(result, ensure_ascii=False, indent=2))
