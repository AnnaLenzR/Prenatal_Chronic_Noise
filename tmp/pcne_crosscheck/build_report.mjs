import fs from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const root = "/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise";
const tmp = `${root}/tmp/pcne_crosscheck`;
const outDir = `${root}/output/crosscheck_report`;
const outPath = `${outDir}/PCN_data_crosscheck_report_v3.xlsx`;

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') {
        field += '"';
        i++;
      } else if (ch === '"') {
        quoted = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ",") {
      row.push(field);
      field = "";
    } else if (ch === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  return rows.filter((r) => r.some((v) => v !== ""));
}

async function readCsv(name) {
  return parseCsv(await fs.readFile(`${tmp}/${name}`, "utf8"));
}

function excelColumn(n) {
  let s = "";
  while (n > 0) {
    n--;
    s = String.fromCharCode(65 + (n % 26)) + s;
    n = Math.floor(n / 26);
  }
  return s;
}

function setWidths(sheet, widths) {
  widths.forEach((width, i) => {
    sheet.getRange(`${excelColumn(i + 1)}:${excelColumn(i + 1)}`).format.columnWidth = width;
  });
}

function writeTableSheet(workbook, name, rows, widths, tableName, freezeRows = 1) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  const nRows = rows.length;
  const nCols = rows[0].length;
  const end = `${excelColumn(nCols)}${nRows}`;
  sheet.getRange(`A1:${end}`).values = rows;
  sheet.getRange(`A1:${end}`).format = {
    font: { name: "Aptos", fontSize: 9, color: "#172033" },
    verticalAlignment: "top",
  };
  sheet.getRange(`A1:${excelColumn(nCols)}1`).format = {
    fill: "#15324B",
    font: { name: "Aptos", fontSize: 9, bold: true, color: "#FFFFFF" },
    verticalAlignment: "center",
    wrapText: true,
    rowHeight: 34,
    borders: { preset: "outside", style: "thin", color: "#15324B" },
  };
  if (nRows > 1) {
    sheet.getRange(`A2:${end}`).format.wrapText = true;
    sheet.getRange(`A2:${end}`).format.borders = {
      insideHorizontal: { style: "thin", color: "#DCE4EA" },
    };
  }
  setWidths(sheet, widths);
  sheet.freezePanes.freezeRows(freezeRows);
  sheet.tables.add(`A1:${end}`, true, tableName).style = "TableStyleMedium2";
  return sheet;
}

const summary = JSON.parse(await fs.readFile(`${tmp}/summary.json`, "utf8"));
const issues = await readCsv("issues.csv");
const priority = await readCsv("priority_issues.csv");
const issueSummary = await readCsv("issue_summary.csv");
const coverage = await readCsv("study_coverage.csv");
const meta = await readCsv("metadigitise_reconciliation.csv");
const raw = await readCsv("raw_data_reconciliation.csv");
const protocol = await readCsv("protocol_dictionary.csv");
const priorityUniqueRows = new Set(priority.slice(1).filter((r) => r[1] === "High" && r[5]).map((r) => r[5])).size;

const wb = Workbook.create();

const readme = wb.worksheets.add("README");
readme.showGridLines = false;
readme.mergeCells("A1:H1");
readme.getRange("A1").values = [["PCN data extraction cross-check report"]];
readme.getRange("A1:H1").format = {
  fill: "#15324B",
  font: { name: "Aptos Display", fontSize: 20, bold: true, color: "#FFFFFF" },
  verticalAlignment: "center",
  rowHeight: 42,
};
readme.mergeCells("A2:H2");
readme.getRange("A2").values = [["Audit of Data/PCN_data_ext_checking_v.3.csv against the protocol and available study evidence"]];
readme.getRange("A2:H2").format = {
  fill: "#E8F0F4",
  font: { name: "Aptos", fontSize: 11, italic: true, color: "#35556D" },
  wrapText: true,
  rowHeight: 30,
};

const readmeRows = [
  ["Scope", "207 effect-size rows, 72 original columns, 16 studies; all primary PDFs inventoried; 106 figure-sourced rows reconciled to MetaDigitise; 92 rows reconciled to available author/prepared workbooks."],
  ["Original preserved", "The source CSV was read only. SHA-256: 0bd770a4f117ead932c53b282c823a312a1526170c49f83623c8a7bb9b59a0fc"],
  ["How to read flags", "Each row in All flags is one cell-level finding. Multiple flags may concern the same effect-size row. Counts are therefore flags, not distinct erroneous rows."],
  ["Certainty", "Confirmed = directly supported by protocol/source or a deterministic calculation. Review = source ambiguity or a modeling/variance decision remains."],
  ["Severity", "High = changes a value, sample size, pairing/identifier, exposure, outcome unit/type, or analysis-critical statistic. Medium = source traceability, protocol placement, or a material schema issue. Low = controlled-vocabulary/case/spelling cleanup."],
  ["Priority review", "Start with Priority flags, then inspect the matching reconciliation tabs. Do not bulk-apply low-priority changes before resolving high-priority pairings/statistics."],
  ["Coverage caveat", "PDF methods/tables and all available digital sources were checked. Author-email values without a saved file remain review items. Visual figure extraction precision is limited by the saved MetaDigitise calibration."],
];
readme.getRange("A4:B10").values = readmeRows;
readme.getRange("A4:A10").format = { fill: "#D9E8EF", font: { bold: true, color: "#15324B" }, verticalAlignment: "top", wrapText: true };
readme.getRange("B4:B10").format = { font: { color: "#172033" }, verticalAlignment: "top", wrapText: true };
readme.getRange("A4:B10").format.borders = { insideHorizontal: { style: "thin", color: "#CAD6DE" }, outside: { style: "thin", color: "#9DB1BE" } };

readme.getRange("D4:H4").merge();
readme.getRange("D4").values = [["Flag summary"]];
readme.getRange("D4:H4").format = { fill: "#D9E8EF", font: { bold: true, color: "#15324B" }, verticalAlignment: "center" };
readme.getRange("D5:E8").values = [
  ["All flags", summary.issues_total],
  ["Confirmed flags", summary.confirmed],
  ["Review flags", summary.review],
  ["Rows with high-priority flags", priorityUniqueRows],
];
readme.getRange("D5:D8").format = { font: { bold: true, color: "#35556D" }, fill: "#F4F7F9" };
readme.getRange("E5:E8").format = { font: { bold: true, fontSize: 14, color: "#15324B" }, fill: "#F4F7F9", horizontalAlignment: "right" };
readme.getRange("G5:H7").values = [
  ["High", summary.by_severity.High],
  ["Medium", summary.by_severity.Medium],
  ["Low", summary.by_severity.Low],
];
readme.getRange("G5:G7").format = { font: { bold: true }, fill: "#F4F7F9" };
readme.getRange("H5:H7").format = { font: { bold: true, fontSize: 14 }, fill: "#F4F7F9", horizontalAlignment: "right" };
readme.getRange("D5:H8").format.borders = { preset: "outside", style: "thin", color: "#9DB1BE" };
readme.getRange("A12:H12").merge();
readme.getRange("A12").values = [["Key confirmed findings"]];
readme.getRange("A12:H12").format = { fill: "#15324B", font: { bold: true, color: "#FFFFFF" }, rowHeight: 26 };
const keyFindings = [
  ["Study / scope", "Finding", "Affected", "Action"],
  ["abramova_2021_front", "All 14 rows use author raw data, but each control arm is summarized from the opposite sex while the experimental arm matches offspring_sex. Six figure-labelled rows also cite the wrong source type.", "14 rows", "Replace control summaries with the same-sex author subgroup; correct source/file fields."],
  ["abramova_2020_genpath", "44 stored SE values are inconsistent with SD/sqrt(n); es162 also has a source-SD mismatch.", "34 rows / 45 flags", "Use the verified SD and n to recompute SE; correct es162 ex_sd first."],
  ["abramova_2023_biopsy", "Sex-coded c_a_id/ex_a_id/comparison values conflict with the paired source rows; mean-grooming units/types are also wrong.", "117 field flags across 39 rows; 4 unit/type rows", "Rebuild identifiers from source sex/group and correct mean-grooming duration to time in seconds."],
  ["arjunan_2023_stress", "Exposure is white/broadband 0-20 kHz, not ultrasound 0-2,000 Hz.", "6 rows", "Correct noise category and frequency before deriving acoustic moderators."],
  ["uygur_2010_aphyhun", "45 min/day was entered as 0.66 h, and CON/PSN sample sizes are reversed.", "3 rows", "Set duration to 0.75 h and sample sizes to control 10 / exposed 9."],
  ["whitlow_1978_thesis", "SD=sqrt(mean) is an explicit assumption because the figure error bars are undefined.", "36 rows", "Make a documented sensitivity-analysis decision; this is not a transcription correction."],
  ["abramova_2024_devneur", "Two author-email sucrose rows lack a supporting file, and four Figure 3b/3c screenshot filenames are transposed.", "6 rows", "Archive the author source and correct the four screenshot stems."],
];
readme.getRange(`A13:D${12 + keyFindings.length}`).values = keyFindings;
readme.getRange("A13:D13").format = { fill: "#D9E8EF", font: { bold: true, color: "#15324B" }, wrapText: true, rowHeight: 28 };
readme.getRange(`A14:D${12 + keyFindings.length}`).format = { wrapText: true, verticalAlignment: "top", font: { fontSize: 9 } };
readme.getRange(`A13:D${12 + keyFindings.length}`).format.borders = { insideHorizontal: { style: "thin", color: "#DCE4EA" }, outside: { style: "thin", color: "#9DB1BE" } };
setWidths(readme, [25, 70, 21, 55, 15, 4, 17, 14]);
readme.freezePanes.freezeRows(2);

const priorities = writeTableSheet(wb, "Priority flags", priority, [11, 10, 12, 25, 26, 11, 11, 29, 35, 42, 65, 55, 38, 58], "PriorityFlagsTable");
const allFlags = writeTableSheet(wb, "All flags", issues, [11, 10, 12, 25, 26, 11, 11, 29, 35, 42, 65, 55, 38, 58], "AllFlagsTable");
const summarySheet = writeTableSheet(wb, "Flag summary", issueSummary, [32, 13, 14, 18], "FlagSummaryTable");
const coverageSheet = writeTableSheet(wb, "Study coverage", coverage, [30, 14, 65, 70, 22, 18, 16, 70], "CoverageTable");
const metaSheet = writeTableSheet(wb, "MetaDigitise check", meta, [26, 11, 11, 19, 35, 23, 23, 14, 24, 33, 15, 15, 13, 14, 24, 33, 15, 15, 13, 14, 15, 50, 55], "MetaCheckTable");
const rawSheet = writeTableSheet(wb, "Author data check", raw, [27, 11, 11, 75, 75, 18, 18, 18, 18, 20, 60], "RawDataCheckTable");
const protocolSheet = writeTableSheet(wb, "Protocol dictionary", protocol, [30, 115], "ProtocolDictionaryTable");

for (const sheet of [priorities, allFlags]) {
  const severityCol = sheet.getRange(`B2:B${sheet.getUsedRange().rowCount}`);
  severityCol.conditionalFormats.add("containsText", { text: "High", format: { fill: "#FDE2E1", font: { color: "#9C1C13", bold: true } } });
  severityCol.conditionalFormats.add("containsText", { text: "Medium", format: { fill: "#FFF0CC", font: { color: "#7A4B00", bold: true } } });
  severityCol.conditionalFormats.add("containsText", { text: "Low", format: { fill: "#E8F0F4", font: { color: "#35556D" } } });
  sheet.getRange(`C2:C${sheet.getUsedRange().rowCount}`).conditionalFormats.add("containsText", { text: "Review", format: { fill: "#EEE5FF", font: { color: "#5D2B91", bold: true } } });
}
metaSheet.getRange(`U2:U${meta.length}`).conditionalFormats.add("containsText", { text: "review", format: { fill: "#FFF0CC", font: { color: "#7A4B00", bold: true } } });
rawSheet.getRange(`J2:J${raw.length}`).conditionalFormats.add("containsText", { text: "match", format: { fill: "#E6F4EA", font: { color: "#1F6F43" } } });
rawSheet.getRange(`J2:J${raw.length}`).conditionalFormats.add("containsText", { text: "mismatch", format: { fill: "#FDE2E1", font: { color: "#9C1C13", bold: true } } });
coverageSheet.getRange(`F2:G${coverage.length}`).format.horizontalAlignment = "right";
summarySheet.getRange(`D2:D${issueSummary.length}`).format.horizontalAlignment = "right";
protocolSheet.getRange(`A2:B${protocol.length}`).format.rowHeight = 38;

await fs.mkdir(outDir, { recursive: true });
const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(outPath);

const checks = [];
checks.push((await wb.inspect({ kind: "table", range: "README!A1:H20", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 8, maxChars: 7000 })).ndjson);
checks.push((await wb.inspect({ kind: "table", range: "Priority flags!A1:N12", include: "values,formulas", tableMaxRows: 12, tableMaxCols: 14, maxChars: 7000 })).ndjson);
checks.push((await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" })).ndjson);
await fs.writeFile(`${tmp}/workbook_inspection.ndjson`, checks.join("\n"), "utf8");

for (const [sheetName, fileName, range] of [
  ["README", "preview_readme.png", "A1:H20"],
  ["Priority flags", "preview_priority.png", "A1:N15"],
  ["All flags", "preview_all_flags.png", "A1:N18"],
  ["Flag summary", "preview_flag_summary.png", "A1:D18"],
  ["Study coverage", "preview_coverage.png", "A1:H18"],
  ["MetaDigitise check", "preview_meta.png", "A1:W14"],
  ["Author data check", "preview_raw.png", "A1:K14"],
  ["Protocol dictionary", "preview_protocol.png", "A1:B18"],
]) {
  const blob = await wb.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(`${tmp}/${fileName}`, new Uint8Array(await blob.arrayBuffer()));
}

console.log(outPath);
