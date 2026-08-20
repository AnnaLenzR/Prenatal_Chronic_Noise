import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = "/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise";
const outDir = `${root}/outputs/019ff719-4f39-7b31-8dee-189f2b3ff628`;
const previewDir = `${root}/tmp/design_block1/previews`;

const decisionCsv = await fs.readFile(`${root}/Data/audits/decision_register_v5_block1.csv`, "utf8");
const designCsv = await fs.readFile(`${root}/Data/audits/design_dependence_register_v5_block1.csv`, "utf8");
const correctionCsv = await fs.readFile(`${root}/Data/audits/correction_log_v5_block1.csv`, "utf8");

const workbook = await Workbook.fromCSV(decisionCsv, { sheetName: "Decisions" });
await workbook.fromCSV(designCsv, { sheetName: "Design Register" });
await workbook.fromCSV(correctionCsv, { sheetName: "Correction Log" });

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:F1").merge();
summary.getRange("A1").values = [["PCN Block 1 - Arm Design and Dependence Decisions"]];
summary.getRange("A1:F1").format = {
  fill: "#173F5F",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  verticalAlignment: "center",
};
summary.getRange("A1:F1").format.rowHeight = 30;

summary.getRange("A3:B7").values = [
  ["Audit metric", "Count"],
  ["Approved decisions", null],
  ["Approved design rows", null],
  ["Oliveira design rows", null],
  ["Whitlow corrected rows", null],
];
summary.getRange("B4").formulas = [["=COUNTIF('Decisions'!$D$2:$D$5,\"Approved\")"]];
summary.getRange("B5").formulas = [["=COUNTIF('Design Register'!$P$2:$P$43,\"Approved\")"]];
summary.getRange("B6").formulas = [["=COUNTIF('Design Register'!$A$2:$A$43,\"oliveira_2015_jbehavbraisci\")"]];
summary.getRange("B7").formulas = [["=COUNTA('Correction Log'!$C$2:$C$37)"]];
summary.getRange("A3:B3").format = {
  fill: "#2A7F9E",
  font: { bold: true, color: "#FFFFFF" },
  borders: { preset: "outside", style: "thin", color: "#2A7F9E" },
};
summary.getRange("A4:B7").format = {
  fill: "#EAF3F6",
  borders: { preset: "inside", style: "thin", color: "#C7DCE4" },
};
summary.getRange("B4:B7").format.numberFormat = "0";

summary.getRange("A9:F9").merge();
summary.getRange("A9").values = [["Approved analysis rules"]];
summary.getRange("A9:F9").format = {
  fill: "#D7A84B",
  font: { bold: true, color: "#1F2937" },
};
summary.getRange("A10:F14").merge(true);
summary.getRange("A10:F14").values = [
  ["Oliveira and Whitlow use independent-arm lnRR calculations."],
  ["Effect sizes remain dependent within study and within behavioural-test clusters."],
  ["Shared controls, shared experimental groups, repeated measures, and multiple outcomes are recorded separately."],
  ["Use the authors' reported pup/offspring sample size; do not substitute unavailable dam counts."],
  ["Whitlow offspring_sex is corrected from male to mixed in all 36 rows."],
];
summary.getRange("A10:F14").format = {
  fill: "#FFF8E7",
  wrapText: true,
  verticalAlignment: "center",
};
summary.getRange("A10:F14").format.rowHeight = 28;
summary.getRange("A16:F18").merge();
summary.getRange("A16").values = [[
  "Litter clustering is documented as a general limitation: pups from the same dam may be more similar, but dam/litter counts are not consistently reported and are not used as model inputs."
]];
summary.getRange("A16:F18").format = {
  fill: "#F3F4F6",
  font: { italic: true, color: "#374151" },
  wrapText: true,
  verticalAlignment: "center",
  borders: { preset: "outside", style: "thin", color: "#CBD5E1" },
};
summary.getRange("A:A").format.columnWidth = 34;
summary.getRange("B:B").format.columnWidth = 12;
summary.getRange("C:F").format.columnWidth = 18;

function styleDataSheet(sheetName, tableName, lastCell, widths) {
  const sheet = workbook.worksheets.getItem(sheetName);
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  const used = sheet.getRange(`A1:${lastCell}`);
  used.format.wrapText = true;
  used.format.verticalAlignment = "top";
  sheet.getRange(`A1:${lastCell.replace(/[0-9]/g, "")}1`).format = {
    fill: "#173F5F",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${lastCell.replace(/[0-9]/g, "")}1`).format.rowHeight = 32;
  const table = sheet.tables.add(`A1:${lastCell}`, true, tableName);
  table.style = "TableStyleMedium2";
  for (const [col, width] of Object.entries(widths)) {
    sheet.getRange(`${col}:${col}`).format.columnWidth = width;
  }
  used.format.autofitRows();
}

styleDataSheet("Decisions", "DecisionTable", "G5", {
  A: 12, B: 28, C: 30, D: 18, E: 58, F: 58, G: 54,
});
styleDataSheet("Design Register", "DesignRegisterTable", "R43", {
  A: 30, B: 10, C: 12, D: 16, E: 30, F: 36, G: 34, H: 34,
  I: 17, J: 20, K: 19, L: 25, M: 28, N: 22, O: 68, P: 16, Q: 15, R: 62,
});
styleDataSheet("Correction Log", "CorrectionLogTable", "J37", {
  A: 34, B: 28, C: 10, D: 14, E: 18, F: 14, G: 14, H: 24, I: 68, J: 64,
});

const summaryCheck = await workbook.inspect({
  kind: "table",
  sheetId: "Summary",
  range: "A1:F18",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 8,
});
console.log(summaryCheck.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

await fs.mkdir(outDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });
for (const sheetName of ["Summary", "Decisions", "Design Register", "Correction Log"]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const safeName = sheetName.toLowerCase().replaceAll(" ", "_");
  await fs.writeFile(`${previewDir}/${safeName}.png`, new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outDir}/PCN_block1_design_decisions.xlsx`);
