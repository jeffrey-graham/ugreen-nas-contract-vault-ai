# Uliya CLI Capability & Action Matrix

This reference maps every UGREEN AI NAS capability used by `contract-invoice-vault-auditor` to its registered expert agent, published CLI, specific action, data effect, approval policy, and completion evidence in `capability-catalog.json` (version `2.0.0`).

## 1. Registered Expert Ownership Table

| Capability Domain | Published CLI | Registered Expert Agent | Role in `contract-invoice-vault-auditor` |
| :--- | :--- | :--- | :--- |
| File management (`file`) | `file-workflow` | `file-agent` | Resolve authorized user workspace directories and execute workflow-approved batch file moves into the archive vault. |
| File management (`file`) | `ug-filesystem` | `file-agent` | Discover contracts, invoices, and audio files, inspect file metadata, compute cryptographic `sha256sum` digests, create archive directories, and copy/move verified files. |
| File management (`file`) | `ug-filemgr` | `file-agent` | Run non-destructive duplicate scans (`scan-dedupe`) and attach semantic audit tags (`Verified-Match`, `Variance-Flagged`, `Duplicate-Candidate`). |
| Album (`album`) | `ug-photo` | `photo-agent` | Search photographed receipts and payment screenshots, inspect image metadata, and extract merchant/tax/payment evidence via `vision-ocr` and `vision-vlm`. |
| Documents (`document`) | `ug-document` | `document-agent` | Read document metadata and page counts, extract structured contract and invoice fields, and reconcile multi-document billing totals and clauses. |
| Knowledge (`knowledge`) | `ug-knowledge` | `knowledge-agent` | Transcribe meeting/voice recordings (`audio-transcription`), gather supporting evidence (`collect-evidence`), and save the Markdown Audit Ledger (`save-text`). |

## 2. Stage-by-Stage Action & Approval Reference

### Stage 1: Scope Discovery, Cryptographic Inventory & Duplicate Scan (`file-agent`)

| CLI | Action | Key Parameters | Effect | Approval | Completion Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `file-workflow` | `get-user-dir` | *(none)* | `read` | `none` | Verified authorized user root directory list. |
| `ug-filesystem` | `find` | `path`, `pattern`, `type`, `start-timestamp`, `end-timestamp`, `max-depth`, `limit` | `read` | `none` | Real matched file paths within the user-specified scope. |
| `ug-filesystem` | `ls` | `path`, `recursive`, `max-depth`, `limit` | `read` | `none` | Directory entry listing with real file names and types. |
| `ug-filesystem` | `stat` | `path` | `read` | `none` | File size, modification timestamp, and attribute metadata. |
| `ug-filesystem` | `sha256sum` | `path` | `read` | `none` | 64-character hexadecimal SHA-256 cryptographic digest per file. |
| `ug-filemgr` | `scan-dedupe` | `path`, `scope` | `read` | `none` | Duplicate candidate groups sharing identical content digests. |

### Stage 2: Visual Receipt & Screenshot OCR/VLM Extraction (`photo-agent`)

| CLI | Action | Key Parameters | Effect | Approval | Completion Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-photo` | `search-picture` | `dir`, `file-name-contains`, `ocr-contains`, `start-time`, `end-time`, `page`, `page-size` | `read` | `none` | Matched photo paths and item metadata from NAS Albums. |
| `ug-photo` | `search-screen` | `keyword`, `path`, `page`, `page-size` | `read` | `none` | Matched billing/wire-transfer screenshot items and paths. |
| `ug-photo` | `meta` | `path`, `raw` | `read` | `none` | Capture timestamp, resolution, and EXIF metadata for audit provenance. |
| `ug-photo` | `vision-ocr` | `path` | `read` | `none` | Raw OCR text lines extracted from receipt photos or screenshots. |
| `ug-photo` | `vision-vlm` | `path`, `prompt`, `model`, `max-tokens`, `temperature` | `read` | `none` | Structured VLM extraction of merchant, date, tax, and payment total. |

### Stage 3: Multi-Document Extraction & Reconciliation (`document-agent`)

| CLI | Action | Key Parameters | Effect | Approval | Completion Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-document` | `page-count` | `file` | `read` | `none` | Verified page count of each contract or invoice document. |
| `ug-document` | `metadata` | `file`, `include-pages`, `directory-limit` | `read` | `none` | Document title, author, creation timestamps, and page structure. |
| `ug-document` | `extract` | `query`, `file`, `schema`, `content-scope`, `max-files`, `body-cap`, `dedupe` | `read` | `none` | Structured JSON/table fields (counterparty, line items, tax, totals, dates). |
| `ug-document` | `reconcile` | `query`, `file`, `max-files` | `read` | `none` | Cross-document comparison identifying matched items and discrepancies. |
| `ug-document` | `qa` | `query`, `file`, `intent`, `content-scope`, `evidence-mode`, `max-files` | `read` | `none` | Clause-level answers with verbatim document evidence citations. |

### Stage 4: Verbal Change-Order Verification & Ledger Persistence (`knowledge-agent`)

| CLI | Action | Key Parameters | Effect | Approval | Completion Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-knowledge` | `audio-transcription` | `path`, `language`, `speak-count` | `read` | `none` | Speaker-attributed transcript of meeting or voice-memo recordings. |
| `ug-knowledge` | `collect-evidence` | `query`, `path`, `extension`, `full` | `read` | `none` | Extracted verbal approval snippets correlated with invoice variances. |
| `ug-knowledge` | `save-text` | `path`, `content`, `content-ref`, `filename-hint` | `state-change` | `workflow` | Saved Markdown Audit Ledger path confirmed after workflow approval. |

### Stage 5: Approval-Gated Semantic Tagging & Vault Organization (`file-agent`)

| CLI | Action | Key Parameters | Effect | Approval | Completion Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ug-filemgr` | `tag-get-by-name` | `name` | `read` | `none` | Existing tag ID if the audit tag already exists on the NAS. |
| `ug-filemgr` | `tag-add` | `colour`, `tag-id` | `state-change` | `gateway` | Newly created tag metadata after gateway approval. |
| `ug-filemgr` | `tag-set` | `tag-id`, `name`, `colour` | `state-change` | `gateway` | Updated tag label and color configuration after gateway approval. |
| `ug-filemgr` | `tag-add-file` | `path`, `tag-id` | `state-change` | `conditional` | Confirmation that the audit tag was attached to the target file path. |
| `ug-filesystem` | `mkdir` | `path`, `mode`, `parents` | `state-change` | `gateway` | Created archive vault directory path after gateway approval. |
| `ug-filesystem` | `cpmv` | `src`, `dst`, `type`, `action-type`, `overwrite` | `state-change` | `gateway` | Verified copy or move completion for each approved file path. |
| `file-workflow` | `batch-move` | `data`, `actionType`, `root`, `renameBy`, `dateField`, `sourceDir`, `destination` | `state-change` | `workflow` | Batch move execution summary after workflow approval. |

## 3. Strict Boundary Rules

1. **Parent Delegation Only**: The parent Skill coordinates child experts solely via `delegate --target <agent-id> --instruction '<task>'`. Child experts select and execute their own underlying CLI actions.
2. **Zero Unsupported Operations**: Every step maps strictly to the 6 published CLIs above. No external network calls, shell scripts, or uncataloged system operations are ever requested.
3. **Real Upstream Evidence Only**: Every stage consumes only real paths, digests, and extracted records returned by an earlier `completed` delegation step.
