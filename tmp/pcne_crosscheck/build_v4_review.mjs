import fs from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const root = "/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise";
const auditDir = `${root}/Data/audits`;
const tmp = `${root}/tmp/pcne_crosscheck`;
const outDir = `${root}/output/crosscheck_report`;
const outPath = `${outDir}/PCN_data_crosscheck_v4_review.xlsx`;

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ",") { row.push(field); field = ""; }
    else if (ch === "\n") { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
    else field += ch;
  }
  if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }
  return rows.filter((r) => r.some((v) => v !== ""));
}

async function readCsv(path) { return parseCsv(await fs.readFile(path, "utf8")); }

function excelColumn(n) {
  let s = "";
  while (n > 0) { n--; s = String.fromCharCode(65 + (n % 26)) + s; n = Math.floor(n / 26); }
  return s;
}

function setWidths(sheet, widths) {
  widths.forEach((width, i) => { sheet.getRange(`${excelColumn(i + 1)}:${excelColumn(i + 1)}`).format.columnWidth = width; });
}

function addStatusFormatting(sheet, range) {
  const r = sheet.getRange(range);
  r.conditionalFormats.add("containsText", { text: "Verified", format: { fill: "#E6F4EA", font: { color: "#1F6F43", bold: true } } });
  r.conditionalFormats.add("containsText", { text: "Corrected transcription", format: { fill: "#DDEBF7", font: { color: "#174A70", bold: true } } });
  r.conditionalFormats.add("containsText", { text: "Corrected derived value", format: { fill: "#E8E1F5", font: { color: "#5B3B82", bold: true } } });
  r.conditionalFormats.add("containsText", { text: "Analysis decision required", format: { fill: "#FFF0CC", font: { color: "#7A4B00", bold: true } } });
  r.conditionalFormats.add("containsText", { text: "Source needed", format: { fill: "#FDE2E1", font: { color: "#9C1C13", bold: true } } });
}

function addTableSheet(wb, name, rows, widths, tableName, statusColumn = null) {
  const sheet = wb.worksheets.add(name);
  sheet.showGridLines = false;
  const nRows = rows.length;
  const nCols = rows[0].length;
  const end = `${excelColumn(nCols)}${nRows}`;
  sheet.getRange(`A1:${end}`).values = rows;
  sheet.getRange(`A1:${end}`).format = { font: { name: "Aptos", fontSize: 9, color: "#172033" }, verticalAlignment: "top" };
  sheet.getRange(`A1:${excelColumn(nCols)}1`).format = {
    fill: "#15324B", font: { name: "Aptos", fontSize: 9, bold: true, color: "#FFFFFF" },
    verticalAlignment: "center", wrapText: true, rowHeight: 34,
  };
  if (nRows > 1) {
    sheet.getRange(`A2:${end}`).format.wrapText = true;
    sheet.getRange(`A2:${end}`).format.borders = { insideHorizontal: { style: "thin", color: "#DCE4EA" } };
  }
  setWidths(sheet, widths);
  sheet.freezePanes.freezeRows(1);
  sheet.tables.add(`A1:${end}`, true, tableName).style = "TableStyleMedium2";
  if (statusColumn) addStatusFormatting(sheet, `${statusColumn}2:${statusColumn}${nRows}`);
  return sheet;
}

const correctedData = await readCsv(`${root}/Data/PCN_data_ext_checking_v.4_crosschecked.csv`);
const corrections = await readCsv(`${auditDir}/correction_log_v4.csv`);
const rowStatus = await readCsv(`${auditDir}/row_review_status_v4.csv`);
const decisions = await readCsv(`${auditDir}/decision_register_v4.csv`);
const wranglingPlan = await readCsv(`${auditDir}/data_wrangling_plan_v4.csv`);
const summary = JSON.parse(await fs.readFile(`${tmp}/v4_summary.json`, "utf8"));

const packages = [
  ["1 – Uygur 2011 outcome units", "uygur_2011_ankarauniv", "4", "Diving and jumping recoded as time in seconds", "No", "Review the four rows, then accept or reject this package as a unit."],
  ["2 – Uygur 2010 exposure and sample sizes", "uygur_2010_aphyhun", "3", "45 min converted to 0.75 h; control/exposed n corrected to 10/9", "No", "Review Methods and Table II evidence."],
  ["3 – Arjunan 2023 acoustic exposure", "arjunan_2023_stress", "6", "White/broadband noise, 0–20,000 Hz; source filenames repaired", "No", "Review the exposure classification before moderator coding."],
  ["4 – Barzegar 2014 title and SEM", "barzegar_2014_hippo", "6", "Copied title and figure paths repaired; es006 SEM separated from SD", "No", "Check es006 first; the analysis SEM is 2.666667 while the legacy c/ex SE fields remain preserved."],
  ["5 – Abramova 2020 derived SEs", "abramova_2020_genpath", "34", "SE recalculated as SD/sqrt(n); es162 source SD repaired", "No", "Author/raw inputs are preserved; only deterministic derived values change."],
  ["6 – Abramova 2021 same-sex controls", "abramova_2021_front", "14", "Controls recalculated from the author raw subgroup matching offspring sex; center-time units repaired", "No", "Review the female and male rows in pairs; exposed summaries were already correct."],
  ["7 – Abramova 2023 identifiers and units", "abramova_2023_biopsy", "44", "Sex-coded IDs, source path, and grooming-duration units repaired", "18 rows deferred to R", "Transcription repairs are applied; median/IQR estimates will be generated reproducibly during R data wrangling."],
];

const wb = Workbook.create();
const start = wb.worksheets.add("START HERE");
start.showGridLines = false;
start.mergeCells("A1:H1");
start.getRange("A1").values = [["PCN cross-check: seven correction packages"]];
start.getRange("A1:H1").format = { fill: "#15324B", font: { name: "Aptos Display", fontSize: 20, bold: true, color: "#FFFFFF" }, rowHeight: 42 };
start.mergeCells("A2:H2");
start.getRange("A2").values = [["Protected v4 review workbook — reported author values are separated from analysis-ready SEs"]];
start.getRange("A2:H2").format = { fill: "#E8F0F4", font: { name: "Aptos", fontSize: 11, italic: true, color: "#35556D" }, rowHeight: 28 };

start.getRange("A4:B10").values = [
  ["Original preserved", `Data/PCN_data_ext_checking_v.3.csv; SHA-256 ${summary.source_sha256}`],
  ["New data file", "Data/PCN_data_ext_checking_v.4_crosschecked.csv"],
  ["Use for analysis", "Use c_se_analysis and ex_se_analysis. Do not use the legacy c_se/ex_se columns for new analysis."],
  ["Reported values", "c_se_reported/ex_se_reported contain only SEMs reported by the paper or digitised as reported SEM."],
  ["Derived values", "c_se_analysis/ex_se_analysis may equal a reported SEM or be calculated as SD/sqrt(n); the derivation and source are adjacent."],
  ["R wrangling later", "Do not estimate missing central tendencies here. Abramova median/IQR conversions are deferred to auditable R code for IRR/analysis preparation."],
  ["Accepted assumption", "Whitlow 1978 uses SD=sqrt(mean), then SE=SD/sqrt(n). These values are labelled as analysis assumptions, never author-reported variance."],
];
start.getRange("A4:A10").format = { fill: "#D9E8EF", font: { bold: true, color: "#15324B" }, wrapText: true, verticalAlignment: "top" };
start.getRange("B4:B10").format = { wrapText: true, verticalAlignment: "top" };
start.getRange("A4:B10").format.borders = { insideHorizontal: { style: "thin", color: "#CAD6DE" }, outside: { style: "thin", color: "#9DB1BE" } };

start.getRange("D4:F4").merge();
start.getRange("D4").values = [["Row status summary"]];
start.getRange("D4:F4").format = { fill: "#D9E8EF", font: { bold: true, color: "#15324B" } };
const statuses = ["Verified – no change", "Corrected transcription", "Corrected derived value", "Analysis decision required", "Source needed"];
start.getRange("D5:D9").values = statuses.map((s) => [s]);
start.getRange("E5:E9").values = statuses.map(() => [""]);
start.getRange("F5:F9").values = [["Ready"], ["Applied"], ["Applied"], ["Decide later"], ["Obtain source"]];
start.getRange("D5:F9").format = { wrapText: true, borders: { insideHorizontal: { style: "thin", color: "#DCE4EA" }, outside: { style: "thin", color: "#9DB1BE" } } };
start.getRange("E5:E9").format = { font: { bold: true, fontSize: 14, color: "#15324B" }, horizontalAlignment: "center" };
addStatusFormatting(start, "D5:D9");

start.getRange("A12:H12").merge();
start.getRange("A12").values = [["SE field guide"]];
start.getRange("A12:H12").format = { fill: "#15324B", font: { bold: true, color: "#FFFFFF" }, rowHeight: 25 };
start.getRange("A13:D18").values = [
  ["Field", "Meaning", "May be blank?", "Rule"],
  ["c_se_reported / ex_se_reported", "SEM explicitly reported by authors or digitised from a figure labelled as SEM", "Yes", "Never calculate a value into this field."],
  ["c_se_analysis / ex_se_analysis", "SE selected for meta-analysis", "Yes", "Use reported SEM unchanged, or derive from verified SD and n."],
  ["c_se_derivation / ex_se_derivation", "How the analysis SE was obtained", "No", "Formula or reason for leaving the SE blank."],
  ["c_se_source / ex_se_source", "Paper, figure, workbook, or raw-data source", "No", "Keep enough detail to trace the value."],
  ["legacy c_se / ex_se", "The original v3 extraction values", "Yes", "Preserved for provenance; not the analysis field."],
];
start.getRange("A13:D13").format = { fill: "#D9E8EF", font: { bold: true, color: "#15324B" } };
start.getRange("A13:D18").format = { wrapText: true, verticalAlignment: "top", borders: { insideHorizontal: { style: "thin", color: "#DCE4EA" }, outside: { style: "thin", color: "#9DB1BE" } } };
setWidths(start, [32, 83, 18, 55, 14, 20, 14, 14]);
start.freezePanes.freezeRows(2);

const queueRows = [["package", "study_id", "rows", "what is contained", "open analysis decisions", "how to review"], ...packages];
const queue = addTableSheet(wb, "Package queue", queueRows, [43, 30, 10, 70, 24, 62], "PackageQueueTable");

const statusSheet = addTableSheet(wb, "Row status", rowStatus, [12, 28, 11, 13, 38, 28, 42, 75, 15, 15, 55, 65, 15, 15, 55, 65], "RowStatusTable", "F");
const seSheet = addTableSheet(wb, "SE review", rowStatus, [12, 28, 11, 13, 38, 28, 42, 75, 15, 15, 55, 65, 15, 15, 55, 65], "SEReviewTable", "F");
start.getRange("E5:E9").formulas = statuses.map((s) => [`=COUNTIF('Row status'!F2:F208,\"${s}\")`]);
const correctionSheet = addTableSheet(wb, "Correction log", corrections, [43, 28, 11, 12, 28, 25, 25, 28, 70, 80], "CorrectionLogTable", "H");
const decisionSheet = addTableSheet(wb, "Decision register", decisions, [43, 28, 11, 12, 28, 65, 65, 80, 70], "DecisionRegisterTable", "E");
const wranglingSheet = addTableSheet(wb, "Wrangling plan", wranglingPlan, [44, 54, 28, 70, 46, 80, 72], "WranglingPlanTable", "C");

const packageMap = [
  ["P1 Uygur 2011", packages[0][0]], ["P2 Uygur 2010", packages[1][0]], ["P3 Arjunan 2023", packages[2][0]],
  ["P4 Barzegar 2014", packages[3][0]], ["P5 Abramova 2020", packages[4][0]], ["P6 Abramova 2021", packages[5][0]],
  ["P7 Abramova 2023", packages[6][0]],
  ["Whitlow assumption", "Variance decision – Whitlow 1978"],
  ["Abramova 2024 source", "Source follow-up – Abramova 2024"],
];
for (const [sheetName, packageName] of packageMap) {
  const rows = [corrections[0], ...corrections.slice(1).filter((r) => r[0] === packageName)];
  addTableSheet(wb, sheetName, rows, [43, 28, 11, 12, 28, 25, 25, 28, 70, 80], `${sheetName.replaceAll(" ", "")}Table`, "H");
}

const dataWidths = correctedData[0].map((header) => {
  if (["title", "crosscheck_notes", "c_se_derivation", "ex_se_derivation", "c_se_source", "ex_se_source"].includes(header)) return 55;
  if (["study_id", "crosscheck_status", "crosscheck_package", "measurement_variable"].includes(header)) return 28;
  if (["stat_comment", "general_comment", "corrections_notes_AL"].includes(header)) return 42;
  return 14;
});
const correctedStatusColumn = excelColumn(correctedData[0].indexOf("crosscheck_status") + 1);
const dataSheet = addTableSheet(wb, "Corrected data", correctedData, dataWidths, "CorrectedDataTable", correctedStatusColumn);
dataSheet.freezePanes.freezeColumns(5);

await fs.mkdir(outDir, { recursive: true });
const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(outPath);

const checks = [];
checks.push((await wb.inspect({ kind: "table", range: "START HERE!A1:H18", include: "values,formulas", tableMaxRows: 18, tableMaxCols: 8, maxChars: 9000 })).ndjson);
checks.push((await wb.inspect({ kind: "table", range: "Package queue!A1:F8", include: "values,formulas", tableMaxRows: 8, tableMaxCols: 6, maxChars: 7000 })).ndjson);
checks.push((await wb.inspect({ kind: "table", range: "P5 Abramova 2020!A1:J12", include: "values,formulas", tableMaxRows: 12, tableMaxCols: 10, maxChars: 7000 })).ndjson);
checks.push((await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "formula error scan" })).ndjson);
await fs.writeFile(`${tmp}/v4_workbook_inspection.ndjson`, checks.join("\n"), "utf8");

for (const [sheetName, fileName, range] of [
  ["START HERE", "v4_preview_start.png", "A1:H18"],
  ["Package queue", "v4_preview_queue.png", "A1:F8"],
  ["Row status", "v4_preview_status.png", "A1:P18"],
  ["P5 Abramova 2020", "v4_preview_p5.png", "A1:J16"],
]) {
  const blob = await wb.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(`${tmp}/${fileName}`, new Uint8Array(await blob.arrayBuffer()));
}

console.log(outPath);
