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
- Extract assignment, quiz, lab, project, exam, survey, registration, and accommodation deadlines. Preserve whether each date is exact, recurring, unpublished, or section-dependent, and record the applicable student track.
- Identify definitions, assumptions, algorithms, failure modes, tradeoffs, examples, counterexamples, and links to existing concepts.
- Apply the course language contract while writing: Chinese-primary prose by default, precise English technical terms, and English citation labels/source markers.

## Write only authorized layers

1. Copy or move the exact source into `raw/` only after the destination is resolved and safe.
2. Append its metadata to `raw/manifest.md`.
3. Follow [reading-workflow.md](reading-workflow.md): create a self-contained primary lecture draft, with a recap, connected explanation, teaching example, assumptions, and closed-book self-check. A revision remains secondary while its differences are unresolved; after source checking, integrate ordinary factual corrections into the primary page while preserving human contributions and source history.
4. Reuse existing concepts; create a topic-cluster concept draft only when it warrants independent assessment or cross-lecture reuse. Keep short definitions and examples inside the lecture. Keep concept references consistent with primary lecture sources; use wiki/pending for actual conflicts, not routine content verification.
5. Create original practice questions with separate collapsed hints and explanations, each linked back to its lecture section. Add top-level return_to links to reference pages.
6. Create new deadline records in `learning/deadlines/` only when an official source is explicit; otherwise create candidate records or a proposal without guessing missing date/time fields.
7. Update the lecture-first reading route in `wiki/index.md` and any secondary reference catalogue; maintain one primary entry per lecture. Append one operation entry to `wiki/log.md`.
8. Leave next_review empty; ingestion does not schedule a test or review session. Keep learning on demand.
9. Refresh the derived Overview summary without copying concept or deadline prose.

## Source verification

After inspecting the source and checking claims/citations, ordinary lecture, concept and question notes can become active with checked_at. Source release status is separate: checking a saved PDF does not verify today's website. Keep unresolved conflicts and policy changes in proposals, preserve human contributions, and describe specific remaining uncertainties. Do not ask the student to approve every routine note.
