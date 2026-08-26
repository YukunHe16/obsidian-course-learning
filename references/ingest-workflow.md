# Source ingestion workflow

## Input and identity

1. Read `Course.md` and locate unprocessed files in `inbox/` or the user-specified path.
2. Compute SHA-256 and compare it with `raw/manifest.md` before analysis.
3. If the hash already exists, report the existing source and stop without duplicate notes.
4. If the lecture number already has another hash, preserve both files and mark the newer draft as a possible revision. Do not supersede the prior source without evidence or confirmation.

## Inspect the source

- For PDFs, extract text and render every page. Inspect diagrams, tables, staged-reveal slides, questions without answers, and pages whose meaning is mostly visual.
- Preserve slide/page numbering in citations.
- Separate durable knowledge from time-sensitive logistics and academic-integrity policy.
- Identify definitions, assumptions, algorithms, failure modes, tradeoffs, examples, counterexamples, and links to existing concepts.
- Apply the course language contract while writing: Chinese-primary prose by default, precise English technical terms, and English citation labels/source markers.

## Write only authorized layers

1. Copy or move the exact source into `raw/` only after the destination is resolved and safe.
2. Append its metadata to `raw/manifest.md`.
3. Create a lecture note with `status: draft`.
4. Create new concept drafts or a proposal under `wiki/pending/` for changes to existing canonical concepts.
5. Create original practice questions with private answer rubrics in `learning/questions/`.
6. Update `wiki/index.md` and append one operation entry to `wiki/log.md`.
7. Set initial concept review to the next day; the scheduled review may pick it up later if it becomes overdue.
8. Refresh the derived Overview summary without copying concept prose.

## Approval boundary

An unattended ingest may produce drafts and proposals. It must not promote a lecture, merge changes into an existing reviewed concept, modify course policy, or overwrite a human edit. End with a compact approval checklist.
