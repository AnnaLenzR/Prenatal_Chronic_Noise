import fs from "node:fs/promises";
import { Workbook } from "@oai/artifact-tool";

const files = [
  ["title_abstract", "../../PCN_screening/title_abstract_2026-08-28_23-45-55/articles.csv"],
  ["full_text", "../../PCN_screening/full_text_2026-08-28_23-47-26/articles.csv"],
];

for (const [stage, path] of files) {
  const csvText = await fs.readFile(new URL(path, import.meta.url), "utf8");
  const workbook = await Workbook.fromCSV(csvText, { sheetName: stage });
  const sheet = workbook.worksheets.getItem(stage);
  const values = sheet.getUsedRange(true).values;
  const headers = values[0];
  const notesIndex = headers.indexOf("notes");
  const keyIndex = headers.indexOf("key");
  const decisions = { Included: 0, Excluded: 0, Missing: 0 };
  const keys = new Set();
  for (const row of values.slice(1)) {
    const note = String(row[notesIndex] ?? "");
    const match = note.match(/RAYYAN-INCLUSION: \{"Anna"=>"([^"]+)"\}/);
    decisions[match ? match[1] : "Missing"] += 1;
    keys.add(String(row[keyIndex]));
  }
  const inspection = await workbook.inspect({
    kind: "sheet,table",
    maxChars: 1600,
    tableMaxRows: 3,
    tableMaxCols: 5,
  });
  console.log(JSON.stringify({
    stage,
    dataRows: values.length - 1,
    uniqueKeys: keys.size,
    decisions,
    inspection: inspection.ndjson,
  }));
}
