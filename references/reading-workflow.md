# Human-readable course notes

Use this reference when ingesting, reorganizing, teaching, or reviewing course material.

## Reading hierarchy

Default to `knowledge_organization: lecture-first` and `concept_granularity: topic-cluster`. Follow an explicit course override.

- `Home.md`: put a prominent link to the reading route before dynamic tables.
- `Index.md`: durable navigation by user intent (learn, review, look up, deadlines, maintenance).
- `wiki/index.md`: the course reading route. List one primary reading page per available lecture with a Chinese descriptive title, central question, prerequisite, and a short closed-book review route. Mark missing lectures explicitly rather than inventing coverage.
- A primary lecture page must teach a coherent unit without requiring the reader to open concept cards. Write connected explanations: problem -> model/assumptions -> mechanism -> worked teaching example -> limitations/tradeoffs -> closed-book self-check. Group related terms under a few meaningful sections.
- Start each lecture with a 3-5 minute recap and local section navigation; end with retrieval questions, links to adjacent lectures, and an optional reference section. Keep formulas with symbol meanings, intuition, assumptions, and scope.
- Concept cards are secondary references with stable concept IDs; Progress owns the student's current questions. Create a separate card only when it supports independent assessment or substantive reuse across lectures. A synonym, short definition, example, or closely dependent subpoint normally belongs in the lecture or a topic cluster.
- Put the full concept catalogue and revision history behind secondary links. Do not put a flat list of dozens of English filenames or several revisions of one lecture on the main reading route. Display Chinese labels while retaining precise English terms and stable paths.
- Cross-lecture synthesis should explain relationships and contrasts, not duplicate all lecture prose. Use a small comparison table or diagram only where it helps.

## Updating existing vaults

Preserve raw files, stable IDs, mastery, review dates, human contributions, and existing links. Reorganization alone is not source verification or learner evidence. Ordinary notes may become active after actual source checking. Reuse and improve the existing primary lecture file; avoid adding a second full set of competing summaries.

An explicitly requested reorganization authorizes navigation edits and the requested content restructuring. Keep source status and uncertainties visible. If incorporating a locally available revision, cite that exact revision and retain a link to its change record. A saved Final PDF does not prove the current website is unchanged.

When a new source arrives unattended, preserve the existing primary reading page if review/approval is required and link its revision proposal secondarily; do not create competing primary entries.

## Return navigation and reading layout

Pin the primary lecture tab when beginning a reading session. Keep references, PDFs, question sets and revisions in separate tabs; when the agent opens them, explicitly request a new tab. Reuse an already open lecture tab when returning, without reopening its file or resetting scroll. In ordinary Markdown, Cmd-click (Ctrl-click on Windows/Linux) opens a reference in a new tab; Back is the fallback for same-tab navigation. Do not claim all plain clicks are automatically intercepted.

Each reference note has visible return links at the top and a return_to list of Wikilinks to relevant primary lecture sections. Shared concepts list all relevant lectures; never write a global “came from” value into a shared note. Keep old file paths and heading anchors stable. A return link goes to the named section; the pinned tab preserves the exact browsing position.

Default to reading mode, hide in-document Properties and the duplicate inline filename, and show Outline. Graph remains available on demand. Do not install a plugin or add a browser app to implement this.

## Review behavior

Only when the learner asks to review, choose the requested lecture or connected topic, briefly orient them, and ask one question at a time. Use actual answers and misconceptions for follow-up; do not generate daily assignments, due queues, or recurring sessions. After real answers, record brief evidence in a session and update Progress's current misconceptions; new records require no score.

## Acceptance

Check the rendered or readable content, not only the schema:
- Can a learner select where to start within one screen?
- Can each lecture be understood and reviewed without opening its concept cards?
- Are historical revisions and optional enrichment clearly separated from required coverage?
- Are recaps, examples, formula assumptions, and self-check questions actually present?
- Do navigation links resolve, including heading links, and do original IDs/review state remain unchanged?
