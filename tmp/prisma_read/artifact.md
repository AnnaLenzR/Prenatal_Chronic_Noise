# Template execution contract

## Reference

- Source: `/Users/annalenz/Desktop/Bird_map/outlines/Bird_noise_map_screening_counts.docx`
- SHA-256: `ccd0edbbcd286bcd7db6c8a7884402ac59c83e30dd44540be9a741ba22eec4ee`
- Render evidence: `tmp/prisma_read/example_docx_render/page-1.png` through `page-12.png`
- Page count: 12; section count: 2.
- Preserve the reference file unchanged. Build the new report from a copied package.

## Page system

- Section 1: US Letter portrait, 8.5 x 11 in; 1 in margins; new-page start.
- Section 2: US Letter landscape, 11 x 8.5 in; 0.75 in margins; new-page start.
- Both sections have independent headers and footers. Page number fields appear in the footer.
- Section 1 is the count/reconciliation brief. Section 2 contains record-level appendices and the final landscape flowchart.

## Typography and color

- Body: Calibri 11 pt, dark navy/black, 6 pt paragraph-after rhythm.
- Title role: 26 pt, dark navy `#17365D`, 15 pt after.
- Subtitle role: 12 pt, muted blue-gray.
- Heading 1: Calibri 16 pt bold, blue `#2E74B5`, 18 pt before and 10 pt after.
- Heading 2: Calibri 13 pt bold, blue `#2E74B5`, 14 pt before and 7 pt after.
- Header/footer: compact uppercase gray-blue text, with project identity left and document role right.

## Tables

- Use the reference's light-blue header fill, thin blue-gray borders, Calibri body, and explicit widths.
- Summary source table: 6.5 in total, columns 5.25 / 1.25 in.
- Stage table: 6.5 in total, columns approximately 3.30 / 0.87 / 2.33 in.
- Appendix table: landscape width 9.5 in, columns approximately 0.85 / 7.05 / 1.60 in.
- Header rows repeat across pages; rows expand automatically; cell margins remain generous.

## Components and content flow

1. Title block: evidence-selection counts, project name, working date.
2. Scope callout: records/reports/studies as reporting units.
3. Source-count table and arithmetic check.
4. Selection-stage reconciliation table.
5. Full-text primary-reason table and arithmetic reconciliation.
6. Source-note section documenting Rayyan, benchmark/general searching, and analysis dataset.
7. Appendix A: full-text exclusions with one primary reason per report.
8. Appendix B: report not retrieved.
9. Appendix C: additional included reports identified outside the formal strategy.
10. Final landscape PRISMA-style flowchart with caption.

## Slot map and rewrite rules

- Rewrite all Bird-project body content for the prenatal chronic-noise meta-analysis.
- Replace the project labels in both section headers.
- Preserve page geometry, footer/page-number pattern, overall type hierarchy, table palette, and appendix density.
- Replace the embedded Bird flowchart with the new PCN flowchart; do not retain Bird records or numbers.
- Keep the record-level appendix auditable with Rayyan ID, reference, and primary reason.

## Package preservation

- Preserve styles, theme, font table, settings, numbering, section geometry, and relationship plumbing unless a necessary cloned component adds a relationship.
- Header text, body document XML, footer PAGE field, and the embedded image relationship are editable.
- No comments, content controls, tracked changes, footnotes, or endnotes are required.

## Fidelity gates

- The reference SHA-256 must remain unchanged.
- Final document must retain the portrait-to-landscape section pattern and recognizable blue/navy visual language.
- Render and inspect every page. Reject clipping, split header rows, broken borders, unexpected font substitution, and any appendix row whose reason is not visible.
- Reconcile every displayed arithmetic total before delivery.
