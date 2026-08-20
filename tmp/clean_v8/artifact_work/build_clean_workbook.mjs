import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = "/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise";
const outDir = `${root}/outputs/019ff719-4f39-7b31-8dee-189f2b3ff628`;
const previewDir = `${root}/tmp/clean_v8/previews`;

const cleanCsv = await fs.readFile(`${root}/Data/PCN_data_ext_checking_v.8_clean.csv`, "utf8");
const removedCsv = await fs.readFile(`${root}/Data/audits/column_cleanup_register_v8.csv`, "utf8");
const renamedCsv = await fs.readFile(`${root}/Data/audits/column_rename_register_v8.csv`, "utf8");

const workbook = await Workbook.fromCSV(cleanCsv, { sheetName: "Clean Data" });
await workbook.fromCSV(removedCsv, { sheetName: "Removed Columns" });
await workbook.fromCSV(renamedCsv, { sheetName: "Renamed Columns" });

const summary = workbook.worksheets.add("README");
summary.showGridLines = false;
summary.getRange("A1:F1").merge();
summary.getRange("A1").values = [["PCN v8 - Clean Cross-Checked Extraction Sheet"]];
summary.getRange("A1:F1").format = {
  fill: "#173F5F",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  verticalAlignment: "center",
};
summary.getRange("A1:F1").format.rowHeight = 30;

summary.getRange("A3:B8").values = [
  ["Workbook metric", "Count"],
  ["Effect-size rows", null],
  ["Clean-data columns", null],
  ["Columns removed from main sheet", null],
  ["Columns renamed for clarity", null],
  ["Retained values changed", 0],
];
summary.getRange("B4").formulas = [["=COUNTA('Clean Data'!$B$2:$B$208)"]];
summary.getRange("B5").formulas = [["=COUNTA('Clean Data'!$A$1:$BS$1)"]];
summary.getRange("B6").formulas = [["=COUNTA('Removed Columns'!$A$2:$A$14)"]];
summary.getRange("B7").formulas = [["=COUNTA('Renamed Columns'!$A$2:$A$4)"]];
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
summary.getRange("A10").values = [["What the clean sheet retains"]];
summary.getRange("A10:F10").format = {
  fill: "#D7A84B",
  font: { bold: true, color: "#1F2937" },
};
summary.getRange("A11:F15").merge(true);
summary.getRange("A11:F15").values = [
  ["All 207 effect-size rows and all retained reported values from v7."],
  ["Stable study, group, outcome, source, exposure, offspring, and behavioural-test fields."],
  ["The approved data_status flag: Verified, corrected transcription, corrected derived value, or analysis decision required."],
  ["Separate reported, analysis, derivation, and source fields for control and experimental SE."],
  ["The original v7 file and audit files remain the recovery source for every column removed from this main sheet."],
];
summary.getRange("A11:F15").format = {
  fill: "#FFF8E7",
  wrapText: true,
  verticalAlignment: "center",
};
summary.getRange("A11:F15").format.rowHeight = 28;

summary.getRange("A17:F17").merge();
summary.getRange("A17").values = [["Column organization"]];
summary.getRange("A17:F17").format = {
  fill: "#6B7280",
  font: { bold: true, color: "#FFFFFF" },
};
summary.getRange("A18:F23").values = [
  ["A-I", "Identifiers and review status", null, null, null, null],
  ["J-S", "Citation and biological context", null, null, null, null],
  ["T-AH", "Exposure, control, offspring and procedures", null, null, null, null],
  ["AI-AW", "Outcome, source, comparison and direction", null, null, null, null],
  ["AX-BQ", "Control and experimental statistics with provenance", null, null, null, null],
  ["BR-BS", "Remaining source comments", null, null, null, null],
];
summary.getRange("A18:F23").format = {
  fill: "#F3F4F6",
  wrapText: true,
  verticalAlignment: "center",
};
summary.getRange("A:A").format.columnWidth = 24;
summary.getRange("B:B").format.columnWidth = 36;
summary.getRange("C:F").format.columnWidth = 16;

const clean = workbook.worksheets.getItem("Clean Data");
clean.showGridLines = false;
clean.freezePanes.freezeRows(1);
clean.freezePanes.freezeColumns(6);
const cleanUsed = clean.getRange("A1:BS208");
cleanUsed.format.verticalAlignment = "top";
cleanUsed.format.wrapText = false;

const cleanTable = clean.tables.add("A1:BS208", true, "PCNCleanDataV8");
cleanTable.style = "TableStyleMedium2";
clean.getRange("A1:I1").format = { fill: "#173F5F", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
clean.getRange("J1:S1").format = { fill: "#2A7F9E", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
clean.getRange("T1:AH1").format = { fill: "#4F7C6A", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
clean.getRange("AI1:AW1").format = { fill: "#725A7A", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
clean.getRange("AX1:BQ1").format = { fill: "#9A6A2F", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
clean.getRange("BR1:BS1").format = { fill: "#6B7280", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
clean.getRange("A1:BS1").format.rowHeight = 40;

const widths = {
  A: 32, B: 10, C: 10, D: 10, E: 10, F: 16, G: 28, H: 34, I: 30,
  J: 48, K: 24, L: 28, M: 20, N: 16, O: 18, P: 12, Q: 32, R: 18, S: 40,
  T: 15, U: 20, V: 20, W: 40, X: 18, Y: 18, Z: 14, AA: 16, AB: 30, AC: 40,
  AD: 16, AE: 18, AF: 34, AG: 28, AH: 44,
  AI: 16, AJ: 28, AK: 36, AL: 36, AM: 14, AN: 14, AO: 18, AP: 42, AQ: 42,
  AR: 14, AS: 14, AT: 30, AU: 15, AV: 22, AW: 42,
  AX: 12, AY: 12, AZ: 10, BA: 16, BB: 16, BC: 30, BD: 44, BE: 12, BF: 12, BG: 12,
  BH: 12, BI: 12, BJ: 10, BK: 16, BL: 16, BM: 30, BN: 44, BO: 12, BP: 12, BQ: 12,
  BR: 42, BS: 42,
};
for (const [column, width] of Object.entries(widths)) {
  clean.getRange(`${column}:${column}`).format.columnWidth = width;
}

clean.getRange("G2:G208").conditionalFormats.add("containsText", {
  text: "Verified",
  format: { fill: "#DCFCE7", font: { color: "#166534" } },
});
clean.getRange("G2:G208").conditionalFormats.add("containsText", {
  text: "Corrected",
  format: { fill: "#DBEAFE", font: { color: "#1D4ED8" } },
});
clean.getRange("G2:G208").conditionalFormats.add("containsText", {
  text: "Analysis decision required",
  format: { fill: "#FEF3C7", font: { color: "#92400E" } },
});

function styleAuditSheet(sheetName, tableName, lastCell, widthsByCol) {
  const sheet = workbook.worksheets.getItem(sheetName);
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  const lastCol = lastCell.replace(/[0-9]/g, "");
  const range = sheet.getRange(`A1:${lastCell}`);
  range.format.wrapText = true;
  range.format.verticalAlignment = "top";
  sheet.getRange(`A1:${lastCol}1`).format = {
    fill: "#173F5F",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${lastCol}1`).format.rowHeight = 34;
  const table = sheet.tables.add(`A1:${lastCell}`, true, tableName);
  table.style = "TableStyleMedium2";
  for (const [column, width] of Object.entries(widthsByCol)) {
    sheet.getRange(`${column}:${column}`).format.columnWidth = width;
  }
  range.format.autofitRows();
}

styleAuditSheet("Removed Columns", "RemovedColumnsV8", "E14", {
  A: 30, B: 84, C: 18, D: 58, E: 15,
});
styleAuditSheet("Renamed Columns", "RenamedColumnsV8", "D4", {
  A: 30, B: 30, C: 76, D: 15,
});

const readmeCheck = await workbook.inspect({
  kind: "table",
  sheetId: "README",
  range: "A1:F23",
  include: "values,formulas",
  tableMaxRows: 26,
  tableMaxCols: 8,
});
console.log(readmeCheck.ndjson);

const cleanCheck = await workbook.inspect({
  kind: "table",
  sheetId: "Clean Data",
  range: "A1:I8",
  include: "values",
  tableMaxRows: 10,
  tableMaxCols: 12,
});
console.log(cleanCheck.ndjson);

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
  ["README", "A1:F23", "readme"],
  ["Clean Data", "A1:S12", "clean_ids_context"],
  ["Clean Data", "T1:AW12", "clean_exposure_outcomes"],
  ["Clean Data", "AX1:BS12", "clean_statistics"],
  ["Clean Data", "AX197:BS208", "clean_statistics_bottom"],
  ["Removed Columns", "A1:E14", "removed_columns"],
  ["Renamed Columns", "A1:D4", "renamed_columns"],
];

for (const [sheetName, range, fileName] of previewSpecs) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(`${previewDir}/${fileName}.png`, new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outDir}/PCN_data_ext_checking_v8_clean.xlsx`);
