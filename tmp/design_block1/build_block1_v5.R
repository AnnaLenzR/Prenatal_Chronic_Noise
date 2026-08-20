source_path <- "Data/PCN_data_ext_checking_v.4_crosschecked.csv"
output_path <- "Data/PCN_data_ext_checking_v.5_design_decisions.csv"
correction_log_path <- "Data/audits/correction_log_v5_block1.csv"
design_register_path <- "Data/audits/design_dependence_register_v5_block1.csv"
decision_register_path <- "Data/audits/decision_register_v5_block1.csv"

read_character_csv <- function(path) {
  read.csv(
    path,
    check.names = FALSE,
    colClasses = "character",
    na.strings = NULL,
    stringsAsFactors = FALSE,
    fileEncoding = "UTF-8"
  )
}

write_character_csv <- function(x, path) {
  write.csv(
    x,
    path,
    row.names = FALSE,
    na = "",
    qmethod = "double",
    fileEncoding = "UTF-8"
  )
}

d <- read_character_csv(source_path)
stopifnot(nrow(d) == 207L)
stopifnot(!anyDuplicated(d$es_id))

whitlow <- d$study_id == "whitlow_1978_thesis"
oliveira <- d$study_id == "oliveira_2015_jbehavbraisci"
stopifnot(sum(whitlow) == 36L)
stopifnot(sum(oliveira) == 6L)
stopifnot(all(d$offspring_sex[whitlow] == "male"))

old_sex <- d$offspring_sex[whitlow]
d$offspring_sex[whitlow] <- "mixed"
d$corrections_notes_AL[whitlow] <- paste(
  "Corrected offspring_sex from male to mixed.",
  "The thesis states that 2 males and 2 females were randomly selected from each litter."
)

write_character_csv(d, output_path)

correction_log <- data.frame(
  package = "Block 1 - Arm design and dependence",
  study_id = d$study_id[whitlow],
  es_id = d$es_id[whitlow],
  source_csv_row = d$source_csv_row[whitlow],
  field = "offspring_sex",
  old_value_v4 = old_sex,
  new_value_v5 = d$offspring_sex[whitlow],
  status = "Corrected transcription",
  source = paste(
    "included_studies/whitlow_1978_thesis.pdf, Experiment 1 Methods;",
    "2 males and 2 females randomly selected from each litter"
  ),
  rationale = paste(
    "Both sexes contributed to the reported group summaries;",
    "the outcome is therefore classified as mixed-sex."
  ),
  stringsAsFactors = FALSE
)
write_character_csv(correction_log, correction_log_path)

selected <- d[oliveira | whitlow, , drop = FALSE]
is_whitlow <- selected$study_id == "whitlow_1978_thesis"

control_group_id <- ifelse(
  is_whitlow,
  ifelse(grepl("^HNoN_", selected$comparison),
         "whitlow_1978_thesis__HNoN",
         "whitlow_1978_thesis__C"),
  "oliveira_2015_jbehavbraisci__C"
)
experimental_group_id <- ifelse(
  is_whitlow,
  ifelse(grepl("_HLN_", selected$comparison),
         "whitlow_1978_thesis__HLN",
         "whitlow_1978_thesis__HN"),
  "oliveira_2015_jbehavbraisci__IE"
)

design_register <- data.frame(
  study_id = selected$study_id,
  es_id = selected$es_id,
  source_csv_row = selected$source_csv_row,
  arm_design = "Independent",
  study_cluster_id = selected$study_id,
  test_cluster_id = ifelse(
    is_whitlow,
    "whitlow_1978_thesis__OFT",
    "oliveira_2015_jbehavbraisci__ETM"
  ),
  control_group_id = control_group_id,
  experimental_group_id = experimental_group_id,
  dep_shared_control = "Yes",
  dep_shared_experimental = "Yes",
  dep_repeated_measure = "Yes",
  dep_multiple_outcomes_same_test = "Yes",
  analysis_sample_size_unit = "Reported offspring/pup count",
  litter_count_used_in_model = "No",
  litter_clustering_note = paste(
    "Potential within-litter similarity is acknowledged, but dam/litter counts",
    "are not consistently available; retain the authors' reported pup n."
  ),
  decision_status = "Approved",
  decision_date = "2026-08-13",
  source = ifelse(
    is_whitlow,
    "included_studies/whitlow_1978_thesis.pdf, Experiment 1 Methods",
    "included_studies/oliveira_2015_jbehavbraisci.pdf, Sections 2.1-2.5"
  ),
  stringsAsFactors = FALSE
)
write_character_csv(design_register, design_register_path)

decision_register <- data.frame(
  decision_id = c("D001", "D002", "D003", "D004"),
  block = "Block 1 - Arm design and dependence",
  scope = c(
    "Oliveira 2015: es047-es052",
    "Whitlow 1978: es094-es129",
    "All included studies",
    "Whitlow 1978: es094-es129"
  ),
  status = c("Approved", "Approved", "Approved", "Corrected transcription"),
  decision = c(
    paste(
      "Use independent-arm lnRR calculations; retain shared-control,",
      "shared-experimental, repeated-measure, and multiple-outcome dependence flags."
    ),
    paste(
      "Use independent-arm lnRR calculations; retain shared-control,",
      "shared-experimental, repeated-measure, and multiple-outcome dependence flags."
    ),
    paste(
      "Use the authors' reported offspring/pup sample size.",
      "Do not substitute dam counts because they are inconsistently reported."
    ),
    "Classify offspring_sex as mixed, not male."
  ),
  analysis_implication = c(
    "Cluster effect sizes within study and ETM test; do not use a paired-arm correlation.",
    "Cluster effect sizes within study and OFT test; do not use a paired-arm correlation.",
    paste(
      "Acknowledge possible litter clustering as a limitation;",
      "no litter-level adjustment can be implemented consistently."
    ),
    "All 36 Whitlow rows now identify the analysed offspring as mixed-sex."
  ),
  source = c(
    "included_studies/oliveira_2015_jbehavbraisci.pdf, Sections 2.1-2.5",
    "included_studies/whitlow_1978_thesis.pdf, Experiment 1 Methods",
    "User-approved analysis rule, 2026-08-13",
    "included_studies/whitlow_1978_thesis.pdf, Experiment 1 Methods"
  ),
  stringsAsFactors = FALSE
)
write_character_csv(decision_register, decision_register_path)

cat(output_path, "\n")
cat(correction_log_path, "\n")
cat(design_register_path, "\n")
cat(decision_register_path, "\n")
