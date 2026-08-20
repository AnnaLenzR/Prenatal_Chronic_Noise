import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = "/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise";
const outDir = `${root}/outputs/019ff719-4f39-7b31-8dee-189f2b3ff628`;
const previewDir = `${root}/tmp/arm_design_v7/previews`;

const decisionsCsv = await fs.readFile(`${root}/Data/audits/decision_register_v7_arm_design.csv`, "utf8");
const correctionsCsv = await fs.readFile(`${root}/Data/audits/correction_log_v7_all_independent_arms.csv`, "utf8");
const studyCountsCsv = await fs.readFile(`${root}/Data/audits/arm_design_counts_by_study_v7.csv`, "utf8");
const allArmsCsv = await fs.readFile(`${root}/Data/audits/arm_design_register_v7_all_rows.csv`, "utf8");

const workbook = await Workbook.fromCSV(decisionsCsv, { sheetName: "Decisions" });
await workbook.fromCSV(correctionsCsv, { sheetName: "Corrections" });
await workbook.fromCSV(studyCountsCsv, { sheetName: "Study Counts" });
await workbook.fromCSV(allArmsCsv, { sheetName: "All Arms" });

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:F1").merge();
summary.getRange("A1").values = [["PCN v7 - Independent Arm Design Audit"]];
summary.getRange("A1:F1").format = {
  fill: "#173F5F",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  verticalAlignment: "center",
};
summary.getRange("A1:F1").format.rowHeight = 30;

summary.getRange("A3:B9").values = [
  ["Audit metric", "Count"],
  ["Effect-size rows", null],
  ["Independent-arm rows", null],
  ["Corrected legacy labels", null],
  ["Unchanged arm labels", null],
  ["Unique study IDs represented", null],
  ["Reported numeric cells changed", null],
];
summary.getRange("B4").formulas = [["=COUNTA('All Arms'!$B$2:$B$208)"]];
summary.getRange("B5").formulas = [["=COUNTIF('All Arms'!$F$2:$F$208,\"Independent\")"]];
summary.getRange("B6").formulas = [["=COUNTA('Corrections'!$B$2:$B$43)"]];
summary.getRange("B7").formulas = [["=B4-B6"]];
summary.getRange("B8").formulas = [["=COUNTA('Study Counts'!$A$2:$A$17)"]];
summary.getRange("B9").formulas = [["=COUNTIF('Corrections'!$D$2:$D$43,\"<>comparison_structure\")"]];
summary.getRange("A3:B3").format = {
  fill: "#2A7F9E",
  font: { bold: true, color: "#FFFFFF" },
  borders: { preset: "outside", style: "thin", color: "#2A7F9E" },
};
summary.getRange("A4:B9").format = {
  fill: "#EAF3F6",
  borders: { preset: "inside", style: "thin", color: "#C7DCE4" },
};
summary.getRange("B4:B9").format.numberFormat = "0";

summary.getRange("A11:F11").merge();
summary.getRange("A11").values = [["Approved interpretation"]];
summary.getRange("A11:F11").format = {
  fill: "#D7A84B",
  font: { bold: true, color: "#1F2937" },
};
summary.getRange("A12:F16").merge(true);
summary.getRange("A12:F16").values = [
  ["All 207 control and noise-exposed arms contain different animals."],
  ["Individual lnRRs use independent-arm formulas; ROMC and a treatment-control correlation are not used."],
  ["Shared groups, repeated measurements, and multiple outcomes can still make effect sizes statistically dependent."],
  ["Those dependencies will be handled later in the variance-covariance structure using the audited identifiers."],
  ["No central-tendency estimation, zero replacement, minimum-mean rule, or lnRR calculation was performed in this correction step."],
];
summary.getRange("A12:F16").format = {
  fill: "#FFF8E7",
  wrapText: true,
  verticalAlignment: "center",
};
summary.getRange("A12:F16").format.rowHeight = 28;

summary.getRange("A18:F20").merge();
summary.getRange("A18").values = [[
  "Version lineage: v7 was created from v6. Exactly 42 comparison_structure cells changed from Dependent to Independent (6 Oliveira; 36 Whitlow); all reported numeric values were preserved."
]];
summary.getRange("A18:F20").format = {
  fill: "#F3F4F6",
  font: { italic: true, color: "#374151" },
  wrapText: true,
  verticalAlignment: "center",
  borders: { preset: "outside", style: "thin", color: "#CBD5E1" },
};
summary.getRange("A:A").format.columnWidth = 35;
summary.getRange("B:B").format.columnWidth = 14;
summary.getRange("C:F").format.columnWidth = 18;

function styleDataSheet(sheetName, tableName, lastCell, widths) {
  const sheet = workbook.worksheets.getItem(sheetName);
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  const used = sheet.getRange(`A1:${lastCell}`);
  used.format.wrapText = true;
  used.format.verticalAlignment = "top";
  const lastCol = lastCell.replace(/[0-9]/g, "");
  sheet.getRange(`A1:${lastCol}1`).format = {
    fill: "#173F5F",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${lastCol}1`).format.rowHeight = 32;
  const table = sheet.tables.add(`A1:${lastCell}`, true, tableName);
  table.style = "TableStyleMedium2";
  for (const [col, width] of Object.entries(widths)) {
    sheet.getRange(`${col}:${col}`).format.columnWidth = width;
  }
  used.format.autofitRows();
}

styleDataSheet("Decisions", "ArmDecisionTableV7", "F5", {
  A: 12, B: 30, C: 68, D: 16, E: 15, F: 72,
});
styleDataSheet("Corrections", "ArmCorrectionTableV7", "J43", {
  A: 34, B: 10, C: 12, D: 25, E: 16, F: 16, G: 24, H: 82, I: 58, J: 15,
});
styleDataSheet("Study Counts", "ArmStudyCountsTableV7", "C17", {
  A: 36, B: 18, C: 18,
});
styleDataSheet("All Arms", "AllArmDesignsTableV7", "K208", {
  A: 34, B: 10, C: 12, D: 12, E: 12, F: 18, G: 28, H: 42, I: 16, J: 58, K: 15,
});

const summaryCheck = await workbook.inspect({
  kind: "table",
  sheetId: "Summary",
  range: "A1:F20",
  include: "values,formulas",
  tableMaxRows: 24,
  tableMaxCols: 8,
});
console.log(summaryCheck.ndjson);

const correctionCheck = await workbook.inspect({
  kind: "table",
  sheetId: "Corrections",
  range: "A1:J8",
  include: "values",
  tableMaxRows: 10,
  tableMaxCols: 12,
});
console.log(correctionCheck.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

await fs.mkdir(outDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

const previewSpecs = [
  ["Summary", "A1:F20", "summary"],
  ["Decisions", "A1:F5", "decisions"],
  ["Corrections", "A1:J43", "corrections"],
  ["Study Counts", "A1:C17", "study_counts"],
  ["All Arms", "A1:K26", "all_arms_top"],
  ["All Arms", "A184:K208", "all_arms_bottom"],
];

for (const [sheetName, range, fileName] of previewSpecs) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(`${previewDir}/${fileName}.png`, new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outDir}/PCN_v7_independent_arm_audit.xlsx`);
