options(stringsAsFactors = FALSE)

input_csv <- "Data/PCN_data_ext_checking_v.6_design_decisions.csv"
output_csv <- "Data/PCN_data_ext_checking_v.7_all_independent_arms.csv"
correction_log_csv <- "Data/audits/correction_log_v7_all_independent_arms.csv"
arm_register_csv <- "Data/audits/arm_design_register_v7_all_rows.csv"
decision_register_csv <- "Data/audits/decision_register_v7_arm_design.csv"
study_counts_csv <- "Data/audits/arm_design_counts_by_study_v7.csv"

source <- read.csv(input_csv, check.names = FALSE, na.strings = character())
stopifnot(nrow(source) == 207L)

comparison_normalized <- trimws(tolower(as.character(source$comparison_structure)))
target <- comparison_normalized == "dependent"
stopifnot(sum(target) == 42L)

target_counts <- sort(unclass(table(source$study_id[target])))
expected_counts <- sort(c(
  oliveira_2015_jbehavbraisci = 6L,
  whitlow_1978_thesis = 36L
))
stopifnot(identical(target_counts, expected_counts))

v7 <- source
v7$comparison_structure[target] <- "Independent"

final_comparison <- trimws(tolower(as.character(v7$comparison_structure)))
stopifnot(all(final_comparison == "independent"))
write.csv(v7, output_csv, row.names = FALSE, na = "")

correction_log <- data.frame(
  study_id = source$study_id[target],
  es_id = source$es_id[target],
  source_csv_row = source$source_csv_row[target],
  variable = "comparison_structure",
  old_value = source$comparison_structure[target],
  new_value = "Independent",
  flag = "Corrected classification",
  rationale = paste(
    "Control and noise-exposed animals are separate groups.",
    "Repeated measurements, shared groups, or multiple outcomes create dependence between effect sizes,",
    "not paired treatment-control arms."
  ),
  decision_source = "Review-team decision confirmed by Anna Lenz on 2026-08-13",
  decision_date = "2026-08-13",
  check.names = FALSE
)
write.csv(correction_log, correction_log_csv, row.names = FALSE, na = "")

arm_register <- data.frame(
  study_id = v7$study_id,
  es_id = v7$es_id,
  source_csv_row = v7$source_csv_row,
  con_id = v7$con_id,
  ex_id = v7$ex_id,
  arm_design = "Independent",
  treatment_control_correlation_used = "No",
  per_effect_size_estimator = ifelse(
    tolower(v7$data_type) == "percentage",
    "Independent-arm percentage formulation",
    "Independent-arm lnRR formulation"
  ),
  decision_status = "Approved",
  decision_source = "Review-team decision confirmed by Anna Lenz on 2026-08-13",
  decision_date = "2026-08-13",
  check.names = FALSE
)
stopifnot(nrow(arm_register) == 207L, all(arm_register$arm_design == "Independent"))
write.csv(arm_register, arm_register_csv, row.names = FALSE, na = "")

study_counts <- aggregate(
  es_id ~ study_id + arm_design,
  data = arm_register,
  FUN = length
)
names(study_counts)[names(study_counts) == "es_id"] <- "effect_size_rows"
study_counts <- study_counts[order(study_counts$study_id), ]
stopifnot(sum(study_counts$effect_size_rows) == 207L)
write.csv(study_counts, study_counts_csv, row.names = FALSE, na = "")

decision_register <- data.frame(
  decision_id = c("ARM-01", "ARM-02", "ARM-03", "ARM-04"),
  scope = c("All 207 effect sizes", "Oliveira es047-es052", "Whitlow es094-es129", "Analysis workflow"),
  decision = c(
    "All control and noise-exposed arms consist of different animals and are classified as independent.",
    "Replace the six legacy Dependent labels with Independent.",
    "Replace the 36 legacy Dependent labels with Independent.",
    "Do not use ROMC or a treatment-control correlation; model dependence among effect sizes separately."
  ),
  status = "Approved",
  decision_date = "2026-08-13",
  analysis_implication = c(
    "Use the independent-arm branch for every row.",
    "Repeated ETM outcomes remain dependent across effect sizes.",
    "Shared groups, repeated times, and multiple OFT outcomes remain dependent across effect sizes.",
    "Retain group, cohort, test, time, and outcome identifiers for the later VCV construction."
  ),
  check.names = FALSE
)
write.csv(decision_register, decision_register_csv, row.names = FALSE, na = "")

reloaded <- read.csv(output_csv, check.names = FALSE, na.strings = character())
stopifnot(nrow(reloaded) == nrow(source), identical(names(reloaded), names(source)))

different <- mapply(
  function(x, y) {
    same_na <- is.na(x) & is.na(y)
    different_na <- is.na(x) != is.na(y)
    ifelse(same_na, FALSE, ifelse(different_na, TRUE, as.character(x) != as.character(y)))
  },
  source,
  reloaded,
  SIMPLIFY = FALSE
)
different <- do.call(cbind, different)
different_locations <- which(different, arr.ind = TRUE)

stopifnot(
  nrow(different_locations) == 42L,
  all(names(source)[different_locations[, "col"]] == "comparison_structure")
)

numeric_columns <- names(source)[vapply(source, is.numeric, logical(1))]
for (column in numeric_columns) {
  stopifnot(identical(source[[column]], reloaded[[column]]))
}

cat("Created", output_csv, "with", nrow(reloaded), "rows.\n")
cat("Corrected comparison_structure cells:", nrow(different_locations), "\n")
cat("Final independent-arm rows:", sum(tolower(reloaded$comparison_structure) == "independent"), "\n")
cat("Reported numeric columns changed: 0\n")
