import csv
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path("/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise")
TA = ROOT / "PCN_screening/title_abstract_2026-08-28_23-45-55/articles.csv"
FT = ROOT / "PCN_screening/full_text_2026-08-28_23-47-26/articles.csv"
DATA = ROOT / "Data/PCN_data_ext_checking_v.3.csv"

SOURCE_COUNTS = {
    "Scopus": 1404,
    "Web of Science": 1842,
    "PubMed": 1056,
    "PsycINFO": 408,
    "OpenAlex": 681,
    "Google Scholar": 489,
    "BASE": 9,
}

MISSING_REASON_MAP = {
    "386282729": "Wrong exposure",
    "386283068": "Wrong population",
    "386283297": "Wrong exposure",
    "386283305": "Foreign language",
    "386283326": "Wrong exposure",
    "386283372": "Wrong exposure",
}

REASON_LABELS = {
    "wrong exposure": "Wrong exposure",
    "wrong outcome": "Wrong outcome",
    "wrong publication type": "Wrong publication type",
    "wrong population": "Wrong population",
}


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def decision(row):
    match = re.search(r'RAYYAN-INCLUSION: \{"Anna"=>"([^"]+)"\}', row.get("notes", "") or "")
    return match.group(1) if match else "Missing"


def reasons(row):
    match = re.search(r"RAYYAN-EXCLUSION-REASONS: (.*?)(?: \| [A-Z][A-Z-]+:|$)", row.get("notes", "") or "")
    return [] if not match else [part.strip().lower() for part in match.group(1).split(",") if part.strip()]


def normalized(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


ta_rows = rows(TA)
ft_rows = rows(FT)
ta_decisions = Counter(decision(row) for row in ta_rows)
ft_decisions = Counter(decision(row) for row in ft_rows)
ta_included = {row["key"] for row in ta_rows if decision(row) == "Included"}
ft_keys = {row["key"] for row in ft_rows}

primary_reasons = Counter()
for row in ft_rows:
    if decision(row) != "Excluded":
        continue
    article_id = row["key"].removeprefix("rayyan-")
    labels = reasons(row)
    if "full text not available" in labels:
        primary = "Full text not available"
    elif "foreign language" in labels:
        primary = "Foreign language"
    elif labels:
        primary = REASON_LABELS[labels[0]]
    else:
        primary = MISSING_REASON_MAP[article_id]
    primary_reasons[primary] += 1

data_rows = rows(DATA)
studies = {}
for row in data_rows:
    studies.setdefault(row["study_id"], row)

included_ft = [row for row in ft_rows if decision(row) == "Included"]
matched_studies = set()
matches = []
for report in included_ft:
    report_title = normalized(report["title"].split("     SO  - ")[0])
    scores = []
    for study_id, study in studies.items():
        score = SequenceMatcher(None, report_title, normalized(study["title"])).ratio()
        scores.append((score, study_id))
    score, study_id = max(scores)
    if score < 0.60:
        raise AssertionError((report["key"], study_id, score))
    matched_studies.add(study_id)
    matches.append({"rayyan_id": report["key"], "study_id": study_id, "title_score": round(score, 3)})

other_studies = sorted(set(studies) - matched_studies)

audit = {
    "source_total": sum(SOURCE_COUNTS.values()),
    "duplicates_removed": sum(SOURCE_COUNTS.values()) - len(ta_rows),
    "title_abstract": {"rows": len(ta_rows), "decisions": dict(ta_decisions)},
    "full_text": {"rows": len(ft_rows), "decisions": dict(ft_decisions)},
    "title_abstract_included_equals_full_text_records": ta_included == ft_keys,
    "full_text_primary_exclusion_reasons": dict(primary_reasons),
    "final_dataset_unique_studies": len(studies),
    "rayyan_included_matches": matches,
    "other_source_study_ids": other_studies,
}

assert audit["source_total"] == 5889
assert audit["duplicates_removed"] == 3576
assert ta_decisions == Counter({"Excluded": 2226, "Included": 87})
assert ft_decisions == Counter({"Excluded": 75, "Included": 12})
assert ta_included == ft_keys
assert primary_reasons == Counter({
    "Wrong exposure": 60,
    "Wrong outcome": 4,
    "Wrong publication type": 4,
    "Wrong population": 4,
    "Foreign language": 2,
    "Full text not available": 1,
})
assert len(studies) == 16
assert len(matched_studies) == 12
assert other_studies == [
    "abramova_2021_front",
    "abramova_2023_biopsy",
    "arjunan_2023_stress",
    "oliveira_2015_jbehavbraisci",
]

print(json.dumps(audit, indent=2, ensure_ascii=False))
