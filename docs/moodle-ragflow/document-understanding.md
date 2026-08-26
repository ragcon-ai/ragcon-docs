# Document understanding

The suite's answers and search are only as good as how well your documents are **read**. RAGflow does
not just index file names and plain text — it parses the **actual content** of your files, including
scanned pages, images and tables, and searches them by **meaning**. That is what sets it apart from
Moodle's built-in search.

## Not just text — the whole document

RAGflow's **DeepDoc** engine reads a document the way a person would:

- **Optical character recognition (OCR).** Scanned PDFs and photographed pages become searchable text.
  Multilingual.
- **Layout understanding.** It recognises the structure of each page — titles, paragraphs, tables,
  figures, headers/footers, references and equations — and reads it in the right order, so a heading
  stays with its section and page furniture (running headers/footers) is discarded.
- **Table structure.** Tables are captured as rows and columns, not a flat blur of numbers.

## Images and figures are understood, too

- A **vision model** (configured as the optional *img2txt* model) describes the figures, diagrams and
  screenshots inside your documents. That description becomes **searchable text**, and the image itself
  is stored with the passage.
- So an image can be **found by search** and **shown as a source in a chat answer** — not only the text
  around it.

!!! note "Image understanding is optional"
    OCR, layout and table recognition are built in. Understanding the *content of images* additionally
    needs an **img2txt (vision) model** configured in RAGflow — see [Set up RAGflow](setup-ragflow.md).

## Choose how documents are parsed

- **DeepDoc** (built in) — the default OCR + layout + table pipeline.
- **MinerU** and **Docling** (RAGflow **0.25+**) — alternative parsing methods for high-fidelity
  extraction, with options such as **formula recognition** and table recognition and multilingual OCR,
  selectable per knowledge base.
- **Content-aware chunking** — templates for general text, papers, books, manuals, presentations,
  tables, Q&amp;A, laws, e-mails and pictures split each document the way its type needs.

## Meaning, not keywords

Retrieval embeds your query and your documents into the same vector space, so a question finds the
passage that **means** the same thing even when it uses different words. An optional **rerank model**
sharpens the order of the results.

## How this differs from Moodle's search

| | Moodle's built-in search | RAGflow (this suite) |
|---|---|---|
| Searches in | titles, text fields, metadata, forum posts | **the content of the files themselves** |
| Scanned PDFs / images | invisible | **OCR + image description → searchable** |
| Tables / diagrams | ignored | **captured as structure / described by a vision model** |
| Matches by | exact keyword | **meaning** (embeddings, optional rerank) |
| Returns | a link to the activity | **the supporting passage + image**, optionally an answer |

Moodle's search is excellent at finding *courses and activities* by name. RAGflow is about finding *what
a document says* — and answering from it.

## What it means in practice

- A learner's question is answered from the **exact paragraph** — even if it lives in a scanned handout
  or on a slide.
- A **diagram** that explains a concept can surface in search, with the picture attached.
- A trainer uploads the material **as-is** — no need to retype tables or transcribe scans.

## Requirements

- An **embedding model** is required (it builds and searches every knowledge base).
- **Image understanding** needs an **img2txt (vision) model**; **formula / high-fidelity extraction**
  needs **MinerU** or **Docling** (RAGflow 0.25+).

See **[Set up RAGflow](setup-ragflow.md)** to configure the models, and the
[Search block](plugins/search.md) and [Tutor block](plugins/tutor.md) to put it to use.
