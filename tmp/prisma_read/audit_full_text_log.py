import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


FOLDER = Path("/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise/PCN_screening/full_text_2026-08-28_23-47-26")

with (FOLDER / "articles.csv").open(encoding="utf-8-sig", newline="") as fh:
    articles = list(csv.DictReader(fh))

with (FOLDER / "customizations_log.csv").open(encoding="utf-8-sig", newline="") as fh:
    events = list(csv.DictReader(fh))

article_by_id = {row["key"].removeprefix("rayyan-"): row for row in articles}

latest = {}
for event in events:
    latest[(event["article_id"], event["key"])] = event

active_reasons = defaultdict(list)
for (article_id, key), event in latest.items():
    if "__EXR__" in key and event["value"] == "1":
        reason = key.replace('"', "").replace("__EXR__", "").strip()
        active_reasons[article_id].append(reason)

records = []
for article_id, row in sorted(article_by_id.items(), key=lambda x: int(x[0])):
    note = row.get("notes", "") or ""
    dm = re.search(r'RAYYAN-INCLUSION: \{"Anna"=>"([^"]+)"\}', note)
    decision = dm.group(1) if dm else "Missing"
    rm = re.search(r"RAYYAN-EXCLUSION-REASONS: (.*?)(?: \| [A-Z][A-Z-]+:|$)", note)
    exported_reasons = []
    if rm:
        exported_reasons = [x.strip() for x in rm.group(1).split(",") if x.strip()]
    um = re.search(r'USER-NOTES: \{"Anna"=>\[(.*?)\]\}', note)
    user_notes = um.group(1) if um else ""
    records.append({
        "article_id": article_id,
        "decision": decision,
        "exported_reasons": exported_reasons,
        "active_log_reasons": sorted(active_reasons.get(article_id, [])),
        "title": row.get("title", ""),
        "user_notes": user_notes,
    })

summary = {
    "decisions": dict(Counter(r["decision"] for r in records)),
    "active_reason_mentions_excluded": dict(Counter(reason for r in records if r["decision"] == "Excluded" for reason in r["active_log_reasons"])),
    "exported_reason_mentions_excluded": dict(Counter(reason for r in records if r["decision"] == "Excluded" for reason in r["exported_reasons"])),
    "excluded_without_exported_reason": [r for r in records if r["decision"] == "Excluded" and not r["exported_reasons"]],
    "excluded_without_active_log_reason": [r for r in records if r["decision"] == "Excluded" and not r["active_log_reasons"]],
    "included_with_exported_reason": [r for r in records if r["decision"] == "Included" and r["exported_reasons"]],
    "included_with_active_log_reason": [r for r in records if r["decision"] == "Included" and r["active_log_reasons"]],
    "export_log_disagreements": [r for r in records if sorted(r["exported_reasons"]) != r["active_log_reasons"]],
    "all_records": records,
}

print(json.dumps(summary, ensure_ascii=False, indent=2))
