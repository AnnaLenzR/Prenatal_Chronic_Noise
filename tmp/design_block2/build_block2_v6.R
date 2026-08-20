options(stringsAsFactors = FALSE)

input_csv <- "Data/PCN_data_ext_checking_v.5_design_decisions.csv"
output_csv <- "Data/PCN_data_ext_checking_v.6_design_decisions.csv"
block1_register_csv <- "Data/audits/design_dependence_register_v5_block1.csv"
cumulative_register_csv <- "Data/audits/design_dependence_register_v6_blocks1_2.csv"
block2_register_csv <- "Data/audits/design_dependence_register_v6_block2.csv"
correction_log_csv <- "Data/audits/correction_log_v6_block2.csv"
decision_register_csv <- "Data/audits/decision_register_v6_block2.csv"

d <- read.csv(input_csv, check.names = FALSE, na.strings = character())
stopifnot(nrow(d) == 207L)

target <- d$study_id == "hadizadeh_2018_irjbamedsci" & d$es_id %in% c("es019", "es020")
old_note <- "one control, one treatment for females and males"
new_note <- "One control and one stress group; male offspring only"
stopifnot(sum(target) == 2L, all(d$id_notes[target] == old_note), all(d$offspring_sex[target] == "male"))
d$id_notes[target] <- new_note
write.csv(d, output_csv, row.names = FALSE, na = "")

source_rows <- setNames(d$source_csv_row, d$es_id)

make_rows <- function(study_id, es_ids, cohort_id, test_code, con_code, ex_code,
                      source, repeated = "No", multiple_outcomes = "Yes") {
  data.frame(
    study_id = study_id,
    es_id = es_ids,
    source_csv_row = unname(source_rows[es_ids]),
    arm_design = "Independent",
    study_cluster_id = study_id,
    cohort_id = cohort_id,
    test_cluster_id = paste0(study_id, "__", test_code),
    control_group_id = paste0(study_id, "__", con_code),
    experimental_group_id = paste0(study_id, "__", ex_code),
    dep_shared_control = "Yes",
    dep_shared_experimental = "Yes",
    dep_repeated_measure = repeated,
    dep_multiple_outcomes_same_test = multiple_outcomes,
    analysis_sample_size_unit = "Reported offspring/pup count",
    litter_count_used_in_model = "No",
    litter_clustering_note = "Potential within-litter similarity is acknowledged, but dam/litter counts are not consistently available; retain the authors' reported pup n.",
    decision_status = "Approved",
    decision_date = "2026-08-13",
    source = source,
    check.names = FALSE
  )
}

block2 <- rbind(
  make_rows(
    "uygur_2010_aphyhun", c("es001", "es002", "es003"),
    "uygur_2010_aphyhun__CON_PSN", "DWT", "CON", "PSN",
    "included_studies/uygur_2010_aphyhun.pdf, Defensive withdrawal test methods/results"
  ),
  make_rows(
    "hassanvand_2012_phyphar", c("es010", "es011", "es012"),
    "hassanvand_2012_phyphar__Control_Exp", "OFT", "Control", "Exp",
    "included_studies/hassanvand_2012_phyphar.pdf, Open-field methods/results"
  ),
  make_rows(
    "hadizadeh_2018_irjbamedsci", c("es019", "es020"),
    "hadizadeh_2018_irjbamedsci__CON_ST", "EPM", "CON", "ST",
    "included_studies/hadizadeh_2018_irjbamedsci.pdf, experimental groups and EPM methods/results"
  )
)
write.csv(block2, block2_register_csv, row.names = FALSE, na = "")

block1 <- read.csv(block1_register_csv, check.names = FALSE, na.strings = character())
block1$cohort_id <- ifelse(
  block1$study_id == "oliveira_2015_jbehavbraisci",
  "oliveira_2015_jbehavbraisci__C_IE",
  "whitlow_1978_thesis__experiment1"
)
desired_order <- names(block2)
block1 <- block1[, desired_order]
cumulative <- rbind(block1, block2)
stopifnot(nrow(cumulative) == 50L, !anyDuplicated(cumulative$es_id))
write.csv(cumulative, cumulative_register_csv, row.names = FALSE, na = "")

correction_log <- data.frame(
  study_id = rep("hadizadeh_2018_irjbamedsci", 2),
  es_id = c("es019", "es020"),
  source_csv_row = unname(source_rows[c("es019", "es020")]),
  variable = "id_notes",
  old_value = old_note,
  new_value = new_note,
  flag = "Corrected transcription",
  rationale = "The paper reports that only male offspring were retained for behavioral testing; the prior note incorrectly mentioned females and males.",
  source = "included_studies/hadizadeh_2018_irjbamedsci.pdf, experimental design",
  decision_date = "2026-08-13"
)
write.csv(correction_log, correction_log_csv, row.names = FALSE, na = "")

decision_register <- data.frame(
  decision_id = c("B2-01", "B2-02", "B2-03", "B2-04"),
  scope = c("Uygur es001-es003", "Hassanvand es010-es012", "Hadizadeh es019-es020", "Hadizadeh es019-es020"),
  decision = c(
    "Independent CON and PSN arms; three outcomes share both groups and one DWT session; not repeated measures.",
    "Independent Control and Exp arms; three outcomes share both groups and one OFT session; not repeated measures.",
    "Independent CON and ST arms; OAE and OAT share both groups and one EPM session; not repeated measures.",
    "Correct id_notes to state that behavioral testing used male offspring only."
  ),
  status = "Approved",
  decision_date = "2026-08-13",
  analysis_implication = c(
    "Cluster within study and DWT test; identify shared control and experimental animals.",
    "Cluster within study and OFT test; identify shared control and experimental animals.",
    "Cluster within study and EPM test; identify shared control and experimental animals.",
    "Metadata correction only; reported numerical results are unchanged."
  )
)
write.csv(decision_register, decision_register_csv, row.names = FALSE, na = "")

v6 <- read.csv(output_csv, check.names = FALSE, na.strings = character())
stopifnot(nrow(v6) == nrow(d), identical(names(v6), names(d)))
different_cells <- which(d != read.csv(input_csv, check.names = FALSE, na.strings = character()), arr.ind = TRUE)
stopifnot(nrow(different_cells) == 2L)
cat("Created v6 with", nrow(v6), "rows; changed cells:", nrow(different_cells), "\n")
cat("Block 2 register rows:", nrow(block2), "; cumulative register rows:", nrow(cumulative), "\n")
