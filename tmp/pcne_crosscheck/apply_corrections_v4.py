from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path("/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise")
SOURCE = ROOT / "Data/PCN_data_ext_checking_v.3.csv"
OUT = ROOT / "Data/PCN_data_ext_checking_v.4_crosschecked.csv"
AUDIT_DIR = ROOT / "Data/audits"
CORRECTION_LOG = AUDIT_DIR / "correction_log_v4.csv"
ROW_STATUS = AUDIT_DIR / "row_review_status_v4.csv"
DECISION_REGISTER = AUDIT_DIR / "decision_register_v4.csv"
WRANGLING_PLAN = AUDIT_DIR / "data_wrangling_plan_v4.csv"
SUMMARY_JSON = ROOT / "tmp/pcne_crosscheck/v4_summary.json"

EXPECTED_SHA256 = "0bd770a4f117ead932c53b282c823a312a1526170c49f83623c8a7bb9b59a0fc"

STATUS_VERIFIED = "Verified – no change"
STATUS_TRANSCRIPTION = "Corrected transcription"
STATUS_DERIVED = "Corrected derived value"
STATUS_DECISION = "Analysis decision required"
STATUS_SOURCE = "Source needed"


def norm(value):
    if pd.isna(value):
        return ""
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.10g}"
    return str(value)


def same(a, b, tol=1e-9):
    if pd.isna(a) and pd.isna(b):
        return True
    try:
        return math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)
    except (TypeError, ValueError):
        return norm(a) == norm(b)


source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
if source_hash != EXPECTED_SHA256:
    raise RuntimeError(f"Source CSV hash changed: {source_hash}")

df = pd.read_csv(SOURCE)
if len(df) != 207:
    raise RuntimeError(f"Expected 207 source rows, found {len(df)}")

df.insert(0, "source_csv_row", np.arange(2, len(df) + 2))
df["c_se_reported"] = np.nan
df["c_se_analysis"] = np.nan
df["c_se_derivation"] = ""
df["c_se_source"] = ""
df["ex_se_reported"] = np.nan
df["ex_se_analysis"] = np.nan
df["ex_se_derivation"] = ""
df["ex_se_source"] = ""
df["crosscheck_status"] = STATUS_VERIFIED
df["crosscheck_package"] = ""
df["crosscheck_notes"] = ""

corrections: list[dict] = []
decisions: list[dict] = []
row_flags: dict[str, set[str]] = {es: set() for es in df["es_id"]}
row_packages: dict[str, set[str]] = {es: set() for es in df["es_id"]}
row_notes: dict[str, list[str]] = {es: [] for es in df["es_id"]}


def row_index(es_id: str) -> int:
    idx = df.index[df["es_id"].eq(es_id)].tolist()
    if len(idx) != 1:
        raise RuntimeError(f"Expected one row for {es_id}; found {len(idx)}")
    return idx[0]


def mark(es_id: str, status: str, package: str, note: str | None = None):
    row_flags[es_id].add(status)
    if package:
        row_packages[es_id].add(package)
    if note and note not in row_notes[es_id]:
        row_notes[es_id].append(note)


def change(es_id: str, field: str, new_value, status: str, package: str, source: str, rationale: str):
    idx = row_index(es_id)
    old_value = df.at[idx, field]
    if same(old_value, new_value):
        return
    df.at[idx, field] = new_value
    corrections.append(
        {
            "package": package,
            "study_id": df.at[idx, "study_id"],
            "es_id": es_id,
            "source_csv_row": int(df.at[idx, "source_csv_row"]),
            "field": field,
            "old_value_v3": norm(old_value),
            "new_value_v4": norm(new_value),
            "status": status,
            "source": source,
            "rationale": rationale,
        }
    )
    mark(es_id, status, package, rationale)


def add_decision(es_id: str, package: str, decision: str, current_treatment: str, options: str, source: str):
    idx = row_index(es_id)
    decisions.append(
        {
            "package": package,
            "study_id": df.at[idx, "study_id"],
            "es_id": es_id,
            "source_csv_row": int(df.at[idx, "source_csv_row"]),
            "status": STATUS_DECISION,
            "decision": decision,
            "current_treatment": current_treatment,
            "options": options,
            "source": source,
        }
    )
    mark(es_id, STATUS_DECISION, package, decision)


def set_se(idx: int, arm: str, reported, analysis, derivation: str, source: str):
    df.at[idx, f"{arm}_se_reported"] = reported
    df.at[idx, f"{arm}_se_analysis"] = analysis
    df.at[idx, f"{arm}_se_derivation"] = derivation
    df.at[idx, f"{arm}_se_source"] = source


def generic_source(row: pd.Series) -> str:
    data_file = norm(row.get("data_file"))
    data_source = norm(row.get("data_source"))
    if data_file:
        return f"{data_file}; {data_source}" if data_source else data_file
    return data_source or "Source recorded in v3 extraction"


# Package 1: Uygur 2011 — diving and jumping are durations.
p1 = "1 – Uygur 2011 outcome units"
p1_source = "included_studies/uygur_2011_ankarauniv.pdf, Methods and Table 2"
for es_id in ["es068", "es069", "es070", "es071"]:
    change(es_id, "data_type", "Time", STATUS_TRANSCRIPTION, p1, p1_source, "The paper reports total time spent in diving or jumping, not event counts.")
    change(es_id, "data_units", "s", STATUS_TRANSCRIPTION, p1, p1_source, "The outcome is a duration in seconds.")


# Package 2: Uygur 2010 — 45 minutes and group sample sizes.
p2 = "2 – Uygur 2010 exposure and sample sizes"
p2_source = "included_studies/uygur_2010_aphyhun.pdf, Methods and Table II"
for es_id in ["es001", "es002", "es003"]:
    change(es_id, "exposure_session_duration_h", 0.75, STATUS_TRANSCRIPTION, p2, p2_source, "The paper reports 45 minutes per day; 45/60 = 0.75 hours.")
    change(es_id, "c_n", 10, STATUS_TRANSCRIPTION, p2, p2_source, "Table II identifies the control group as CON, n=10.")
    change(es_id, "ex_n", 9, STATUS_TRANSCRIPTION, p2, p2_source, "Table II identifies the prenatal-stress group as PSN, n=9.")


# Package 3: Arjunan 2023 — audible white noise spanning 0–20 kHz.
p3 = "3 – Arjunan 2023 acoustic exposure"
p3_source = "included_studies/arjunan_2023_stress.pdf, Methods section 4.3"
for es_id in ["es013", "es014", "es015", "es016", "es017", "es018"]:
    change(es_id, "noise_type", "White noise", STATUS_TRANSCRIPTION, p3, p3_source, "The source describes a white-noise generator, not ultrasound.")
    change(es_id, "noise_type_2", "Audible", STATUS_TRANSCRIPTION, p3, p3_source, "The stated range is within the audible/broadband band used in this review.")
    change(es_id, "frequency_Hz", "0-20,000", STATUS_TRANSCRIPTION, p3, p3_source, "The source states all frequencies from 0 to 20 kHz.")
for es_id in ["es014", "es016", "es018"]:
    change(es_id, "data_file", "arjunan_2023_stress_fig3B_peri.png", STATUS_TRANSCRIPTION, p3, "Metadigitise_figs/arjunan_2023_stress_fig3B_peri.png", "Use the exact saved image filename for reproducibility.")


# Package 4: Barzegar 2014 — copied title, figure traceability, and one SEM transcription.
p4 = "4 – Barzegar 2014 title and SEM"
p4_pdf = "included_studies/barzegar_2014_hippo.pdf"
barzegar_title = "Prenatal Exposure to Noise Stress: Anxiety, Impaired Spatial Memory, and Deteriorated Hippocampal Plasticity in Postnatal Life"
change("es004", "title", barzegar_title, STATUS_TRANSCRIPTION, p4, p4_pdf, "Replace the title copied from another study with the Barzegar paper title.")
for es_id in ["es004", "es006", "es008"]:
    change(es_id, "data_file", "barzegar_2014_figure2a.png", STATUS_TRANSCRIPTION, p4, "Metadigitise_figs/barzegar_2014_figure2a.png", "Use the exact saved image filename for reproducibility.")
for es_id in ["es005", "es007", "es009"]:
    change(es_id, "data_file", "barzegar_2014_figure2b.png", STATUS_TRANSCRIPTION, p4, "Metadigitise_figs/barzegar_2014_figure2b.png", "Use the exact saved image filename for reproducibility.")


# Package 5: Abramova 2020 — source SD and deterministic SE derivation.
p5 = "5 – Abramova 2020 derived SEs"
p5_source = "included_studies/abramova_2020_genpath/abramova2020_descriptives.xlsx, tidy_all"
change("es162", "ex_sd", 28.935591, STATUS_TRANSCRIPTION, p5, p5_source, "Use the SD in the matching author-data descriptive row before deriving SE.")


# Package 6: Abramova 2021 — replace opposite-sex controls with same-sex author raw groups.
p6 = "6 – Abramova 2021 same-sex controls"
p6_source = "included_studies/abramova_2021_front/abramova_2021_front.xlsx, Лист1, handling=No handling"
raw21 = pd.read_excel(ROOT / "included_studies/abramova_2021_front/abramova_2021_front.xlsx", sheet_name="Лист1")
metric_map = {
    "Sections crossed": "squares",
    "Rearing frequency": "rearing",
    "Center entries (crossing)": "center_num",
    "Time in central square": "center_totalTime",
    "Grooming frequency": "grum_number",
    "Total grooming time": "grum_totalTime",
    "Total freezing time": "freez_totalTime",
}
for idx in df.index[df["study_id"].eq("abramova_2021_front")]:
    es_id = df.at[idx, "es_id"]
    sex = "Females" if str(df.at[idx, "offspring_sex"]).lower() == "female" else "Males"
    metric = metric_map[df.at[idx, "measurement_variable"]]
    subset = raw21[(raw21["handling"] == "No handling") & (raw21["group"] == "Control") & (raw21["sex"] == sex)][metric].dropna()
    n = int(subset.count())
    mean = float(subset.mean())
    sd = float(subset.std(ddof=1))
    change(es_id, "c_n", n, STATUS_TRANSCRIPTION, p6, p6_source, f"Use the {sex.lower()} control subgroup matching offspring_sex.")
    change(es_id, "c_mean", round(mean, 6), STATUS_TRANSCRIPTION, p6, p6_source, f"Recalculate the control mean from the same-sex author raw subgroup ({metric}).")
    change(es_id, "c_sd", round(sd, 6), STATUS_TRANSCRIPTION, p6, p6_source, f"Recalculate the control SD from the same-sex author raw subgroup ({metric}).")
    change(es_id, "data_source", "Author raw data", STATUS_TRANSCRIPTION, p6, p6_source, "All summaries in this package are calculated from the saved author workbook.")
    change(es_id, "data_file", "included_studies/abramova_2021_front/abramova_2021_front.xlsx", STATUS_TRANSCRIPTION, p6, p6_source, "Use the stable path to the saved author workbook.")
for es_id in ["es080", "es081"]:
    change(es_id, "data_type", "Time", STATUS_TRANSCRIPTION, p6, p6_source, "The author raw variable center_totalTime is a duration, not a count.")
    change(es_id, "data_units", "s", STATUS_TRANSCRIPTION, p6, "included_studies/abramova_2021_front/abramova_2021_front.pdf, Open-Field Test methods", "Open-field durations are recorded in seconds.")


# Package 7: Abramova 2023 — sex-coded identifiers, units, and source traceability.
p7 = "7 – Abramova 2023 identifiers and units"
p7_source = "included_studies/abramova_2023_biopsy/abramova_2023_biopsy_data_calculations.xlsx, Table1_Extract"
raw23 = pd.read_excel(ROOT / "included_studies/abramova_2023_biopsy/abramova_2023_biopsy_data_calculations.xlsx", sheet_name="Table1_Extract")
raw23 = raw23[raw23["Test"].ne("Social interaction")].reset_index(drop=True)
idx23 = df.index[df["study_id"].eq("abramova_2023_biopsy")].tolist()
if len(raw23) != len(idx23):
    raise RuntimeError(f"Abramova 2023 source alignment failed: {len(raw23)} source rows vs {len(idx23)} CSV rows")
for source_i, idx in enumerate(idx23):
    es_id = df.at[idx, "es_id"]
    source_sex = str(raw23.at[source_i, "Sex"]).strip().lower()
    expected_sex = str(df.at[idx, "offspring_sex"]).strip().lower()
    if source_sex != expected_sex:
        raise RuntimeError(f"Abramova 2023 row order/sex mismatch at {es_id}: {source_sex} vs {expected_sex}")
    token = "f" if expected_sex == "female" else "m"
    change(es_id, "c_a_id", f"KON_{token}_", STATUS_TRANSCRIPTION, p7, p7_source, "Make the control identifier agree with the sex in the paired source row.")
    change(es_id, "ex_a_id", f"PS_{token}_", STATUS_TRANSCRIPTION, p7, p7_source, "Make the exposed identifier agree with the sex in the paired source row.")
    change(es_id, "comparison", f"KON_PS_{token}_", STATUS_TRANSCRIPTION, p7, p7_source, "Make the comparison identifier agree with the sex in the paired source row.")
    change(es_id, "data_file", "included_studies/abramova_2023_biopsy/abramova_2023_biopsy_data_calculations.xlsx", STATUS_TRANSCRIPTION, p7, p7_source, "Use the stable path to the saved extraction/calculation workbook.")
for es_id in ["es176", "es177", "es196", "es197"]:
    change(es_id, "data_type", "Time", STATUS_TRANSCRIPTION, p7, p7_source, "Mean grooming duration is a duration, not a percentage.")
    change(es_id, "data_units", "s", STATUS_TRANSCRIPTION, p7, p7_source, "The source table reports mean grooming duration in seconds.")


# Populate reported/analysis SE provenance. The legacy c_se/ex_se fields are retained unchanged.
reported_studies = {
    "uygur_2010_aphyhun", "uygur_2011_ankarauniv", "barzegar_2014_hippo",
    "badache_2017_stress", "hadizadeh_2018_irjbamedsci",
    "nishio_2006_intjdevlneur", "oliveira_2015_jbehavbraisci",
}
for idx, row in df.iterrows():
    study_id = row["study_id"]
    es_id = row["es_id"]
    source = generic_source(row)
    for arm in ["c", "ex"]:
        legacy_se = row[f"{arm}_se"]
        sd = df.at[idx, f"{arm}_sd"]
        n = df.at[idx, f"{arm}_n"]
        reported = np.nan
        analysis = np.nan
        derivation = "Not available"

        if study_id == "whitlow_1978_thesis":
            analysis = float(sd) / math.sqrt(float(n)) if pd.notna(sd) and pd.notna(n) and float(n) > 0 else np.nan
            derivation = "Accepted analysis assumption: SD = sqrt(mean); SE = SD / sqrt(n)"
            source = "included_studies/whitlow_1978_thesis.pdf; figure error bars are not defined; assumption approved by reviewer"
            if pd.notna(analysis):
                corrections.append({
                    "package": "Variance decision – Whitlow 1978",
                    "study_id": study_id,
                    "es_id": es_id,
                    "source_csv_row": int(df.at[idx, "source_csv_row"]),
                    "field": f"{arm}_se_analysis",
                    "old_value_v3": norm(legacy_se),
                    "new_value_v4": norm(round(analysis, 6)),
                    "status": STATUS_DERIVED,
                    "source": source,
                    "rationale": "Apply the reviewer-approved variance assumption transparently; no author-reported variance is implied.",
                })
                mark(es_id, STATUS_DERIVED, "Variance decision – Whitlow 1978", "Variance assumption accepted: SD=sqrt(mean), then SE=SD/sqrt(n).")
        elif study_id == "abramova_2020_genpath":
            analysis = float(sd) / math.sqrt(float(n)) if pd.notna(sd) and pd.notna(n) and float(n) > 0 else np.nan
            derivation = "SD / sqrt(n), using descriptive statistics calculated from author raw data"
            source = p5_source
            if pd.notna(legacy_se) and pd.notna(analysis) and not same(legacy_se, analysis, tol=5e-5):
                corrections.append({
                    "package": p5,
                    "study_id": study_id,
                    "es_id": es_id,
                    "source_csv_row": int(df.at[idx, "source_csv_row"]),
                    "field": f"{arm}_se_analysis",
                    "old_value_v3": norm(legacy_se),
                    "new_value_v4": norm(round(analysis, 6)),
                    "status": STATUS_DERIVED,
                    "source": source,
                    "rationale": "Retain the author-data SD and n; correct only the deterministic SE derivation.",
                })
                mark(es_id, STATUS_DERIVED, p5, "The analysis SE is recalculated as SD/sqrt(n); no author-reported statistic is overwritten.")
        elif study_id == "abramova_2021_front":
            analysis = float(sd) / math.sqrt(float(n)) if pd.notna(sd) and pd.notna(n) and float(n) > 0 else np.nan
            derivation = "SD / sqrt(n), using the same-sex subgroup in author raw data"
            source = p6_source
            if arm == "c" and pd.notna(legacy_se) and pd.notna(analysis) and not same(legacy_se, analysis, tol=5e-5):
                corrections.append({
                    "package": p6,
                    "study_id": study_id,
                    "es_id": es_id,
                    "source_csv_row": int(df.at[idx, "source_csv_row"]),
                    "field": "c_se_analysis",
                    "old_value_v3": norm(legacy_se),
                    "new_value_v4": norm(round(analysis, 6)),
                    "status": STATUS_DERIVED,
                    "source": source,
                    "rationale": "Recalculate SE after replacing the opposite-sex control summary with the same-sex subgroup.",
                })
        elif study_id == "abramova_2023_biopsy":
            source_i = idx23.index(idx)
            report_type = str(raw23.at[source_i, "Reported in paper"])
            if "Mean" in report_type and "SEM" in report_type:
                source_value = raw23.at[source_i, f"{arm}_se ({'control' if arm == 'c' else 'PS'} se)"] if arm == "c" else raw23.at[source_i, "ex_se (PS se)"]
                reported = float(source_value)
                analysis = float(source_value)
                derivation = "Reported SEM; used unchanged for analysis"
                source = f"{p7_source}, source row {source_i + 2}"
            else:
                derivation = "Not calculated here: median (Q1; Q3) reported; estimation is deferred to reproducible R data wrangling"
                source = f"{p7_source}, source row {source_i + 2}"
                add_decision(
                    es_id,
                    p7,
                    "Choose and implement the central-tendency/dispersion conversion in the R data-wrangling workflow.",
                    "Reported median and quartiles are preserved; no estimate is calculated in the cross-check dataset and analysis SE remains blank.",
                    "Use a documented established conversion in R, retain reported median/Q1/Q3, record package versions and formulas, and run a sensitivity analysis where appropriate.",
                    source,
                )
        elif study_id == "barzegar_2014_hippo":
            reported = legacy_se
            if es_id == "es006" and arm == "ex":
                reported = 2.666667
                corrections.append({
                    "package": p4,
                    "study_id": study_id,
                    "es_id": es_id,
                    "source_csv_row": int(df.at[idx, "source_csv_row"]),
                    "field": "ex_se_reported",
                    "old_value_v3": norm(legacy_se),
                    "new_value_v4": norm(reported),
                    "status": STATUS_TRANSCRIPTION,
                    "source": "Metadigitise_figs/metaDigitise_output.csv; barzegar_2014_figure2a, N2",
                    "rationale": "The digitised figure error is SEM; 8.43 is the corresponding SD, not the reported SEM.",
                })
                mark(es_id, STATUS_TRANSCRIPTION, p4, "Correct the N2 experimental SEM transcription while retaining the source-reported figure value separately.")
            analysis = reported
            derivation = "Digitised reported SEM; used unchanged for analysis"
            source = "Metadigitise_figs/metaDigitise_output.csv and saved figure image"
        elif study_id in reported_studies or (pd.notna(legacy_se) and pd.isna(sd)) or "Mean±SEM" in str(row.get("stat_comment", "")):
            reported = legacy_se
            analysis = legacy_se
            derivation = "Reported SEM; used unchanged for analysis"
        elif pd.notna(sd) and pd.notna(n) and float(n) > 0:
            analysis = float(sd) / math.sqrt(float(n))
            derivation = "SD / sqrt(n); derived for analysis from the extracted SD and sample size"
        elif pd.notna(legacy_se):
            reported = legacy_se
            analysis = legacy_se
            derivation = "Legacy extraction treated as reported SEM; source classification should be retained with the extraction record"

        set_se(idx, arm, reported, round(analysis, 6) if pd.notna(analysis) else np.nan, derivation, source)


# The Abramova 2024 author email is now archived; update traceability without changing statistics.
email_source = "included_studies/abramova_2024_devneur/abramova_2024_devneur_author_email_sucrose_preference.png"
for es_id in ["es045", "es046"]:
    change(es_id, "data_source", "Author email (saved screenshot)", STATUS_TRANSCRIPTION, "Source follow-up – Abramova 2024", email_source, "The supplied author email confirms the stored mean and SE values.")
    change(es_id, "data_file", email_source, STATUS_TRANSCRIPTION, "Source follow-up – Abramova 2024", email_source, "Link the extracted values to the archived author correspondence screenshot.")
    idx = row_index(es_id)
    for arm in ["c", "ex"]:
        df.at[idx, f"{arm}_se_source"] = email_source
        df.at[idx, f"{arm}_se_derivation"] = "Reported SE in author email; used unchanged for analysis"


# Assign one primary row flag. Unresolved source/analysis needs take priority over completed corrections.
priority = [STATUS_SOURCE, STATUS_DECISION, STATUS_TRANSCRIPTION, STATUS_DERIVED]
for idx, es_id in zip(df.index, df["es_id"]):
    flags = row_flags[es_id]
    df.at[idx, "crosscheck_status"] = next((s for s in priority if s in flags), STATUS_VERIFIED)
    df.at[idx, "crosscheck_package"] = "; ".join(sorted(row_packages[es_id]))
    df.at[idx, "crosscheck_notes"] = " | ".join(row_notes[es_id])


# A compact all-row register makes the five-status workflow filterable without scanning the wide data sheet.
status_cols = [
    "source_csv_row", "study_id", "es_id", "offspring_sex", "measurement_variable",
    "crosscheck_status", "crosscheck_package", "crosscheck_notes",
    "c_se_reported", "c_se_analysis", "c_se_derivation", "c_se_source",
    "ex_se_reported", "ex_se_analysis", "ex_se_derivation", "ex_se_source",
]
status_df = df[status_cols].copy()
corrections_df = pd.DataFrame(corrections).sort_values(["package", "source_csv_row", "field"], kind="stable")
decisions_df = pd.DataFrame(decisions).drop_duplicates(subset=["study_id", "es_id", "status", "decision"]).sort_values(["status", "source_csv_row"], kind="stable")
wrangling_df = pd.DataFrame([
    {
        "topic": "Missing central tendency and dispersion estimates",
        "scope": "All studies where authors did not report an analysis-ready mean/SD/SE",
        "status": "Deferred to R data wrangling",
        "decision": "Do not estimate missing central tendencies during source cross-checking.",
        "implementation_stage": "R workflow used to prepare data for IRR and analysis",
        "reproducibility_requirement": "Keep reported median/Q1/Q3 unchanged; write explicit R formulas/functions, method citation, package versions, and sensitivity-analysis fields.",
        "current_dataset_treatment": "Reported values retained; analysis estimates remain blank until the R workflow is run.",
    },
    {
        "topic": "Abramova median/IQR derivations",
        "scope": "Abramova papers, including 18 Abramova 2023 median (Q1; Q3) rows",
        "status": "Deferred to R data wrangling",
        "decision": "Perform all missing central-tendency/dispersion derivations reproducibly in R, not manually in v4.",
        "implementation_stage": "R workflow used to prepare data for IRR and analysis",
        "reproducibility_requirement": "Preserve author-reported statistics in separate columns and generate analysis estimates with auditable code.",
        "current_dataset_treatment": "c_se_analysis/ex_se_analysis remain blank for these rows.",
    },
    {
        "topic": "Whitlow 1978 variance",
        "scope": "36 whitlow_1978_thesis rows",
        "status": "Assumption accepted",
        "decision": "Assume SD = sqrt(mean), then calculate SE = SD/sqrt(n).",
        "implementation_stage": "Cross-check v4 and later R workflow",
        "reproducibility_requirement": "Label the values as an analysis assumption, never as author-reported variance, and retain for sensitivity analysis.",
        "current_dataset_treatment": "Reported SE is blank; analysis SE is populated from the accepted assumption.",
    },
    {
        "topic": "Abramova 2024 sucrose preference source",
        "scope": "es045 and es046",
        "status": "Source archived and verified",
        "decision": "Use the author-email mean ± SE values unchanged.",
        "implementation_stage": "Cross-check v4",
        "reproducibility_requirement": f"Retain the archived screenshot at {email_source}.",
        "current_dataset_treatment": "Source traceability updated; numerical values unchanged.",
    },
])

AUDIT_DIR.mkdir(parents=True, exist_ok=True)
OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False, encoding="utf-8")
corrections_df.to_csv(CORRECTION_LOG, index=False, encoding="utf-8")
status_df.to_csv(ROW_STATUS, index=False, encoding="utf-8")
decisions_df.to_csv(DECISION_REGISTER, index=False, encoding="utf-8")
wrangling_df.to_csv(WRANGLING_PLAN, index=False, encoding="utf-8")

status_counts = df["crosscheck_status"].value_counts().reindex(
    [STATUS_VERIFIED, STATUS_TRANSCRIPTION, STATUS_DERIVED, STATUS_DECISION, STATUS_SOURCE], fill_value=0
).to_dict()
package_summary = (
    corrections_df.groupby(["package", "status"], dropna=False)
    .agg(cells=("field", "size"), rows=("es_id", "nunique"))
    .reset_index()
    .to_dict(orient="records")
)
summary = {
    "source_file": str(SOURCE.relative_to(ROOT)),
    "source_sha256": source_hash,
    "output_file": str(OUT.relative_to(ROOT)),
    "rows": int(len(df)),
    "columns": int(len(df.columns)),
    "correction_log_entries": int(len(corrections_df)),
    "rows_with_logged_corrections": int(corrections_df["es_id"].nunique()),
    "decision_register_entries": int(len(decisions_df)),
    "wrangling_plan_entries": int(len(wrangling_df)),
    "status_counts": status_counts,
    "package_summary": package_summary,
}
SUMMARY_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(summary, indent=2, ensure_ascii=False))
