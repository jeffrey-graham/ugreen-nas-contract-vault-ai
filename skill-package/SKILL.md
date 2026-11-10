---
name: contract-invoice-vault-auditor
description: Cross-modal contract, invoice, receipt photo, and voice-memo reconciliation report with cryptographic SHA-256 duplicate auditing and verified archive organization on UGREEN AI NAS; use when the user asks to audit project contracts against invoices and receipts, flag billing discrepancies or duplicate files, attach audit tags, and organize verified records into a structured knowledge vault.
---

# Goal

Deliver an end-to-end, local-first financial and legal document audit on UGREEN AI NAS (`kimage-planb` full `main-agent` profile) that reconciles project contracts, vendor invoices, photographed paper receipts or payment screenshots, and recorded verbal change-order memos within user-authorized NAS directories. The Skill produces:

1. A cryptographic file inventory and non-destructive duplicate billing report (`sha256sum` digests and `scan-dedupe` candidate groups).
2. A cross-modal reconciliation matrix comparing signed contract terms, invoice line items, OCR/VLM-extracted receipt totals, and transcribed audio approvals.
3. A persistent Markdown Audit & Reconciliation Ledger saved to the user's NAS knowledge base after workflow approval.
4. Approval-gated semantic file tags (`Verified-Match`, `Variance-Flagged`, `Duplicate-Candidate`) and organized archive folders for verified records.

For detailed CLI action parameters, schemas, test cases, and compliance disclosures, consult the directly linked references:
- Read [references/cli-command-matrix.md](references/cli-command-matrix.md) when mapping capability domains, CLI actions, data effects, and approval boundaries.
- Read [references/schema-and-output-templates.md](references/schema-and-output-templates.md) when structuring extraction prompts, reconciliation payloads, and the final Markdown Audit Ledger.
- Read [references/test-cases-and-edge-recovery.md](references/test-cases-and-edge-recovery.md) when validating core workflows, edge cases, empty results, and state recovery.
- Read [references/security-and-permission-model.md](references/security-and-permission-model.md) when reviewing privacy rules, approval gates, third-party/open-source licenses, and AI tool disclosures.

# Required input

Collect only the parent-level orchestration scope from the user before starting delegation; do not pre-collect private parameters owned by child experts:

- **Source scope** (required): User-specified project directory name, folder scope, or date/project filter containing the contracts, invoices, or audio notes to audit (for example, `Projects/2026-Q4-Client-Alpha` or `Downloads/Billing-2026`). If the user omits the source scope, enter `waiting_user` and ask for the target folder or project keyword.
- **Visual receipt scope** (optional): Album name, time range, or keyword in NAS Photos containing photographed receipts or wire-transfer screenshots (for example, `2026-Q4-Receipts`). When omitted, the photo receipt stage is omitted cleanly unless requested.
- **Archive & ledger destination** (optional): Target archive folder name and knowledge note location for storing the reconciled ledger and organized files. Even when the user specifies an archive destination upfront, all state-changing write, tag, mkdir, and move operations still require runtime confirmation (`waiting_approval` / `waiting_user`).
- **Audit tolerance & rules** (optional): Currency, tax rate expectations, or line-item variance threshold (defaults to exact zero-variance matching across contract total, invoice total, and receipt payment amount).

# Generation-time capability evidence

- `file-workflow` → `file-agent`
- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `ug-photo` → `photo-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`

# Orchestration

The parent Skill coordinates four registered child experts in five sequential stages. Every stage passes only verified upstream business results (`completed` outputs with real file paths, SHA-256 digests, extracted fields, or album items) to downstream stages. See [references/cli-command-matrix.md](references/cli-command-matrix.md) for the complete action matrix and [references/schema-and-output-templates.md](references/schema-and-output-templates.md) for structured payload templates.

## Stage 1: Scope Resolution, Cryptographic Inventory & Duplicate Scan (`file-agent`)

Resolve the authorized user directory, enumerate candidate contract, invoice, and audio files, compute SHA-256 integrity hashes, and run a read-only duplicate scan within the user's target scope. Never delete, move, or modify files during Stage 1.

`delegate --target file-agent --instruction 'Resolve the user authorized directory scope and list all contract, invoice, receipt, and meeting audio files matching the user requested project folder and time window. Compute sha256sum and stat metadata for each matched file and run a read-only scan-dedupe check within the same folder scope. Do not modify, move, or delete any files. If no matching files exist, return an explicit empty result immediately.'`

- **Upstream-to-downstream handoff**: Extract the verified list of document file paths, audio file paths, file sizes, timestamps, SHA-256 hashes, and duplicate groups from the real result of Stage 1.
- **Empty-result gate**: If Stage 1 returns an empty result (`no results` / `zero matches` in the specified directory), report clearly to the user that no matching files were found in the target scope and stop all downstream stages without guessing alternative directories or fabricating filenames.

## Stage 2: Visual Receipt & Billing Screenshot OCR/VLM Extraction (`photo-agent`)

When the user's request includes photographed receipts, delivery dockets, or payment screenshots (or when image assets are referenced in the project scope), delegate visual search and on-device OCR/VLM extraction to `photo-agent`.

`delegate --target photo-agent --instruction 'Search the user authorized photo and screenshot albums for payment receipts, invoices, and billing confirmations matching the user specified project keyword and date range. For each matched image, run vision-ocr and vision-vlm to extract merchant name, transaction date, currency, tax amount, total paid amount, and payment reference number alongside the real image path and metadata. Perform read-only operations only and report an empty result if zero matches are found.'`

- **Upstream-to-downstream handoff**: Pass only verified receipt records (real image path, OCR text, VLM-parsed vendor, date, tax, and payment total) to Stage 3 for cross-modal reconciliation. If no receipt photos match (`empty list`), record that visual receipt coverage is absent and continue Stage 3 using the verified document paths from Stage 1.

## Stage 3: Multi-Document Extraction & Cross-Modal Reconciliation (`document-agent`)

Pass the verified contract and invoice file paths from Stage 1 and the verified visual receipt totals from Stage 2 to `document-agent` to inspect page counts and metadata, extract structured clauses and billing tables, and reconcile contracts against invoices and receipts.

`delegate --target document-agent --instruction 'Using only the verified contract and invoice file paths returned by the upstream file inventory and the verified receipt payment records from the upstream photo extraction, inspect document metadata and page-count, extract structured fields including counterparty name, contract cap, payment milestones, invoice number, line items, tax, and total due, and run reconcile and qa checks to identify exact matches, overbilling variances, tax calculation errors, missing receipts, or duplicate invoice numbers. Perform read-only analysis and never fabricate missing clauses or numbers.'`

- **Upstream-to-downstream handoff**: Pass the verified reconciliation summary, matched records, flagged discrepancy records, and source file citations to Stage 4.

## Stage 4: Verbal Change-Order Verification & Audit Ledger Persistence (`knowledge-agent`)

If Stage 1 discovered meeting or voice-memo audio recordings in the project scope, delegate `audio-transcription` and `collect-evidence` to `knowledge-agent` to verify whether any invoice variance flagged in Stage 3 was authorized by a recorded verbal change order. Then, after workflow approval, save the complete Markdown Audit & Reconciliation Ledger via `save-text`.

`delegate --target knowledge-agent --instruction 'Using the verified audio file paths from the upstream file inventory and the flagged billing variances from the upstream document reconciliation, transcribe the meeting recordings with audio-transcription and run collect-evidence to check whether any price or scope variance matches a recorded verbal approval. Compile the complete Markdown Audit and Reconciliation Ledger containing SHA-256 digests, duplicate file groups, contract-to-invoice-to-receipt reconciliation tables, and verbal evidence citations, and save the ledger to the user authorized knowledge destination via save-text after required workflow approval.'`

- **Upstream-to-downstream handoff**: Pass the saved Audit Ledger path and the final classification of each verified file (`Verified-Match`, `Variance-Flagged`, `Duplicate-Candidate`) to Stage 5.

## Stage 5: Approval-Gated Semantic Tagging & Vault Archiving (`file-agent`)

Before applying any file tags, creating archive directories, or moving/copying files, present the reconciliation summary and proposed file actions to the user and require explicit confirmation (`waiting_user` / `waiting_approval`). Once approved, delegate non-destructive tagging and archive organization to `file-agent`.

`delegate --target file-agent --instruction 'Using only the verified file paths and audit classifications from the upstream reconciliation and knowledge ledger steps, and strictly after user and gateway or workflow approval, resolve or create the audit tags Verified-Match, Variance-Flagged, and Duplicate-Candidate, attach the corresponding tag to each verified file path, create the approved archive directory structure, and copy or move the confirmed files into their designated archive folders without deleting any unapproved source files.'`

# Completion and failure

Handle all five public delegation states explicitly at every stage (detailed recovery matrices are in [references/test-cases-and-edge-recovery.md](references/test-cases-and-edge-recovery.md)):

- **`completed`**: Verify that the child expert returned concrete completion evidence (real file paths, SHA-256 digests, extracted fields, saved ledger path, or applied tag IDs). Advance to the next stage or present the final Audit & Reconciliation Report only when verified evidence is present.
- **`waiting_user`**: Pause orchestration immediately when required scope inputs are missing, when multiple candidate folders/albums are ambiguous, or when explicit user confirmation is required before state-changing archive operations. Present a clear prompt and wait for the user's response.
- **`waiting_approval`**: When a gateway-governed or workflow-governed action (`save-text`, `tag-add`, `tag-add-file`, `mkdir`, `cpmv`, `batch-move`) enters `waiting_approval`, report the pending operation, target paths, and data effect clearly to the user. Never treat `waiting_approval` as completed, and never proceed with dependent write steps until approval succeeds.
- **`cancelled`**: If the user cancels an approval prompt or halts execution, stop all pending delegations immediately, preserve any read-only findings or earlier `completed` outputs already confirmed, and report exactly which steps were completed and which were cancelled.
- **`failed`**: If any child expert returns `failed` (such as an unreadable or password-protected PDF, unsupported audio format, or permission error), halt any downstream step that depends on that missing result, preserve partial results from succeeded files, never fabricate replacement data, and report the exact failure reason and recovery guidance.
- **Empty and partial results**: When a query returns `no results` / `empty result` / `zero matches`, report the empty outcome honestly and stop without expanding scope or substituting unrelated NAS files. When a batch contains both readable and unreadable documents, report the verified results for succeeded files alongside an explicit exception table for failed files.

# Disclosures and boundaries

- **Newly developed principal functionality**: The 5-stage cross-modal reconciliation workflow (`contract-invoice-vault-auditor`), SHA-256 duplicate auditing flow, approval-gated vault tagging model, structured extraction schemas, and validation suite were newly developed specifically for the UGREEN Hackathon 2026 on AI NAS.
- **Third-party & open-source components**: This Skill package is pure Markdown and embeds zero external runtime SDKs or third-party code dependencies, executing entirely through built-in UGOS registered expert agents (`file-agent`, `photo-agent`, `document-agent`, `knowledge-agent`). Development-time validation used the official UGREEN `uliya-skill-kit` v0.7.3 (`capability-catalog.json` v2.0.0 and `check-skill.mjs` on Node.js under MIT License).
- **AI tool disclosure**: Claude Code / Antigravity AI coding assistant was used during development to query `capability-catalog.json`, format Markdown reference tables, and verify static compliance against `check-skill.mjs`. See [references/security-and-permission-model.md](references/security-and-permission-model.md) for the complete disclosure table.

The Skill is complete. You can upload it to [skillhub](https://skills.ugreen.com/skill-hub/publish).
