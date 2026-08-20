import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = "/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise";
const outDir = `${root}/outputs/019ff719-4f39-7b31-8dee-189f2b3ff628`;
const previewDir = `${root}/tmp/design_block2/previews`;

const decisionCsv = await fs.readFile(`${root}/Data/audits/decision_register_v6_block2.csv`, "utf8");
const designCsv = await fs.readFile(`${root}/Data/audits/design_dependence_register_v6_block2.csv`, "utf8");
const correctionCsv = await fs.readFile(`${root}/Data/audits/correction_log_v6_block2.csv`, "utf8");

const workbook = await Workbook.fromCSV(decisionCsv, { sheetName: "Decisions" });
await workbook.fromCSV(designCsv, { sheetName: "Design Register" });
await workbook.fromCSV(correctionCsv, { sheetName: "Correction Log" });

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:F1").merge();
summary.getRange("A1").values = [["PCN Block 2 - Approved Design and Dependence Decisions"]];
summary.getRange("A1:F1").format = {
  fill: "#173F5F",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  verticalAlignment: "center",
};
summary.getRange("A1:F1").format.rowHeight = 30;

summary.getRange("A3:B8").values = [
  ["Audit metric", "Count"],
  ["Approved decisions", null],
  ["Block 2 design rows", null],
  ["Uygur rows", null],
  ["Hassanvand rows", null],
  ["Hadizadeh rows", null],
];
summary.getRange("B4").formulas = [["=COUNTIF('Decisions'!$D$2:$D$5,\"Approved\")"]];
summary.getRange("B5").formulas = [["=COUNTIF('Design Register'!$Q$2:$Q$9,\"Approved\")"]];
summary.getRange("B6").formulas = [["=COUNTIF('Design Register'!$A$2:$A$9,\"uygur_2010_aphyhun\")"]];
summary.getRange("B7").formulas = [["=COUNTIF('Design Register'!$A$2:$A$9,\"hassanvand_2012_phyphar\")"]];
summary.getRange("B8").formulas = [["=COUNTIF('Design Register'!$A$2:$A$9,\"hadizadeh_2018_irjbamedsci\")"]];
summary.getRange("A3:B3").format = {
  fill: "#2A7F9E",
  font: { bold: true, color: "#FFFFFF" },
  borders: { preset: "outside", style: "thin", color: "#2A7F9E" },
};
summary.getRange("A4:B8").format = {
  fill: "#EAF3F6",
  borders: { preset: "inside", style: "thin", color: "#C7DCE4" },
};
summary.getRange("B4:B8").format.numberFormat = "0";

summary.getRange("A10:F10").merge();
summary.getRange("A10").values = [["Approved analysis rules"]];
summary.getRange("A10:F10").format = {
  fill: "#D7A84B",
  font: { bold: true, color: "#1F2937" },
};
summary.getRange("A11:F15").merge(true);
summary.getRange("A11:F15").values = [
  ["All three studies use independent treatment and control arms for lnRR calculation."],
  ["Outcomes remain dependent within their study and behavioural-test clusters."],
  ["Each Block 2 row shares both its control and experimental group with another outcome from the same test."],
  ["These are multiple outcomes from one test session, not repeated measurements over time."],
  ["Hadizadeh metadata now correctly records that behavioural testing involved male offspring only; numerical results are unchanged."],
];
summary.getRange("A11:F15").format = {
  fill: "#FFF8E7",
  wrapText: true,
  verticalAlignment: "center",
};
summary.getRange("A11:F15").format.rowHeight = 28;
summary.getRange("A17:F19").merge();
summary.getRange("A17").values = [[
  "This workbook covers 8 of the 207 effect-size rows. The cumulative machine-readable register for Blocks 1-2 contains 50 classified rows; the analysis dataset remains 207 rows."
]];
summary.getRange("A17:F19").format = {
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

styleDataSheet("Decisions", "DecisionTableB2", "F5", {
  A: 12, B: 28, C: 64, D: 16, E: 15, F: 58,
});
styleDataSheet("Design Register", "DesignRegisterTableB2", "S9", {
  A: 32, B: 10, C: 12, D: 16, E: 32, F: 38, G: 36, H: 34, I: 38,
  J: 17, K: 20, L: 19, M: 25, N: 28, O: 22, P: 68, Q: 16, R: 15, S: 70,
});
styleDataSheet("Correction Log", "CorrectionLogTableB2", "J3", {
  A: 34, B: 10, C: 12, D: 18, E: 48, F: 52, G: 24, H: 72, I: 68, J: 15,
});

const summaryCheck = await workbook.inspect({
  kind: "table",
  sheetId: "Summary",
  range: "A1:F19",
  include: "values,formulas",
  tableMaxRows: 22,
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
await output.save(`${outDir}/PCN_block2_design_decisions.xlsx`);
