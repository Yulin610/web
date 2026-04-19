# Export to PDF (API Doc + Technical Report)

This repo stores PDF-ready Markdown in `docs/`.

## Files to export
- `docs/API_Documentation.md` -> `docs/API_Documentation.pdf`
- `docs/Technical_Report.md` -> `docs/Technical_Report.pdf`

## Option A: Pandoc (recommended)
Install Pandoc, then run:

```bash
pandoc docs/API_Documentation.md -o docs/API_Documentation.pdf
pandoc docs/Technical_Report.md -o docs/Technical_Report.pdf
```

## Option B: VS Code / Cursor print-to-PDF
1. Open the `.md` file
2. Use Markdown Preview
3. Print / Export as PDF

## After export
Commit the generated PDFs into the GitHub repo and link them in `README.md`.

