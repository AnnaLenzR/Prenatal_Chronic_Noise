# Manuscript plan: prenatal chronic noise exposure and offspring behaviour

## Working title

**Effects of prenatal chronic noise exposure on anxiety- and depression-like behaviours in rodent offspring: a systematic review and multilevel meta-analysis**

This neutral title is preferable until the analysis is final because the current overall confidence intervals include no effect.

## Version basis and drafting rules

This plan is based on the registered protocol (v4, 11 November 2025), the protocol-deviation documents updated through 3 September 2026, the current `pcne_book`, and the analysis dataset rendered on 2 September 2026. Current numerical results are provisional until the book is rerendered after the final data and naming decisions.

Drafting rules:

- Use the protocol's direct first-person style: “We searched,” “We extracted,” and “We fitted.”
- Keep the subject and verb close, prefer active voice, and use specific quantities rather than “many” or “most.”
- Build each paragraph around one job and link the last idea of one sentence to the first idea of the next.
- Report estimates with confidence intervals before interpreting p-values.
- Distinguish absence of clear evidence from evidence of no effect.
- Treat all uni-moderator analyses as separate, non-additive, exploratory comparisons. Do not rank moderators only by statistical significance.
- Use “studies” for independent reports and *k* for effect sizes. Always show both where possible.
- Use “anxiety- and depression-like behaviours,” not human clinical diagnoses, when describing rodents.

## Hard word budget

Target the manuscript at about 7,700 words to leave a 300-word revision buffer below the 8,000-word ceiling.

| Component | Target words | Hard ceiling |
|---|---:|---:|
| Title, keywords, headings | 100 | 120 |
| Abstract | 230 | 250 |
| Introduction | 600 | 650 |
| Results | 950 | 1,050 |
| Discussion | 750 | 850 |
| Methods | 1,400 | 1,500 |
| Author contributions, funding, competing interests, data/code availability | 150 | 180 |
| References (estimated 40-45 references) | 900 | 1,000 |
| Eight main figures at approximately 300 words each | 2,400 | 2,400 |
| **Total** | **7,480** | **8,000** |

The supplementary material in Appendix III should carry full search strings, excluded-report lists, equations or implementation detail that the journal permits outside the main word count, complete moderator outputs, and secondary sensitivity analyses.

## Story in one sentence

Prenatal chronic noise exposure may alter mean anxiety-like behaviour in rodent offspring, but the evidence is heterogeneous, depends on what and how researchers measure, and is too uneven across biological and exposure contexts for a simple general conclusion.

## Section-by-section outline

### Abstract — 230 words

Use six compact moves:

1. **Context (35 words):** Prenatal noise is a common environmental stressor, but experimental evidence for lasting affect-related effects is dispersed and heterogeneous.
2. **Gap (25 words):** No quantitative synthesis has jointly evaluated changes in mean behaviour and inter-individual variability.
3. **Methods (60 words):** Preregistered systematic review; seven search sources; 16 studies; 187 lnRR and 175 lnVR effect sizes; multilevel models with sampling covariances and study, effect-size, and strain random effects.
4. **Overall results (45 words):** Current lnRR = 0.197, 95% CI [-0.055, 0.449]; current lnVR = -0.042, 95% CI [-0.206, 0.122]. Translate cautiously: approximately 22% higher mean adverse behaviour, but the interval includes no difference.
5. **Heterogeneity/moderators/robustness (45 words):** High heterogeneity; outcome-type contrast for lnRR; selected biological and methodological moderators; no small-study or time-lag pattern; Abramova-laboratory exclusion did not materially change the estimate.
6. **Conclusion (20 words):** Emphasize uncertainty, uneven evidence coverage, and the need for better-reported, sex-balanced, independently replicated experiments.

Do not write “prenatal noise had no effect.” The current result is imprecise and compatible with effects in both directions.

### Introduction — 600 words

#### Paragraph 1 — Why prenatal noise matters (120 words)

- Introduce environmental noise as a widespread stressor.
- Explain why gestation is a sensitive period for neurodevelopmental programming.
- Link prenatal stress to persistent behavioural and neuroendocrine consequences in offspring.

#### Paragraph 2 — Why rodent evidence is useful but difficult to interpret (130 words)

- Rodent experiments can isolate exposure timing, intensity, and acoustic properties more clearly than observational human studies.
- Anxiety- and depression-like assays measure different behavioural processes and may respond differently.
- Existing studies vary in strain, sex, offspring age, gestational window, noise type, loudness, control conditions, and assay.

#### Paragraph 3 — Why means are not the complete result (110 words)

- Mean effects answer whether exposed offspring respond differently on average.
- Variability effects answer whether prenatal noise makes responses more or less heterogeneous among offspring.
- Introduce lnRR for mean differences and lnVR for absolute variability. Mention lnCVR only as a supplementary analysis.

#### Paragraph 4 — Evidence gap and need for multilevel synthesis (110 words)

- Individual studies contribute multiple, dependent outcomes.
- A multilevel meta-analysis can retain this information while representing shared groups and clustering.
- Critical appraisal is needed because incomplete reporting and risk of bias can restrict interpretation.

#### Paragraph 5 — Aim and research questions (130 words)

End with explicit numbered aims:

1. Estimate the overall effect of maternal chronic-noise exposure during gestation on mean anxiety- and depression-like behaviour in offspring.
2. Estimate whether prenatal noise changes behavioural variability among offspring.
3. Test whether offspring sex or age modifies these effects.
4. Test whether gestational timing, exposure duration, acoustic frequency range, loudness, outcome type, or behavioural assay modifies these effects.
5. Assess reporting quality, methodological quality, risk of bias, small-study patterns, time-lag patterns, and influence of individual studies or the Abramova-laboratory cluster.

Aim 2 (lnVR) was not specified in the registered protocol. We will record the addition of lnVR and lnCVR in the deviations-and-additions record and describe it explicitly in the Methods.

### Results — 950 words

#### Evidence base — 160 words

- PRISMA: 5,889 records identified; 3,576 duplicates removed; 2,313 unique records screened; 87 full texts sought/screened; 75 full-text reports excluded; 12 included from the formal search plus four benchmark-set studies; 16 studies in the meta-analysis.
- Current analysis: 187 lnRR effect sizes from 16 studies and 175 lnVR effect sizes from 14 studies.
- Effect-size distribution: 160/187 (86%) anxiety and 27/187 (14%) depression; 176/187 (94%) rat and 11/187 (6%) mouse; 92 male, 57 female, and 38 mixed-sex effect sizes.
- Make clear that these percentages describe effect sizes, not independent studies.
- Refer to Figure 1 for study-level coverage and Figure S1 for record selection.

#### Overall effects — 130 words

- lnRR: 0.197, 95% CI [-0.055, 0.449], *p* = 0.124, *k* = 187 from 16 studies. On the ratio scale, this is about 1.22, with the interval spanning about 0.95-1.57.
- lnVR: -0.042, 95% CI [-0.206, 0.122], *p* = 0.612, *k* = 175 from 14 studies.
- Heterogeneity: lnRR total I² = 95.8%; lnVR total I² = 81.8%. Present component-specific I² in Appendix III, Table S6, or a compact main-text results table.
- Interpretation: neither overall estimate provides clear evidence of a consistent population-wide change, while both show important heterogeneity.

#### Outcome type — 120 words

- lnRR differed between outcome types: depression-like outcomes were 0.258 lnRR units lower than anxiety-like outcomes, 95% CI [-0.457, -0.060], *p* = 0.011.
- The anxiety estimate was 0.238 (95% CI [-0.012, 0.489]); the implied depression estimate was approximately -0.020.
- For lnVR, depression-like outcomes were 0.209 units lower than anxiety-like outcomes, but the interval included no difference, 95% CI [-0.456, 0.037], *p* = 0.095.
- State the imbalance: anxiety contributes 160 effects from 15 studies, while depression contributes 27 effects from five studies.

#### Uni-moderators — 260 words

Lead with the complete-model rule: all planned moderators are reported in Appendix III, Tables S7-S9, regardless of estimate direction or p-value, and the main figures show a question-driven subset.

- **Biological moderators:** offspring sex and age did not clearly explain lnRR or lnVR heterogeneity in the current uni-moderator models. Stress that mixed-sex data came from only two studies and that species/strain was not tested as a moderator because strain entered as a random effect.
- **Mean effects:** behavioural assay had the largest marginal R² among the plotted protocol moderators for lnRR (6.1%; omnibus *p* = 0.063). Outcome type explained 3.8% and is shown separately in Figure 3. The control-condition model explained 5.6% (*p* = 0.030), but this was an added moderator and its silence level contained only nine effects from two studies; keep it supplementary and interpret it as study-context variation, not a causal control effect.
- **Variability:** loudness had the largest current marginal R² for lnVR (9.6%; slope = -0.0074 lnVR per dB, 95% CI [-0.0130, -0.0018]). Frequency range explained 6.3% (ultrasound-audible contrast = 0.262, 95% CI [-0.047, 0.571]); exposure type explained 6.1% (intermittent-continuous contrast = -0.253, 95% CI [-0.555, 0.049]); gestational timing explained 4.6%. Treat these as associations because moderator categories are partly confounded with study and laboratory.
- Do not call a moderator “important” only because *p* < 0.05. Compare effect size, interval, evidence coverage, and marginal R².

#### Small-study and time-lag patterns — 90 words

- N-based Egger-type coefficient = -0.040, 95% CI [-1.129, 1.049], *p* = 0.942.
- Publication-year coefficient adjusted for the precision term = 0.0072 lnRR units/year, 95% CI [-0.0023, 0.0167], *p* = 0.136.
- Describe both diagnostics as exploratory because the effect sizes are heterogeneous and dependent.
- Avoid the categorical phrase “no publication bias”; write “we found no clear small-study or time-lag pattern with these diagnostics.”

#### CRIME-Q appraisal — 100 words

- The finalized workbook contains 16 studies and 21 items spanning quality of reporting, methodological quality, and risk of bias.
- All 16 studies partly reported exposure details; none fully met the exposure-reporting items.
- Fifteen of 16 did not report an a priori sample-size calculation; allocation, cage-position protection, outcome-selection safeguards, and selective-reporting judgments were unclear for all 16.
- Blinding was unclear in 15 of 16 studies, and attrition handling was unclear in 12.
- Report item-level patterns, not a summed quality score.

#### Sensitivity analyses — 90 words

- The four Abramova-laboratory studies contributed 98/187 effect sizes (52%).
- Full data: lnRR = 0.197, 95% CI [-0.055, 0.449]. Excluding all four: lnRR = 0.232, 95% CI [-0.008, 0.471], *k* = 89 from 12 studies.
- Study-level leave-one-out estimates ranged from 0.119 to 0.263 and all current intervals included no effect.
- Excluding the two exact-zero-corrected effect sizes produced lnRR = 0.195, 95% CI [-0.055, 0.445], showing negligible change.

### Discussion — 750 words, keep as bullets for now

#### Opening synthesis

- The pooled mean effect points toward more anxiety- and depression-like behaviour after prenatal noise, but its interval includes no average difference.
- The pooled variability effect is close to zero, but high heterogeneity means that a single overall average does not describe every exposure and outcome context.
- Outcome type separates the mean response more clearly than sex or age in the current data.

#### Interpretation of mean and variability together

- A shift in the mean without a matching change in variability would imply a relatively uniform displacement of behaviour; a variability change would imply altered heterogeneity among offspring.
- The current overall models do not support either simple pattern conclusively.
- Lower lnVR at higher loudness is interesting but counterintuitive and observational across studies. Possible explanations include restricted behavioural ranges, exposure categories correlated with laboratory protocols, or genuine homogenization under intense stress. Do not present a causal mechanism without further evidence.

#### Biological moderators

- Limited evidence for sex or age moderation is not evidence that prenatal-noise effects are sex- or age-independent.
- Female, mixed-sex, mouse, and depression-like evidence is sparse relative to male rat anxiety outcomes.
- Species and strain cannot be separated cleanly with the current evidence base; strain is modelled as a grouping factor.

#### Measurement and design dependence

- Assay and outcome-type differences may reflect distinct behavioural constructs, scale properties, direction coding, or exposure sensitivity.
- Control-condition differences may reflect background acoustic environments, but silence is represented by only two studies. Treat this result as hypothesis-generating.
- Percentage outcomes enter lnRR after transformation but are excluded from lnVR/lnCVR, so the mean and variability datasets are not identical.

#### Reliability and reporting

- High I² and uneven CRIME-Q ratings limit generalization.
- Incomplete reporting of randomization, blinding, attrition, acoustic delivery, and control environments prevents firm risk-of-bias judgments.
- The Abramova sensitivity result suggests that the pooled estimate is not created solely by that laboratory, although the laboratory's 52% contribution still limits independence and external validity.

#### Strengths

- Preregistered, broad multilingual search with benchmark-based sensitivity checking.
- Complete cross-checking of extraction, if confirmed.
- Explicit harmonization of behavioural direction.
- Multilevel models retain multiple outcomes and represent shared-group sampling covariance.
- Separate analyses of mean and variability, complete moderator reporting, study-level leave-one-out checks, and adapted CRIME-Q appraisal.

#### Limitations

- Only 16 studies; moderator levels often come from few independent studies even when *k* is large.
- Uni-moderator results are correlated and do not estimate independent causal contributions.
- Working correlation ρ = 0.5 was assumed rather than observed; add a ρ-sensitivity analysis if feasible.
- lnVR and lnCVR were added after registration and must be labelled as such.
- Continuity corrections were needed for two effect sizes; the exclusion check was stable.
- Search dates, author contact outcomes, and appraisal workflow still need confirmation in the final text.

#### Recommendations

- Balance sexes and report sex-disaggregated outcomes.
- Replicate mouse and depression-like outcomes across laboratories.
- Report exact sound level, frequency spectrum, playback schedule, gestational window, background/control sound, cage placement, and acoustic isolation.
- Prespecify primary outcomes and analysis plans; report all exclusions and animal-level attrition by group.
- Report raw or individual-level data so future syntheses can model distributions and dependence more directly.

#### Closing sentence

- Prenatal noise may shape offspring affect-related behaviour, but better-replicated and better-reported experiments are needed to determine when, how strongly, and for which offspring these effects occur.

## Draft Methods — working text bank (currently about 1,800 words; compress to 1,400-1,500)

This draft is deliberately fuller than the manuscript allocation so that you can choose what to retain. Move equations, operational detail, and complete deviation descriptions to Appendix III when you compress the main Methods.

### Protocol and reporting

We preregistered the systematic-review protocol on the Open Science Framework on 14 November 2025 [ADD OSF DOI/URL and registration identifier]. We developed the search and review procedures before formal screening. We report the search following PRISMA-S and the completed review following PRISMA-EcoEvo. We will use MeRIT to report each author's methodological contributions.

### Eligibility criteria

We defined eligibility with the Population, Exposure/Intervention, Comparator, Outcomes, and Study type (PECOS) framework. We included experimental primary studies of offspring from laboratory-bred rodent dams. Eligible offspring were not genetically modified or exposed to behaviour-modifying pharmacological or surgical procedures, except for appropriate sham controls. We excluded studies in which dams or offspring received another perinatal stressor that prevented isolation of the noise effect.

Eligible dams experienced an intermittent or continuous acoustic stimulus without musical structure for at least seven consecutive days during gestation; exposure could begin before gestation if it continued during gestation. We included infrasonic, audible, or ultrasonic stimuli that the authors described and used as stressors. We excluded music, acute acoustic exposure, natural sounds, animal calls, and noise combined with other stressors when the effect of noise could not be isolated. The comparator was offspring from dams not exposed to the experimental chronic-noise treatment during gestation. Eligible controls could experience ambient sound, white noise, or explicitly reported silence.

Studies had to report at least one postnatal measure of anxiety- or depression-like behaviour. Eligible assays included the Open Field Test, Elevated Plus Maze, Elevated T Maze, Light-Dark Box, Hole Board Test, Novelty-Suppressed Feeding, Defensive Withdrawal Test, Tail Suspension Test, Forced Swim Test, Sucrose Preference Test, or an equivalent assay supported by the authors' classification. We excluded reports limited to histological, biochemical, molecular, genetic, or maternal outcomes. We included peer-reviewed studies and theses or dissertations but excluded reviews, methodological or simulation studies, case reports, and conference abstracts without sufficient methods and results.

### Search strategy and study selection

We developed English search strings from the PECOS concepts and adapted them for Scopus, Web of Science, PubMed, PsycINFO, OpenAlex, the Bielefeld Academic Search Engine (BASE), and Google Scholar. We applied no publication-year or subject-area restriction and considered records in English, French, Italian, Portuguese, Spanish, Polish, Russian, and Japanese. [ADD last search date for each source and state exactly how many Google Scholar results were retained per query.] We evaluated search sensitivity with relative recall against eight benchmark studies. Seven benchmark studies were indexed in Scopus, and the final Scopus string retrieved all seven.

We imported records into R for initial deduplication and then into Rayyan for a second deduplication and two-stage screening. Two reviewers independently screened titles and abstracts and then full texts. We resolved disagreements through discussion [ADD third-reviewer rule if used]. We recorded one primary exclusion reason for each excluded full-text report. The search identified 5,889 records; after removing 3,576 duplicates, we screened 2,313 unique records. We assessed 87 reports at full text, excluded 75, and included 12 studies from the formal search. Four additional benchmark studies met the eligibility criteria, giving 16 studies in the meta-analysis. Figure S1 presents the selection process, and Appendix III, Table S2 lists excluded full-text reports and reasons.

### Data extraction

One reviewer (A.L.) extracted study identifiers, species and strain, dam and offspring characteristics, exposure and control conditions, assay and outcome information, and the summary statistics needed to calculate effect sizes. The other team members divided and independently cross-checked the complete extraction [CONFIRM that 100% cross-checking was completed before retaining this sentence]. Before full extraction, A.L. and M.L. independently extracted two benchmark studies and reconciled differences to refine the codebook. When numerical results appeared only in figures, we digitized them with the R package `metaDigitise`.

We retained the source database unchanged and created analysis-ready derived files. When a report provided a median and interquartile range but no mean or standard deviation, we estimated the mean with the Luo et al. method and the standard deviation with the Wan et al. method. We converted standard errors to standard deviations as SD = SE × √n and calculated missing standard errors as SE = SD/√n. We retained extracted values when the required statistic was reported directly and recorded the provenance of every derived value.

We excluded ten outcomes (`out045` and `out067`-`out075`) from the analysis because the corresponding outcomes were not described in the methods of the full-text reports. We retained these rows in the extraction record and documented the exclusion before modelling. [ADD this decision to the deviations record if it is not already documented.]

### Protocol deviations and post-extraction decisions

We added several operational rules after extraction and before or during modelling. We retained offspring age in days as the primary continuous age moderator. We also classified juvenile, adolescent, and adult stages with species- and sex-specific thresholds for descriptive and sensitivity analyses only. Following the registered codebook, we extracted the gestational stage of noise exposure in `gest_stage_ex`, using early (days 0-7), mid (days 8-14), late (day 15 to term), combinations of these stages, `Not reported`, or `Unclear`. For the current meta-regression, we derived the mutually exclusive analysis variable `gest_stage_ex_standardised` with the categories `early_mid`, `mid_late`, `late`, and `full_gestation`. We added `Unclear` to the control-condition variable when the report did not distinguish silence from ambient or another acoustic condition. We used the physical control setting descriptively and did not fit it as a moderator. We renamed the standardized acoustic-band variable `noise_frequency_range` and treated its `Unclear` level as missing in moderator models. We included strain as a random-effect grouping factor rather than as a categorical uni-moderator.

The registered protocol specified lnRR but did not specify lnVR or lnCVR. We added lnVR to evaluate absolute behavioural variability and used lnCVR as a supplementary relative-variability analysis. We recorded both additions, their timing, and their rationale in the deviations-and-additions record [ADD decision date/reference once entered]. We also added exposure type and control conditions as exploratory uni-moderators; the registered questions did not explicitly promise these variables.

### Effect-size calculation

We quantified differences in mean behaviour with the bias-corrected log response ratio (lnRR):

\[
\ln RR = \ln(M_T/M_C) + \frac{1}{2}\left(\frac{SD_T^2}{N_TM_T^2}-\frac{SD_C^2}{N_CM_C^2}\right),
\]

where T and C denote prenatal-noise and control groups. We reversed the sign when higher values represented less anxiety- or depression-like behaviour. Positive lnRR values therefore represent more anxiety- or depression-like behaviour in exposed offspring, and negative values represent less.

We quantified differences in absolute variability with the bias-corrected log variability ratio:

\[
\ln VR = \ln(SD_T/SD_C) + \frac{1}{2}\left(\frac{1}{N_T-1}-\frac{1}{N_C-1}\right).
\]

Positive lnVR values represent greater variability in exposed offspring. We did not reverse lnVR because a standard deviation has no beneficial or adverse behavioural direction. We calculated lnCVR as a supplementary measure of variability relative to the mean.

We applied an arcsine-square-root transformation before calculating lnRR for percentage outcomes. We did not calculate lnVR or lnCVR for percentage outcomes because their bounded scale creates a mechanical relationship between the mean and variance. For non-percentage outcomes, we replaced a zero mean with 0.9 times the smallest positive mean in the same assay, measurement, data-type, and unit stratum. We replaced a zero standard deviation with the smallest positive standard deviation in the same arm and outcome stratum. For percentage outcomes, we replaced boundary means of 0% and 100% with 0.5% and 99.5%, respectively. We tested the influence of the two effect sizes that required both a control-mean and control-SD correction in a sensitivity analysis.

For independent-group comparisons, we calculated lnRR, lnVR, and lnCVR with `ROM`, `VR`, and `CVR` in `metafor::escalc()`. For dependent comparisons, we used `ROMC`, `VRC`, and `CVRC` and assumed a within-subject correlation of 0.5.

### Sampling dependence and meta-analytic models

We constructed a sampling variance-covariance matrix for each effect-size metric with `metafor::vcalc()`. We used study as the cluster, exposed- and control-group identifiers to identify shared groups, and group sample sizes as weights. We assumed a working correlation of ρ = 0.5 for multiple or repeated outcomes that shared an exposed or control group and assigned zero sampling covariance when effect sizes shared neither group.

We fitted separate multilevel intercept-only models for lnRR and lnVR with restricted maximum likelihood. Each model included random intercepts for study, effect-size identifier, and strain. We used t-based tests and 95% confidence intervals. We quantified total heterogeneity and its study-, effect-size-, and strain-level components with multilevel I². We present prediction intervals in the orchard plots [VERIFY that final figures include and label prediction intervals].

### Moderator analyses

We fitted one uni-moderator model at a time with the same variance-covariance matrix and random-effects structure as the corresponding overall model. Prespecified moderator concepts were offspring sex, offspring age in days, gestational timing (extracted as `gest_stage_ex` and analysed using `gest_stage_ex_standardised`), exposure duration in days, acoustic frequency range, loudness in unweighted dB, outcome type, and behavioural assay. We excluded the `Unclear` frequency-range category and excluded categorical levels represented by fewer than five effect sizes. The loudness model excluded the dBA value from Barzegar et al. because A-weighted and unweighted decibels are not directly comparable. We fitted exposure type and control conditions as added exploratory moderators.

For each model, we report the coefficient estimates, 95% confidence intervals, omnibus moderator test, marginal R², conditional R², *k*, and number of studies per level. For categorical variables with at least three retained levels, we calculated unadjusted pairwise contrasts defined by a Tukey contrast matrix. We did not adjust these exploratory contrasts for multiple comparisons; therefore, we interpret them cautiously and do not use p-values alone to select results for presentation.

The current computational rule (*k* ≥ 5 effect sizes per category) is an effect-size availability rule, not an independent-replication rule. We will therefore retain the implemented rule unless we formally revise it, but we will also report the number of contributing studies for every level. We will mark levels represented by fewer than three studies as sparsely replicated, avoid strong level-specific conclusions, and consider placing their pairwise contrasts in the supplementary tables. This reporting rule does not hide or remove results.

### Small-study effects and sensitivity analyses

We inspected a funnel plot of lnRR against inverse standard error. Because lnRR and its sampling variance are mathematically linked, we tested small-study patterns with an N-based precision term, √(1/N_T + 1/N_C), rather than the standard error. We fitted this term as a moderator in the multilevel model. We also fitted mean-centred publication year and the N-based precision term together to evaluate a time-lag pattern while accounting for effective sample size. We treated both diagnostics as exploratory because the effect sizes were heterogeneous and dependent.

We removed each study in turn, reconstructed the sampling variance-covariance matrix, and refitted the overall lnRR model. Four studies from the Abramova laboratory contributed 98 of 187 lnRR effect sizes, so we also excluded these studies together and refitted the model. Finally, we excluded the two exact-zero-corrected effect sizes and refitted the model.

### Critical appraisal

We adapted CRIME-Q to appraise quality of reporting, methodological quality, and risk of bias in whole-animal behavioural experiments. The final codebook contained 21 items with prespecified response categories (`Yes`, `Partly`, `No`, `Unclear`, or `Not applicable`, as allowed for each item). We retained item-level ratings and did not calculate a composite score. [ADD who completed the first appraisal, who independently checked each study, how disagreements were resolved, Cohen's kappa and item-level disagreement rates if these planned steps were completed. Do not claim two-person independent appraisal until confirmed.] We display the final item-by-study ratings as a coloured grid.

### Software and reproducibility

We conducted data processing, analysis, and visualization in R. The current rendered book used R 4.5.1, `metafor` 5.0-1, `orchaRd` 2.2.1, `ggplot2` 4.0.3, `multcomp` 1.4-31, and associated tidyverse packages. [Update these versions from the final session information at submission.] The data, code, model summaries, and complete moderator outputs will be available at [ADD repository and archived release/DOI].

## Main-figure plan

Renumber consecutively. The current list skips Figure 6; the clean sequence below uses Figures 1-8.

### Figure 1 — Study and exposure coverage

- **Panel A: Study subjects.** Study-level alluvial plot: outcome coverage → species → strain; ribbon colour = sex coverage.
- **Panel B: Noise exposure.** Study-level alluvial plot: gestational-stage coverage → exposure type → author-reported noise type; ribbon colour = control condition.
- Keep each study's total width equal to one. Do not weight the alluvial plots by number of effect sizes.

### Figure 2 — Overall effects

- **Panel A:** lnRR overall orchard plot, *k* = 187 (16 studies).
- **Panel B:** lnVR overall orchard plot, *k* = 175 (14 studies).
- Use matched design, show 95% confidence and prediction intervals, and define direction on each axis.

### Figure 3 — Outcome type

- **Panel A:** Anxiety and depression lnRR, with *k* and study counts.
- **Panel B:** Anxiety and depression lnVR, with *k* and study counts.
- Keep because outcome type is central to the protocol and the lnRR contrast is one of the clearest current findings.

### Figure 4 — Protocol-focused lnRR moderators

Recommended seven-panel dashboard, ordered by the research questions rather than p-value:

- **A:** offspring sex;
- **B:** offspring age at testing (continuous);
- **C:** gestational timing;
- **D:** exposure duration in days (continuous);
- **E:** noise frequency range;
- **F:** loudness in unweighted dB (continuous);
- **G:** behavioural assay.

This is a large figure, but it answers the registered biological and methodological questions without selecting only positive results. Use a 2 × 4 layout with Panel G spanning the final two columns. If the journal makes the panel text unreadable, retain A, B, D, E, F, and G in the main figure and move gestational timing to Figure S3.

### Figure 5 — Protocol-focused lnVR moderators

Use the same seven moderators, panel order, scales where defensible, and colours as Figure 4. The matched structure lets readers compare whether each moderator relates to means, variability, both, or neither. The loudness panel is currently the strongest lnVR association, but it should appear because intensity was specified in the protocol, not because its p-value is small.

### Figure 6 — Small-study and time-lag patterns

- **Panel A:** lnRR against √(1/N_T + 1/N_C), with the multilevel regression line.
- **Panel B:** lnRR against publication year, adjusted for the precision term.
- Place the residual funnel plot in Appendix III/Figure S6 unless the target journal expects it in the main paper.

### Figure 7 — CRIME-Q

- Study × item heatmap for all 16 studies and 21 items.
- Group items visually into reporting, methodological quality, and risk-of-bias domains.
- Provide item definitions in Appendix III, Table S11 rather than overloading the legend.

### Figure 8 — Abramova-laboratory sensitivity analysis

- **Panel A:** overall lnRR with all studies.
- **Panel B:** overall lnRR after excluding all four Abramova-laboratory studies.
- Use identical axes and show *k* and study counts. Explain that this is a laboratory-cluster sensitivity analysis, not a conventional leave-one-out analysis.

## Online supplementary HTML structure

### Appendix I — Sensitivity analyses

Use the current sensitivity-analysis chapter for:

- the combined Abramova-laboratory exclusion;
- the exact-zero-correction exclusion;
- the ρ-sensitivity analysis, if added.

The main manuscript can still reproduce the Abramova comparison as Figure 8 because it addresses the unusually large contribution from one laboratory.

### Appendix II — Main figures

Expand the current alluvial-plot chapter into a main-figures chapter containing Figures 1-8 in final order. Each figure should have its own subsection so that its title appears in the **On this page** index.

### Appendix III — Supplementary figures and tables

#### Supplementary figures

Corrected numbering:

- **Figure S1 — PRISMA flow diagram.**
- **Figure S2 — Screening decision tree.**
- **Figure S3 — Additional/exploratory lnRR uni-moderators.** Exposure type and control conditions; include gestational timing here only if it cannot fit in Figure 4.
- **Figure S4 — Additional/exploratory lnVR uni-moderators.** Exposure type and control conditions; include gestational timing here only if it cannot fit in Figure 5.
- **Figure S5 — Study-level leave-one-out orchard plot.**
- **Figure S6 — Residual funnel plot.** Retain if it is not included with the main publication-bias figure.
- **Figure S7 — Exact-zero-correction sensitivity comparison.**
- **Figure S8 — Overall lnCVR and complete lnCVR moderator dashboard.**

#### Supplementary tables

Create a separate QMD for the tables. Give every table an informative heading, not only a number, so the heading appears in the **On this page** index. Set `toc: true` and `toc-depth: 3` if tables are nested under an Appendix III heading.

- **Table S1 — Search strategy: database-specific search strings, search dates, and records retrieved.**
- **Table S2 — Excluded studies: full-text reports and one primary exclusion reason.**
- **Table S3 — Included studies: bibliographic and study characteristics, including publication language.**
- **Table S4 — Updated codebook: variable roles, definitions, units, allowed values, and authority.**
- **Table S5 — Index of data and resources: main extraction data, derived datasets, analysis books, GitHub links, and a short description of how to use each resource.** This content can also supply the GitHub README and the first page of the analysis HTML.
- **Table S6 — Overall meta-analytic results and multilevel heterogeneity.**
- **Table S7 — Complete lnRR uni-moderator results.** Include every model and level, *k*, contributing-study count, estimates, intervals, omnibus tests, and R².
- **Table S8 — Complete lnVR uni-moderator results.** Use the same columns and order as Table S7.
- **Table S9 — Complete lnCVR supplementary results.**
- **Table S10 — Pairwise moderator contrasts.** Label them as unadjusted exploratory contrasts.
- **Table S11 — CRIME-Q item definitions and reviewer agreement.** Include Cohen's kappa and item-level disagreement rates if available.

Appendix III should also document the effect-size equations, boundary-correction rules and affected IDs, VCV construction and ρ assumption, complete CRIME-Q codebook, session information, software versions, repository URL, and archived release/DOI. These can be short notes linked to the relevant figures or tables rather than additional numbered tables.

## Decisions and checks before converting this outline into a manuscript

- Add the OSF registration link/identifier and final search dates.
- Confirm that 100% of data extraction was independently cross-checked.
- Confirm the CRIME-Q appraisal workflow and calculate the planned Cohen's kappa/disagreement rates, or describe the workflow that was actually completed.
- Complete the agreed deviations-and-additions entry for lnVR and lnCVR, including its decision date and rationale. Check whether the ten unreported-outcome exclusions, exposure type, and control-condition moderator decisions also require entries.
- Preserve `gest_stage_ex` as the registered extracted/reported codebook field. Keep `gest_stage_ex_standardised` explicitly identified as a derived analysis variable unless the team later approves a different name; do not call the derived variable the protocol codebook variable.
- Confirm that the final dataset remains 187 lnRR effects from 16 studies and 175 lnVR effects from 14 studies.
- Add numbers of independent studies to every moderator level. The current *k* ≥ 5 rule alone can retain levels represented by only one or two studies.
- Before changing the analysis, decide whether to add a formal minimum-study rule. My default recommendation is to retain the current models, label levels with fewer than three studies as sparsely replicated, and avoid strong pairwise inference from those levels.
- Add a sensitivity analysis across plausible shared-outcome correlations (for example ρ = 0, 0.3, 0.5, 0.7, and 0.9) if feasible.
- Correct the figure sequence from 1-5, 7-9 to 1-8.
- Update software versions and numerical results only after the final render.

## PRISMA production note

The existing PRISMA figure was not created in R. It was generated programmatically as an editable SVG and as a vector PDF with Python (`build_prisma_svg.py` and ReportLab). The counts are stored in `outputs/prisma/PCN_PRISMA_screening_counts.docx`. The SVG is the easiest source to revise while preserving sharp text and lines.
