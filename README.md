# Prenatal Chronic Noise Exposure Meta-analysis

A multilevel meta-analysis of the effect of prenatal/gestational chronic noise exposure on anxiety- and depression-like behaviour in rodent offspring.

The analysis and its full reproducible record live in [`pcne_book/`](pcne_book/), a Quarto book. The rendered report is the primary output of this repository; everything else (extraction files, source PDFs, protocol documents) exists to support and audit that report.

## Protocol

The analysis follows a pre-specified protocol, with one documented deviation:

- `protocol/PCNE_protocol_v.4_111425.docx` - the analysis protocol
- `protocol/` also holds the deviation addendum referenced throughout the book (offspring age class handled as a sensitivity analysis rather than the primary age moderator)

## Repository structure

- `pcne_book/` - the Quarto book: all analysis chapters (data wrangling, effect size calculation, overall effect, moderators, publication bias, CRIME-Q appraisal, leave-one-out sensitivity analysis), rendered to `pcne_book/_site/`
- `Data/` - extraction data, including `Data/derived/` (analysis-ready files produced by the book, e.g. `db_effect_sizes.csv`) and `Data/audits/` (provenance and sensitivity-check exports written by the book, safe to regenerate by re-rendering)
- `outputs/` - the reviewed, version-controlled extraction database (the file the book reads from is never overwritten by re-rendering)
- `output/` - crosscheck/review reports comparing extraction versions
- `included_studies/` - full-text PDFs of the included studies
- `Metadigitise_figs/` - figures digitized with metaDigitise for studies reporting data only in plots
- `protocol/` - the protocol and its deviation addendum
- `R/` - early exploratory scripts, superseded by the Quarto book
- `html/` - standalone rendered figures/reports outside the book
- `Figures/` - currently empty; reserved for manuscript-ready figure exports

## How to reproduce the analysis

1. Open `ChronicNoise_Rodents.Rproj` in RStudio.
2. Open any chapter's setup chunk once to let `pacman` install the required R packages (each chapter lists its own).
3. Render the whole book: in RStudio's **Build** pane, click **Render Book**, or run `quarto render` from a terminal inside `pcne_book/`.

The rendered site is written to `pcne_book/_site/` (not tracked in git - see below).

Every chapter resolves paths relative to the project root (`normalizePath("..")` with `execute-dir: project` in `_quarto.yml`), so the book renders correctly regardless of which machine or folder location it is run from, as long as the folder structure above stays intact.

## Publishing the rendered book to GitHub Pages

From a terminal inside `pcne_book/`:

```
quarto publish gh-pages
```

This renders the book and pushes the contents of `_site/` to a `gh-pages` branch on this repository, then prints the published URL (`https://annalenzr.github.io/Prenatal_Chronic_Noise/`). The first run will ask to confirm the destination and may open a browser window for GitHub authentication; afterwards, re-running the same command updates the published site with the latest render.

## License

MIT - see `LICENSE`.

## Contact

Anna Lenz (lenzrive@ualberta.ca)
