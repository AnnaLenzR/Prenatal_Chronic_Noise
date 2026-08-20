from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from docx import Document


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "tmp" / "pcne_crosscheck"
DATA_PATH = ROOT / "Data" / "PCN_data_ext_checking_v.3.csv"


def norm(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())


def show(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.8g}"
    return str(value)


def close(a: object, b: object, abs_tol: float = 0.02, rel_tol: float = 0.005) -> bool:
    if pd.isna(a) or pd.isna(b):
        return False
    a = float(a)
    b = float(b)
    return abs(a - b) <= max(abs_tol, rel_tol * max(abs(a), abs(b), 1.0))


issues: list[dict] = []


def add_issue(
    *,
    severity: str,
    certainty: str,
    category: str,
    study_id: str = "",
    es_id: str = "",
    csv_row: object = "",
    field: str,
    current: object,
    expected: object,
    evidence: str,
    source_file: str,
    source_locator: str,
    recommendation: str,
) -> None:
    issues.append(
        {
            "issue_id": f"I{len(issues) + 1:04d}",
            "severity": severity,
            "certainty": certainty,
            "category": category,
            "study_id": study_id,
            "es_id": es_id,
            "csv_row": csv_row,
            "field": field,
            "current_value": show(current),
            "expected_or_review": show(expected),
            "evidence": evidence,
            "source_file": source_file,
            "source_locator": source_locator,
            "recommended_action": recommendation,
        }
    )


df = pd.read_csv(DATA_PATH)
df.insert(0, "csv_row", np.arange(2, len(df) + 2))

# Sheet/schema checks anchored in protocol Table 5.
if "Unnamed: 70" in df.columns and df["Unnamed: 70"].isna().all():
    add_issue(
        severity="Low",
        certainty="Confirmed",
        category="Schema",
        field="Unnamed: 70",
        current="entirely blank column",
        expected="remove in next version",
        evidence="The column has no values and is not an extraction item in Protocol Table 5.",
        source_file="protocol/PCNE_protocol_v.4_111425.docx",
        source_locator="Table 5",
        recommendation="Drop only in the corrected copy; retain the original CSV unchanged.",
    )

if "higher_better_notes.1" in df.columns:
    add_issue(
        severity="Medium",
        certainty="Confirmed",
        category="Schema",
        field="higher_better_notes / higher_better_notes.1",
        current="duplicate source header resolved by pandas suffix",
        expected="two uniquely named fields or one consolidated notes field",
        evidence="Protocol Table 5 defines one higher_better_notes field; the CSV contains two identically named source headers.",
        source_file="protocol/PCNE_protocol_v.4_111425.docx",
        source_locator="Table 5, item higher_better_notes",
        recommendation="Determine the meaning of the first duplicate (it appears to contain direction labels) and rename explicitly in the corrected copy.",
    )

allowed_gestation = {"early", "mid", "late", "early, mid", "mid, late", "early, late", "early, mid, late", "not reported", "unclear"}
allowed_exposure = {"Intermittent", "Continuous"}
allowed_outcomes = {"Anxiety", "Depression", "Both"}
allowed_timing = {"Light Phase", "Dark Phase", "Not Reported"}

for _, row in df.iterrows():
    sid = row["study_id"]
    common = {"study_id": sid, "es_id": row["es_id"], "csv_row": int(row["csv_row"])}
    if str(row["gest_stage_ex"]).lower() in allowed_gestation and str(row["gest_stage_ex"]) not in allowed_gestation:
        add_issue(
            **common,
            severity="Low",
            certainty="Confirmed",
            category="Coding",
            field="gest_stage_ex",
            current=row["gest_stage_ex"],
            expected=str(row["gest_stage_ex"]).lower(),
            evidence="Protocol coding categories are lower-case; case variation creates duplicate levels.",
            source_file="protocol/PCNE_protocol_v.4_111425.docx",
            source_locator="Table 5, item gest_stage_ex",
            recommendation="Standardize case in the corrected copy.",
        )
    if row["exposure_type"] not in allowed_exposure:
        expected = "Intermittent" if norm(row["exposure_type"]) == "intermitent" else "review"
        add_issue(
            **common,
            severity="Low",
            certainty="Confirmed" if expected != "review" else "Review",
            category="Coding",
            field="exposure_type",
            current=row["exposure_type"],
            expected=expected,
            evidence="Protocol permits Intermittent or Continuous.",
            source_file="protocol/PCNE_protocol_v.4_111425.docx",
            source_locator="Table 5, item exposure_type",
            recommendation="Standardize to the protocol spelling.",
        )
    if row["exposure_type"] == "Continuous" and not pd.isna(row["exposure_session_duration_h"]):
        add_issue(
            **common,
            severity="Low",
            certainty="Confirmed",
            category="Protocol conformity",
            field="exposure_session_duration_h",
            current=row["exposure_session_duration_h"],
            expected="blank (continuous exposure)",
            evidence="Protocol says to populate session duration only for intermittent exposure.",
            source_file="protocol/PCNE_protocol_v.4_111425.docx",
            source_locator="Table 5, item exposure_session_duration",
            recommendation="Move 24 h/day to notes if useful, or document a protocol deviation before retaining it.",
        )
    if row["outcome_type"] not in allowed_outcomes:
        expected = "Anxiety" if norm(row["outcome_type"]) == "axiety" else "review"
        add_issue(
            **common,
            severity="Medium",
            certainty="Confirmed" if expected != "review" else "Review",
            category="Coding",
            field="outcome_type",
            current=row["outcome_type"],
            expected=expected,
            evidence="Value is outside Protocol Table 5 categories Anxiety, Depression, or Both.",
            source_file="protocol/PCNE_protocol_v.4_111425.docx",
            source_locator="Table 5, item outcome_type",
            recommendation="Correct the category before analysis.",
        )
    if row["measurement_timing"] not in allowed_timing:
        expected = {"lightphase": "Light Phase", "darkphase": "Dark Phase", "notreported": "Not Reported"}.get(norm(row["measurement_timing"]), "review")
        add_issue(
            **common,
            severity="Low",
            certainty="Confirmed" if expected != "review" else "Review",
            category="Coding",
            field="measurement_timing",
            current=row["measurement_timing"],
            expected=expected,
            evidence="Case does not match the protocol's three allowed labels.",
            source_file="protocol/PCNE_protocol_v.4_111425.docx",
            source_locator="Table 5, item measurement_timing",
            recommendation="Standardize the label in the corrected copy.",
        )

# Study-level metadata structure.
for sid, group in df.groupby("study_id", sort=False):
    titles = group["title"].dropna().astype(str).unique().tolist()
    if len(titles) > 1:
        bad_rows = group[group["title"] != group["title"].mode().iloc[0]]
        for _, row in bad_rows.iterrows():
            add_issue(
                severity="High",
                certainty="Confirmed",
                category="Study metadata",
                study_id=sid,
                es_id=row["es_id"],
                csv_row=int(row["csv_row"]),
                field="title",
                current=row["title"],
                expected=group["title"].mode().iloc[0],
                evidence="A study_id should map to one publication title; this row contains a title from another included study.",
                source_file=f"included_studies/{sid}.pdf" if (ROOT / "included_studies" / f"{sid}.pdf").exists() else "included_studies/barzegar_2014_hippo.pdf",
                source_locator="PDF page 1",
                recommendation="Replace with the publication title used by the other rows for this study_id.",
            )
    doi_values = group["doi"].dropna().astype(str).str.strip().unique().tolist()
    for doi in doi_values:
        if doi and not doi.startswith("10."):
            for _, row in group[group["doi"].astype(str).str.strip().eq(doi)].iterrows():
                add_issue(
                    severity="Medium",
                    certainty="Confirmed",
                    category="Study metadata",
                    study_id=sid,
                    es_id=row["es_id"],
                    csv_row=int(row["csv_row"]),
                    field="doi",
                    current=doi,
                    expected="blank if no DOI; keep the article URL in a separate URL field",
                    evidence="Protocol specifies a short DOI beginning with 10.; the current value is a webpage URL.",
                    source_file="protocol/PCNE_protocol_v.4_111425.docx",
                    source_locator="Table 5, item doi",
                    recommendation="Do not treat the article landing-page URL as a DOI.",
                )

# Numeric relationships: SE must equal SD/sqrt(n) when all three are populated.
for _, row in df.iterrows():
    for arm in ("c", "ex"):
        sd, n, se = row[f"{arm}_sd"], row[f"{arm}_n"], row[f"{arm}_se"]
        if pd.isna(sd) or pd.isna(n) or pd.isna(se) or float(n) <= 0:
            continue
        expected = float(sd) / math.sqrt(float(n))
        if abs(float(se) - expected) > max(0.02, 0.02 * max(abs(expected), 1.0)):
            source = "included_studies/abramova_2020_genpath/abramova2020_descriptives.xlsx" if row["study_id"] == "abramova_2020_genpath" else "Metadigitise_figs/metaDigitise_output.csv"
            locator = "matching descriptive-statistics row" if row["study_id"] == "abramova_2020_genpath" else "matching figure/group row"
            add_issue(
                severity="High",
                certainty="Confirmed",
                category="Summary statistics",
                study_id=row["study_id"],
                es_id=row["es_id"],
                csv_row=int(row["csv_row"]),
                field=f"{arm}_se",
                current=se,
                expected=round(expected, 6),
                evidence=f"The stored SE is inconsistent with {arm}_sd / sqrt({arm}_n).",
                source_file=source,
                source_locator=locator,
                recommendation="Recalculate SE from the verified SD and n in the corrected copy; preserve the original value in an audit column.",
            )

# MetaDigitise reconciliation.
meta_path = ROOT / "Metadigitise_figs" / "metaDigitise_output.csv"
meta = pd.read_csv(meta_path)
meta["file_stem"] = meta["filename"].str.replace(r"\.png$", "", regex=True)
meta["norm_group"] = meta["group_id"].map(norm)
meta_recon: list[dict] = []

def meta_candidates(row: pd.Series, group_value: str) -> pd.DataFrame:
    sid_prefix = "_".join(str(row["study_id"]).split("_")[:2])
    candidates = meta[meta["filename"].str.lower().str.startswith(sid_prefix.lower())].copy()
    if not pd.isna(row["data_file"]):
        exact_file = candidates[candidates["file_stem"].map(norm).eq(norm(row["data_file"]))]
        if not exact_file.empty:
            candidates = exact_file
    exact = candidates[candidates["norm_group"].eq(norm(group_value))]
    if len(exact) == 1:
        return exact
    # Known harmless label variants between the extraction IDs and saved
    # MetaDigitise group labels.
    aliases = [str(group_value)]
    if row["study_id"] == "hassanvand_2012_phyphar":
        aliases.append(str(group_value).replace("Expn_", "Exp_"))
    if row["study_id"] == "barzegar_2014_hippo":
        aliases.append(str(group_value).split("_")[0])
        panel = "2a" if str(row["data_source"]).lower().endswith("a") else "2b"
        candidates = candidates[candidates["file_stem"].str.lower().str.contains(panel, regex=False)]
    for alias in aliases[1:]:
        hit = candidates[candidates["norm_group"].eq(norm(alias))]
        if len(hit) == 1:
            return hit
    # Group labels in the sheet sometimes append a metric suffix absent from MetaDigitise.
    parts = str(group_value).split("_")
    for cut in range(len(parts) - 1, 0, -1):
        short = norm("_".join(parts[:cut]))
        hit = candidates[candidates["norm_group"].eq(short)]
        if len(hit) == 1:
            return hit
    # Narrow repeated generic labels using the figure/panel in data_source.
    figure_token = norm(row["data_source"]).replace("figure", "fig")
    if figure_token:
        narrowed = candidates[candidates["file_stem"].map(norm).str.contains(figure_token, regex=False)]
        exact = narrowed[narrowed["norm_group"].eq(norm(group_value))]
        if len(exact) == 1:
            return exact
    return candidates.iloc[0:0]


for _, row in df.iterrows():
    if "figure" not in str(row["data_source"]).lower() and not str(row["data_source"]).lower().startswith("fig"):
        continue
    rec = {
        "study_id": row["study_id"],
        "es_id": row["es_id"],
        "csv_row": int(row["csv_row"]),
        "data_source": row["data_source"],
        "data_file": show(row["data_file"]),
        "control_group": row["c_a_id"],
        "experimental_group": row["ex_a_id"],
    }
    all_ok = True
    source_files = set()
    notes = []
    for arm, group_col in (("c", "c_a_id"), ("ex", "ex_a_id")):
        hit = meta_candidates(row, row[group_col])
        if len(hit) != 1:
            rec[f"{arm}_status"] = "unmatched"
            all_ok = False
            notes.append(f"{arm} group not uniquely matched")
            continue
        m = hit.iloc[0]
        source_files.add(m["filename"])
        comparisons = {
            "mean": close(row[f"{arm}_mean"], m["mean"]),
            "sd": close(row[f"{arm}_sd"], m["sd"]),
            "n": close(row[f"{arm}_n"], m["n"], abs_tol=0.001, rel_tol=0),
            "se": close(row[f"{arm}_se"], m["se"]),
        }
        rec[f"{arm}_status"] = "match" if all(comparisons.values()) else "mismatch"
        rec[f"{arm}_meta_group"] = m["group_id"]
        rec[f"{arm}_meta_file"] = m["filename"]
        rec[f"{arm}_mean_meta"] = m["mean"]
        rec[f"{arm}_sd_meta"] = m["sd"]
        rec[f"{arm}_n_meta"] = m["n"]
        rec[f"{arm}_se_meta"] = m["se"]
        if not all(comparisons.values()):
            all_ok = False
            bad = [key for key, value in comparisons.items() if not value]
            notes.append(f"{arm} differs in {', '.join(bad)}")
            # Abramova 2021 values come from the author workbook despite several
            # rows being labelled as figures. Whitlow SDs were explicitly
            # assumed as sqrt(mean), so neither is a direct MetaDigitise error.
            report_bad = [] if row["study_id"] in {"abramova_2021_front", "whitlow_1978_thesis"} else [x for x in bad if x != "se"]
            for stat in report_bad:
                add_issue(
                    severity="High" if stat in {"mean", "sd", "n"} else "Medium",
                    certainty="Confirmed",
                    category="MetaDigitise reconciliation",
                    study_id=row["study_id"],
                    es_id=row["es_id"],
                    csv_row=int(row["csv_row"]),
                    field=f"{arm}_{stat}",
                    current=row[f"{arm}_{stat}"],
                    expected=m[stat],
                    evidence=f"CSV value does not match MetaDigitise group {m['group_id']}.",
                    source_file="Metadigitise_figs/metaDigitise_output.csv",
                    source_locator=f"filename={m['filename']}; group_id={m['group_id']}",
                    recommendation="Reconcile against the saved digitization/calibration and update only the corrected dataset.",
                )
    rec["overall_status"] = "match" if all_ok else "review"
    rec["meta_files"] = "; ".join(sorted(source_files))
    rec["notes"] = "; ".join(notes)
    meta_recon.append(rec)

# File naming/existence checks for digitized figures.
available_stems = {p.stem.lower(): p.relative_to(ROOT).as_posix() for p in (ROOT / "Metadigitise_figs").glob("*.png")}
for _, row in df.iterrows():
    if "figure" not in str(row["data_source"]).lower() and not str(row["data_source"]).lower().startswith("fig"):
        continue
    current = str(row["data_file"]) if not pd.isna(row["data_file"]) else ""
    if current.lower() not in available_stems and row["study_id"] != "abramova_2021_front":
        # If MetaDigitise reconciliation found a unique file, recommend it.
        recon = next((r for r in meta_recon if r["es_id"] == row["es_id"]), None)
        expected = recon.get("meta_files", "review") if recon else "review"
        add_issue(
            severity="Medium",
            certainty="Confirmed",
            category="Source traceability",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="data_file",
            current=current,
            expected=expected or "review",
            evidence="No PNG in Metadigitise_figs has the current data_file stem.",
            source_file="Metadigitise_figs/",
            source_locator="file inventory",
            recommendation="Use the exact saved PNG stem so the extraction is reproducible.",
        )

# Abramova 2021: verify all extracted statistics against author raw data. The
# experimental arm matches offspring_sex, but the control arm is taken from the
# opposite-sex subgroup throughout the 14-row block.
raw2021_path = ROOT / "included_studies" / "abramova_2021_front" / "abramova_2021_front.xlsx"
raw2021 = pd.read_excel(raw2021_path, sheet_name="Лист1")
raw2021 = raw2021[raw2021["handling"].eq("No handling")].copy()
metric_map_2021 = {
    "Sections crossed": "squares",
    "Rearing frequency": "rearing",
    "Center entries (crossing)": "center_num",
    "Time in central square": "center_totalTime",
    "Grooming frequency": "grum_number",
    "Total grooming time": "grum_totalTime",
    "Total freezing time": "freez_totalTime",
}
raw_recon: list[dict] = []
for _, row in df[df["study_id"].eq("abramova_2021_front")].iterrows():
    metric = metric_map_2021[row["measurement_variable"]]
    source_stats = {}
    for arm, group in (("c", "Control"), ("ex", "PS")):
        best = None
        for sex_label, sex_value in (("Males", "male"), ("Females", "female")):
            values = pd.to_numeric(raw2021.loc[(raw2021["group"] == group) & (raw2021["sex"] == sex_label), metric], errors="coerce").dropna()
            stats = {"n": len(values), "mean": values.mean(), "sd": values.std(ddof=1), "se": values.std(ddof=1) / math.sqrt(len(values))}
            score = abs(float(row[f"{arm}_mean"]) - stats["mean"]) + abs(float(row[f"{arm}_n"]) - stats["n"]) * 5
            if best is None or score < best[0]:
                best = (score, sex_value, stats)
        source_stats[arm] = {"sex": best[1], **best[2]}
    expected_sex = str(row["offspring_sex"]).lower()
    expected_label = "Males" if expected_sex == "male" else "Females"
    expected_control_values = pd.to_numeric(
        raw2021.loc[(raw2021["group"] == "Control") & (raw2021["sex"] == expected_label), metric], errors="coerce"
    ).dropna()
    expected_control = {
        "n": len(expected_control_values),
        "mean": expected_control_values.mean(),
        "sd": expected_control_values.std(ddof=1),
        "se": expected_control_values.std(ddof=1) / math.sqrt(len(expected_control_values)),
    }
    experimental_match = all(
        close(row[f"ex_{stat}"], source_stats["ex"][stat], abs_tol=0.02, rel_tol=0.002)
        for stat in ("mean", "sd", "n", "se")
    )
    control_same_sex_match = all(
        close(row[f"c_{stat}"], expected_control[stat], abs_tol=0.02, rel_tol=0.002)
        for stat in ("mean", "sd", "n", "se")
    )
    raw_recon.append(
        {
            "study_id": row["study_id"],
            "es_id": row["es_id"],
            "csv_row": int(row["csv_row"]),
            "source_file": raw2021_path.relative_to(ROOT).as_posix(),
            "source_locator": f"Лист1; handling=No handling; metric={metric}",
            "current_offspring_sex": row["offspring_sex"],
            "source_offspring_sex": source_stats["ex"]["sex"],
            "control_source_sex": source_stats["c"]["sex"],
            "experimental_source_sex": source_stats["ex"]["sex"],
            "statistics_status": "match" if control_same_sex_match and experimental_match else "mixed-sex control",
            "notes": "Experimental statistics match offspring_sex; control statistics match the opposite-sex author subgroup.",
        }
    )
    if source_stats["c"]["sex"] != expected_sex and source_stats["ex"]["sex"] == expected_sex:
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Author raw-data reconciliation",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="c_mean; c_sd; c_n; c_se",
            current=f"mean={show(row['c_mean'])}; sd={show(row['c_sd'])}; n={show(row['c_n'])}; se={show(row['c_se'])}",
            expected=f"mean={show(expected_control['mean'])}; sd={show(expected_control['sd'])}; n={show(expected_control['n'])}; se={show(expected_control['se'])}",
            evidence=f"Control summaries match author raw-data sex={source_stats['c']['sex']}, whereas offspring_sex and the experimental arm are sex={expected_sex}.",
            source_file=raw2021_path.relative_to(ROOT).as_posix(),
            source_locator=f"Лист1; No handling; metric={metric}; Control {expected_label}",
            recommendation="Replace the four control statistics with the same-sex Control subgroup and retain offspring_sex/experimental statistics.",
        )
    if str(row["data_source"]).lower().startswith("figure"):
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Source traceability",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="data_source",
            current=row["data_source"],
            expected="Author raw data",
            evidence="The CSV statistics exactly reproduce the author raw-data subgroup, not the MetaDigitise values for the cited figure.",
            source_file=raw2021_path.relative_to(ROOT).as_posix(),
            source_locator=f"Лист1; No handling; {metric}",
            recommendation="Change the source field and retain the figure only as a secondary publication reference.",
        )
    add_issue(
        severity="Medium",
        certainty="Confirmed",
        category="Source traceability",
        study_id=row["study_id"],
        es_id=row["es_id"],
        csv_row=int(row["csv_row"]),
        field="data_file",
        current=row["data_file"],
        expected=raw2021_path.relative_to(ROOT).as_posix(),
        evidence="The current value is not a file in the study folder; the statistics are reproducible from the author workbook.",
        source_file=raw2021_path.relative_to(ROOT).as_posix(),
        source_locator="Лист1",
        recommendation="Use the exact author workbook filename/path in the corrected copy.",
    )

# Whitlow figure error bars were not used because their meaning was not reported;
# the sheet instead assumes SD=sqrt(mean). This is a transparent assumption to
# review, not a direct MetaDigitise transcription mismatch.
for _, row in df[df["study_id"].eq("whitlow_1978_thesis")].iterrows():
    add_issue(
        severity="Medium",
        certainty="Review",
        category="Statistical assumption",
        study_id=row["study_id"],
        es_id=row["es_id"],
        csv_row=int(row["csv_row"]),
        field="c_sd; ex_sd",
        current=f"{show(row['c_sd'])}; {show(row['ex_sd'])}",
        expected="decision required",
        evidence="stat_comment states SD was imputed as sqrt(mean); the figure error-bar meaning is not reported.",
        source_file="included_studies/whitlow_1978_thesis.pdf",
        source_locator=f"{row['data_source']} and Metadigitise_figs/{row['data_file']}.png",
        recommendation="Pre-specify whether to retain this variance assumption, derive an alternative, or include these effects only in sensitivity analysis.",
    )

# Abramova 2020: means, SDs and n can be reconciled to the author's
# descriptive-statistics workbook. The SE discrepancies are separately listed
# by the SD/sqrt(n) check above.
desc2020_path = ROOT / "included_studies" / "abramova_2020_genpath" / "abramova2020_descriptives.xlsx"
desc2020 = pd.read_excel(desc2020_path, sheet_name="tidy_all")
for _, row in df[df["study_id"].eq("abramova_2020_genpath")].iterrows():
    arm_notes = []
    all_core_match = True
    se_match = True
    locators = []
    for arm in ("c", "ex"):
        candidates = desc2020[
            desc2020["n"].eq(row[f"{arm}_n"])
            & desc2020["mean"].map(lambda x: close(x, row[f"{arm}_mean"], abs_tol=0.02, rel_tol=0.002))
            & desc2020["sd"].map(lambda x: close(x, row[f"{arm}_sd"], abs_tol=0.02, rel_tol=0.002))
        ]
        if candidates.empty:
            all_core_match = False
            arm_notes.append(f"{arm}: mean/SD/n not uniquely located")
            continue
        source_row = candidates.iloc[0]
        locators.append(f"{arm}=tidy_all row {int(candidates.index[0]) + 2}")
        this_se_match = close(row[f"{arm}_se"], source_row["se"], abs_tol=0.02, rel_tol=0.002)
        se_match = se_match and this_se_match
        arm_notes.append(f"{arm}: mean/SD/n match; SE {'matches' if this_se_match else 'differs'}")
    raw_recon.append(
        {
            "study_id": row["study_id"],
            "es_id": row["es_id"],
            "csv_row": int(row["csv_row"]),
            "source_file": desc2020_path.relative_to(ROOT).as_posix(),
            "source_locator": "; ".join(locators),
            "current_offspring_sex": row["offspring_sex"],
            "source_offspring_sex": "not evaluated by this numeric match",
            "control_source_sex": "",
            "experimental_source_sex": "",
            "statistics_status": "match" if all_core_match and se_match else ("SE mismatch" if all_core_match else "review"),
            "notes": "; ".join(arm_notes),
        }
    )

row_es162 = df[df["es_id"].eq("es162")].iloc[0]
source_es162 = desc2020[
    desc2020["sheet"].eq("sucrose")
    & desc2020["group_code"].eq("US")
    & desc2020["sex"].eq("m")
    & desc2020["variable"].eq("Индекс")
].iloc[0]
if not close(row_es162["ex_sd"], source_es162["sd"], abs_tol=0.02, rel_tol=0.002):
    add_issue(
        severity="High",
        certainty="Confirmed",
        category="Author raw-data reconciliation",
        study_id=row_es162["study_id"],
        es_id=row_es162["es_id"],
        csv_row=int(row_es162["csv_row"]),
        field="ex_sd",
        current=row_es162["ex_sd"],
        expected=source_es162["sd"],
        evidence="The experimental mean and n identify the US male sucrose-index row, but the stored SD differs from the author-data descriptive statistic.",
        source_file=desc2020_path.relative_to(ROOT).as_posix(),
        source_locator=f"tidy_all row {int(source_es162.name) + 2}; sheet=sucrose; group_code=US; sex=m; variable=Индекс",
        recommendation="Replace ex_sd with the source descriptive SD and recalculate ex_se.",
    )

# Abramova 2023: reconcile row order to the prepared Table 1 extraction, excluding social-interaction rows not in this review.
calc2023_path = ROOT / "included_studies" / "abramova_2023_biopsy" / "abramova_2023_biopsy_data_calculations.xlsx"
calc2023 = pd.read_excel(calc2023_path, sheet_name="Table1_Extract")
calc2023 = calc2023[~calc2023["Test"].eq("Social interaction")].reset_index(drop=True)
csv2023 = df[df["study_id"].eq("abramova_2023_biopsy")].reset_index(drop=True)
for i, row in csv2023.iterrows():
    src = calc2023.iloc[i]
    expected_sex = str(src["Sex"]).lower()
    if str(src["Reported in paper"]).startswith("Median"):
        stat_map = {
            "c_n": "offspring_c_n (control n)",
            "ex_n": "offspring_ex_n (PS n)",
            "c_median": "c_median",
            "c_q1": "c_q1",
            "c_q3": "c_q3",
            "ex_median": "ex_median",
            "ex_q1": "ex_q1",
            "ex_q3": "ex_q3",
        }
    else:
        stat_map = {
            "c_mean": "c_mean (control mean)",
            "c_sd": "c_sd (control sd formula)",
            "c_n": "offspring_c_n (control n)",
            "c_se": "c_se (control se)",
            "ex_mean": "ex_mean (PS mean)",
            "ex_sd": "ex_sd (PS sd formula)",
            "ex_n": "offspring_ex_n (PS n)",
            "ex_se": "ex_se (PS se)",
        }
    stats_match = all(close(row[col], src[src_col], abs_tol=0.02, rel_tol=0.002) for col, src_col in stat_map.items())
    raw_recon.append(
        {
            "study_id": row["study_id"],
            "es_id": row["es_id"],
            "csv_row": int(row["csv_row"]),
            "source_file": calc2023_path.relative_to(ROOT).as_posix(),
            "source_locator": f"Table1_Extract row {i + 2}; {src['Test']}; {src['Metric']}; {src['Sex']}",
            "current_offspring_sex": row["offspring_sex"],
            "source_offspring_sex": expected_sex,
            "statistics_status": "match" if stats_match else "review",
            "notes": "Statistics match the prepared table extraction." if stats_match else "One or more statistics differ.",
        }
    )
    if row["offspring_sex"] != expected_sex:
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Author/table reconciliation",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="offspring_sex",
            current=row["offspring_sex"],
            expected=expected_sex,
            evidence="Sex does not match the corresponding Table1_Extract row.",
            source_file=calc2023_path.relative_to(ROOT).as_posix(),
            source_locator=f"Table1_Extract row {i + 2}",
            recommendation="Correct sex and all sex-coded arm/comparison IDs together.",
        )
    expected_token = "m" if expected_sex == "male" else "f"
    for field in ("c_a_id", "ex_a_id", "comparison"):
        tokens = [x for x in str(row[field]).lower().split("_") if x in {"m", "f"}]
        if tokens and expected_token not in tokens:
            add_issue(
                severity="High",
                certainty="Confirmed",
                category="Identifier integrity",
                study_id=row["study_id"],
                es_id=row["es_id"],
                csv_row=int(row["csv_row"]),
                field=field,
                current=row[field],
                expected=f"ID containing _{expected_token}_",
                evidence="Sex token in arm ID conflicts with offspring_sex and the matched source row.",
                source_file=calc2023_path.relative_to(ROOT).as_posix(),
                source_locator=f"Table1_Extract row {i + 2}",
                recommendation="Rebuild the arm and comparison IDs from the corrected sex/group labels.",
            )
    expected_unit = "" if pd.isna(src["Unit"]) else str(src["Unit"])
    if expected_unit and norm(row["data_units"]) != norm(expected_unit):
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Outcome metadata",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="data_units",
            current=row["data_units"],
            expected=expected_unit,
            evidence="Unit conflicts with the Table 1 extraction.",
            source_file=calc2023_path.relative_to(ROOT).as_posix(),
            source_locator=f"Table1_Extract row {i + 2}; Metric={src['Metric']}",
            recommendation="Correct unit and data_type together.",
        )
    expected_type = "Time" if expected_unit == "s" else ("Count" if expected_unit == "count" else None)
    if expected_type and norm(row["data_type"]) != norm(expected_type):
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Outcome metadata",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="data_type",
            current=row["data_type"],
            expected=expected_type,
            evidence="Data type conflicts with the unit and metric in the Table 1 extraction.",
            source_file=calc2023_path.relative_to(ROOT).as_posix(),
            source_locator=f"Table1_Extract row {i + 2}; Metric={src['Metric']}",
            recommendation="Correct data_type and data_units together.",
        )
    add_issue(
        severity="Medium",
        certainty="Confirmed",
        category="Source traceability",
        study_id=row["study_id"],
        es_id=row["es_id"],
        csv_row=int(row["csv_row"]),
        field="data_file",
        current=row["data_file"],
        expected=calc2023_path.relative_to(ROOT).as_posix(),
        evidence="The referenced workbook name does not exist; this is the available calculation/source workbook used for reconciliation.",
        source_file=calc2023_path.relative_to(ROOT).as_posix(),
        source_locator="Table1_Extract",
        recommendation="Use the exact filename/path in the corrected copy.",
    )

# Direct publication-based confirmed corrections.
for _, row in df[df["study_id"].eq("arjunan_2023_stress")].iterrows():
    if row["noise_type"] == "Ultrasound":
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Exposure metadata",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="noise_type",
            current=row["noise_type"],
            expected="White noise / broadband audible noise",
            evidence="Methods specify a white-noise generator emitting 0-20 kHz; this is not ultrasound-only exposure.",
            source_file="included_studies/arjunan_2023_stress.pdf",
            source_locator="PDF page 8, section 4.3 Noise Exposure",
            recommendation="Correct the exposure category and re-evaluate any derived acoustic-band moderator.",
        )
    if norm(row["frequency_Hz"]) == norm("0-2,000"):
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Exposure metadata",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="frequency_Hz",
            current=row["frequency_Hz"],
            expected="0-20,000",
            evidence="Methods report all frequencies in the 0-20 kHz range; the extraction is missing one zero in the upper bound.",
            source_file="included_studies/arjunan_2023_stress.pdf",
            source_locator="PDF page 8, section 4.3 Noise Exposure",
            recommendation="Correct the frequency range before acoustic-band derivation.",
        )

# Uygur 2010: the methods state 45 minutes/day (0.75 h), and Table II
# reports PSN n=9 and CON n=10. The extracted n values are reversed.
for _, row in df[df["study_id"].eq("uygur_2010_aphyhun")].iterrows():
    if close(row["exposure_session_duration_h"], 0.66, abs_tol=0.001, rel_tol=0):
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Exposure metadata",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="exposure_session_duration_h",
            current=row["exposure_session_duration_h"],
            expected=0.75,
            evidence="Methods report 45 min/day; 45/60 = 0.75 h.",
            source_file="included_studies/uygur_2010_aphyhun.pdf",
            source_locator="PDF page 3, Stress procedures",
            recommendation="Correct the daily exposure duration.",
        )
    if int(row["c_n"]) == 9 and int(row["ex_n"]) == 10:
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Sample size",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="c_n; ex_n",
            current=f"{int(row['c_n'])}; {int(row['ex_n'])}",
            expected="10; 9",
            evidence="Table II labels CON n=10 and PSN n=9; the means/SEs in this row correspond to CON and PSN respectively.",
            source_file="included_studies/uygur_2010_aphyhun.pdf",
            source_locator="PDF page 5, Table II",
            recommendation="Swap the control and experimental sample sizes; retain the arm means and SEs.",
        )

# Uygur 2011 describes total time in each forced-swim behavior. Diving and
# jumping rows are currently typed as counts.
for _, row in df[
    df["study_id"].eq("uygur_2011_ankarauniv")
    & df["measurement_variable"].isin(["Total diving time", "Total jumping time"])
].iterrows():
    add_issue(
        severity="High",
        certainty="Confirmed",
        category="Outcome metadata",
        study_id=row["study_id"],
        es_id=row["es_id"],
        csv_row=int(row["csv_row"]),
        field="data_type; data_units",
        current=f"{row['data_type']}; {row['data_units']}",
        expected="Time; s",
        evidence="Methods state that total time spent immobile, swimming, jumping, and diving was calculated for the test period.",
        source_file="included_studies/uygur_2011_ankarauniv.pdf",
        source_locator="PDF page 3, Forced swimming test; PDF page 4, Table 2",
        recommendation="Correct both data type and unit before outcome harmonization.",
    )

# Abramova 2024 Figure 3b/3c screenshot filenames are transposed for the
# rearing and squares-crossed outcomes.
for es_id, expected_file in {
    "es033": "abramova_2024_devneur_fig3c",
    "es034": "abramova_2024_devneur_fig3c",
    "es035": "abramova_2024_devneur_fig3b",
    "es036": "abramova_2024_devneur_fig3b",
}.items():
    row = df[df["es_id"].eq(es_id)].iloc[0]
    if row["data_file"] != expected_file:
        add_issue(
            severity="High",
            certainty="Confirmed",
            category="Source traceability",
            study_id=row["study_id"],
            es_id=row["es_id"],
            csv_row=int(row["csv_row"]),
            field="data_file",
            current=row["data_file"],
            expected=expected_file,
            evidence="The current screenshot stem points to the other Figure 3 panel; the MetaDigitise file and group labels identify the correct panel.",
            source_file="Metadigitise_figs/metaDigitise_output.csv",
            source_locator=f"filename={expected_file}.png",
            recommendation="Correct the screenshot filename without changing the already matching extracted statistics.",
        )

# Cross-fostering is not a sham surgical/pharmacological intervention under the protocol definition.
for _, row in df[df["experimental_procedures"].astype(str).str.lower().eq("cross-fostered")].iterrows():
    add_issue(
        severity="Medium",
        certainty="Confirmed",
        category="Protocol conformity",
        study_id=row["study_id"],
        es_id=row["es_id"],
        csv_row=int(row["csv_row"]),
        field="experimental_procedures",
        current=row["experimental_procedures"],
        expected="None; document cross-fostering in experimental_procedures_notes or a dedicated design field",
        evidence="Protocol defines this field only for sham surgical or pharmacological interventions.",
        source_file="protocol/PCNE_protocol_v.4_111425.docx",
        source_locator="Table 5, item experimental_procedures",
        recommendation="Preserve cross-fostering information, but move it to an appropriate notes/design variable.",
    )

# Rows sourced only from an author email but lacking a saved raw-data file cannot be independently reproduced from the workspace.
for _, row in df[df["data_source"].astype(str).str.lower().str.contains("author") & df["data_file"].isna()].iterrows():
    add_issue(
        severity="High",
        certainty="Review",
        category="Source availability",
        study_id=row["study_id"],
        es_id=row["es_id"],
        csv_row=int(row["csv_row"]),
        field="data_file",
        current="blank",
        expected="saved author-supplied file/email attachment with a stable filename",
        evidence="The numerical source is described as an author email, but no supporting file is present in the study folder.",
        source_file="included_studies/",
        source_locator="workspace inventory",
        recommendation="Add the author-supplied source file (or a dated correspondence note) before treating the values as independently verified.",
    )

# Protocol dictionary extraction for the report.
doc = Document(ROOT / "protocol" / "PCNE_protocol_v.4_111425.docx")
protocol_rows = []
for table in doc.tables:
    if len(table.rows) < 2 or len(table.columns) < 2:
        continue
    headers = [c.text.strip() for c in table.rows[0].cells]
    if headers[:2] == ["Items", "Descriptions"]:
        for row in table.rows[1:]:
            item = row.cells[0].text.strip()
            desc = row.cells[1].text.strip()
            if item and item not in {"Study information", "Population", "Dam", "Offspring"}:
                protocol_rows.append({"protocol_item": item, "description": desc})
        break

# Coverage summary.
pdf_manifest = json.loads((OUT / "source_manifest.json").read_text(encoding="utf-8"))["pdfs"]
pdf_by_study = defaultdict(list)
for item in pdf_manifest:
    name = Path(item["source_file"]).name
    for sid in df["study_id"].unique():
        if name.startswith(sid) or sid in item["source_file"] or (sid == "pavlov_2023_molsci" and "pavlov_2023" in item["source_file"]):
            pdf_by_study[sid].append(item["source_file"])
coverage = []
issue_frame = pd.DataFrame(issues)
for sid, group in df.groupby("study_id", sort=False):
    study_issues = issue_frame[issue_frame["study_id"].eq(sid)] if not issue_frame.empty else pd.DataFrame()
    coverage.append(
        {
            "study_id": sid,
            "extracted_rows": len(group),
            "source_pdf": "; ".join(pdf_by_study.get(sid, [])),
            "author_data_files": "; ".join(sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "included_studies").rglob("*.xlsx") if sid in p.as_posix())),
            "metadigitise_effect_sizes": sum(1 for r in meta_recon if r["study_id"] == sid),
            "confirmed_issues": int((study_issues["certainty"] == "Confirmed").sum()) if not study_issues.empty else 0,
            "review_items": int((study_issues["certainty"] == "Review").sum()) if not study_issues.empty else 0,
            "audit_scope": "protocol/schema + internal statistics + PDF methods + available figure/raw-data reconciliation",
        }
    )

issue_frame = pd.DataFrame(issues)
issue_frame.to_csv(OUT / "issues.csv", index=False)
issue_frame[(issue_frame["severity"] == "High") | (issue_frame["certainty"] == "Review")].to_csv(
    OUT / "priority_issues.csv", index=False
)
issue_frame.groupby(["category", "severity", "certainty"], dropna=False).size().reset_index(name="cell_level_flags").sort_values(
    ["severity", "cell_level_flags"], ascending=[True, False]
).to_csv(OUT / "issue_summary.csv", index=False)
pd.DataFrame(meta_recon).to_csv(OUT / "metadigitise_reconciliation.csv", index=False)
pd.DataFrame(raw_recon).to_csv(OUT / "raw_data_reconciliation.csv", index=False)
pd.DataFrame(coverage).to_csv(OUT / "study_coverage.csv", index=False)
pd.DataFrame(protocol_rows).to_csv(OUT / "protocol_dictionary.csv", index=False)

summary = {
    "source_csv": DATA_PATH.relative_to(ROOT).as_posix(),
    "source_rows": len(df),
    "source_columns": len(df.columns) - 1,
    "issues_total": len(issue_frame),
    "confirmed": int((issue_frame["certainty"] == "Confirmed").sum()),
    "review": int((issue_frame["certainty"] == "Review").sum()),
    "by_severity": issue_frame["severity"].value_counts().to_dict(),
    "by_category": issue_frame["category"].value_counts().to_dict(),
    "studies": int(df["study_id"].nunique()),
    "metadigitise_rows_checked": len(meta_recon),
    "raw_data_rows_checked": len(raw_recon),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
