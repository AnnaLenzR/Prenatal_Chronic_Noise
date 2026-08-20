options(stringsAsFactors = FALSE)

input_csv <- "Data/PCN_data_ext_checking_v.7_all_independent_arms.csv"
output_csv <- "Data/PCN_data_ext_checking_v.8_clean.csv"
removed_register_csv <- "Data/audits/column_cleanup_register_v8.csv"
renamed_register_csv <- "Data/audits/column_rename_register_v8.csv"

source <- read.csv(input_csv, check.names = FALSE, na.strings = character())
stopifnot(nrow(source) == 207L, ncol(source) == 84L, !anyDuplicated(source$es_id))

removed <- data.frame(
  column = c(
    "source_csv_row",
    "control_loudness",
    "comparison_structure",
    "c_se",
    "c_ci",
    "ex_se",
    "ex_ci",
    "checked_ML",
    "checked_ML_comments",
    "Unnamed: 70",
    "corrections_notes_AL",
    "crosscheck_package",
    "crosscheck_notes"
  ),
  reason = c(
    "Audit-only source row number; es_id is the stable unique row identifier.",
    "Completely empty in all 207 rows.",
    "Constant after the approved decision that all 207 treatment-control arms are independent; retained in the separate arm-design register.",
    "Ambiguous legacy SE field superseded by c_se_reported and c_se_analysis.",
    "Completely empty in all 207 rows.",
    "Ambiguous legacy SE field superseded by ex_se_reported and ex_se_analysis.",
    "Completely empty in all 207 rows.",
    "Legacy reviewer workflow flag; superseded by the approved data-status system and audit logs.",
    "Legacy reviewer working comments; preserved in v7 but not needed in the clean analysis sheet.",
    "Unnamed and completely empty source column.",
    "Working correction notes; final corrections are preserved in versioned audit logs.",
    "Temporary correction-package label; package membership is preserved in the audit files.",
    "Detailed cross-check working notes; decisions and corrections are preserved in the audit files."
  ),
  nonblank_values = vapply(
    source[c(
      "source_csv_row", "control_loudness", "comparison_structure", "c_se", "c_ci",
      "ex_se", "ex_ci", "checked_ML", "checked_ML_comments", "Unnamed: 70",
      "corrections_notes_AL", "crosscheck_package", "crosscheck_notes"
    )],
    function(x) sum(!is.na(x) & trimws(as.character(x)) != ""),
    integer(1)
  ),
  recovery_location = "Data/PCN_data_ext_checking_v.7_all_independent_arms.csv",
  cleanup_date = "2026-08-13",
  check.names = FALSE
)
write.csv(removed, removed_register_csv, row.names = FALSE, na = "")

renamed <- data.frame(
  old_column = c("higher_better_notes", "higher_better_notes.1", "crosscheck_status"),
  new_column = c("effect_direction_label", "higher_better_notes", "data_status"),
  rationale = c(
    "The values are Positive/Negative direction labels, not explanatory notes.",
    "This is the actual explanatory higher-better note field.",
    "Shorter, clearer name for the approved Verified/Corrected/Decision-required flag."
  ),
  cleanup_date = "2026-08-13",
  check.names = FALSE
)
write.csv(renamed, renamed_register_csv, row.names = FALSE, na = "")

clean <- source[, setdiff(names(source), removed$column), drop = FALSE]
names(clean)[names(clean) == "higher_better_notes"] <- "effect_direction_label"
names(clean)[names(clean) == "higher_better_notes.1"] <- "higher_better_notes"
names(clean)[names(clean) == "crosscheck_status"] <- "data_status"

ordered_columns <- c(
  # Stable identifiers and review status
  "study_id", "es_id", "ex_id", "con_id", "out_id", "shared_control",
  "data_status", "id_notes", "outcome_id_notes",

  # Citation and biological context
  "title", "doi", "publish_in", "sp_latin", "sp_common", "strain",
  "dam_age", "dam_age_notes", "gest_stage_ex", "gest_stage_ex_notes",

  # Exposure details
  "exposure_span_d", "exposure_type", "exposure_session_duration_h",
  "ex_session_duration_notes", "noise_type", "noise_type_2", "loudness_dB",
  "frequency_Hz", "control_conditions", "control_notes",

  # Offspring and procedures
  "offspring_sex", "offspring_age_d", "offspring_age_notes",
  "experimental_procedures", "experimental_procedures_notes",

  # Outcome definition
  "outcome_type", "assay_type", "assay_type_notes", "measurement_variable",
  "data_type", "data_units", "measurement_timing", "data_source", "data_file",

  # Comparison and direction
  "c_a_id", "ex_a_id", "comparison", "higher_better",
  "effect_direction_label", "higher_better_notes",

  # Control statistics and provenance
  "c_mean", "c_sd", "c_n", "c_se_reported", "c_se_analysis",
  "c_se_derivation", "c_se_source", "c_median", "c_q1", "c_q3",

  # Experimental statistics and provenance
  "ex_mean", "ex_sd", "ex_n", "ex_se_reported", "ex_se_analysis",
  "ex_se_derivation", "ex_se_source", "ex_median", "ex_q1", "ex_q3",

  # Remaining source comments
  "stat_comment", "general_comment"
)

stopifnot(
  length(ordered_columns) == ncol(clean),
  setequal(ordered_columns, names(clean)),
  !anyDuplicated(ordered_columns)
)
clean <- clean[, ordered_columns, drop = FALSE]
write.csv(clean, output_csv, row.names = FALSE, na = "")

reloaded <- read.csv(output_csv, check.names = FALSE, na.strings = character())
stopifnot(
  nrow(reloaded) == 207L,
  ncol(reloaded) == 71L,
  identical(reloaded$es_id, source$es_id),
  !anyDuplicated(reloaded$es_id),
  all(reloaded$data_status %in% c(
    "Verified – no change",
    "Corrected transcription",
    "Corrected derived value",
    "Analysis decision required",
    "Source needed"
  ))
)

rename_map <- setNames(renamed$old_column, renamed$new_column)
for (column in names(reloaded)) {
  source_column <- if (column %in% names(rename_map)) rename_map[[column]] else column
  stopifnot(identical(as.character(reloaded[[column]]), as.character(source[[source_column]])))
}

cat("Created", output_csv, "with", nrow(reloaded), "rows and", ncol(reloaded), "columns.\n")
cat("Removed columns:", nrow(removed), "\n")
cat("Renamed columns:", nrow(renamed), "\n")
cat("Retained values changed: 0\n")
