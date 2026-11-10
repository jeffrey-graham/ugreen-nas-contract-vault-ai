# Validation Plan, Test Cases & Edge-Case Recovery

This reference specifies the Round 2 target-device validation protocol on the UGREEN AI NAS iDX6011 Pro (64GB) environment, covering two core end-to-end test cases, one adversarial edge case, and deterministic recovery rules for every delegation status.

## 1. Core Test Case 1: Four-Way Multi-Modal Reconciliation & Approved Vault Archiving

- **Objective**: Verify that `contract-invoice-vault-auditor` accurately reconciles a master service contract PDF, three vendor invoice PDFs, two photographed payment receipts in NAS Photos, and one meeting voice recording, then saves the Audit Ledger and organizes tagged files after user approval.
- **Synthetic Test Dataset**:
  - `Workspace/Test-Suite-TC1/Contracts/MSA-2026-Alpha.pdf` (Milestone 1: 5,000 USD; Milestone 2: 14,000 USD).
  - `Workspace/Test-Suite-TC1/Invoices/INV-101.pdf` (5,000 USD, exact match) and `INV-102.pdf` (14,500 USD subtotal, +500 USD rush tooling variance).
  - `Albums/Test-Suite-TC1-Receipts/Receipt-101.jpg` (5,000 USD paid) and `Receipt-102.png` (14,500 USD subtotal paid).
  - `Workspace/Test-Suite-TC1/Audio/2026-10-24-Change-Order.m4a` (60-second synthetic voice memo approving the 500 USD rush tooling fee on `INV-102`).
- **Expected Execution & Verification**:
  1. `file-agent` enumerates all 4 workspace files, returns their exact `sha256sum` digests, and confirms zero duplicates (`completed`).
  2. `photo-agent` locates both receipt images via `search-picture` / `search-screen` and extracts exact payment amounts via `vision-ocr` and `vision-vlm` (`completed`).
  3. `document-agent` runs `metadata`, `page-count`, `extract`, and `reconcile`, confirming `INV-101` as an exact match and flagging the +500 USD variance on `INV-102` (`completed`).
  4. `knowledge-agent` transcribes `2026-10-24-Change-Order.m4a` via `audio-transcription`, correlates the verbal approval via `collect-evidence`, requests workflow approval (`waiting_approval`), and writes the Markdown Audit Ledger via `save-text` (`completed`).
  5. `file-agent` requests gateway/workflow approval (`waiting_approval`), attaches `Verified-Match` to `MSA-2026-Alpha.pdf` and `INV-101.pdf` and `Variance-Flagged` to `INV-102.pdf`, creates the archive folders via `mkdir`, and copies the files via `cpmv` (`completed`).

## 2. Core Test Case 2: Non-Destructive Cryptographic Duplicate Detection & Overbilling Catch

- **Objective**: Verify that byte-identical and renamed duplicate invoices across nested project directories are detected before reconciliation, preventing double-counting and isolating duplicates non-destructively.
- **Synthetic Test Dataset**:
  - `Workspace/Test-Suite-TC2/Incoming/INV-2026-880.pdf` (8,200 USD).
  - `Workspace/Test-Suite-TC2/Incoming/Subfolder/INV-2026-880-resent.pdf` (byte-identical copy of `INV-2026-880.pdf` with identical SHA-256 digest).
  - `Workspace/Test-Suite-TC2/Incoming/INV-2026-881.pdf` (unapproved 1,200 USD surcharge with no matching contract clause or audio memo).
- **Expected Execution & Verification**:
  1. `file-agent` runs `sha256sum` and `scan-dedupe`, grouping `INV-2026-880.pdf` and `INV-2026-880-resent.pdf` under one SHA-256 digest without deleting either file.
  2. `document-agent` deduplicates the identical file from billing totals so the 8,200 USD invoice is counted once, while flagging `INV-2026-881.pdf` as an unapproved overbilling variance.
  3. After approval, `file-agent` tags `INV-2026-880-resent.pdf` with `Duplicate-Candidate` and moves it to the approved `Duplicate-Quarantine` archive directory while keeping `INV-2026-880.pdf` intact.

## 3. Edge Case: Empty Directory, Corrupted/Encrypted Document, or Denied Approval

- **Scenario A — Empty Scope (`zero matches`)**:
  - **Trigger**: User requests an audit on `Workspace/Empty-Folder-2026` where no files match.
  - **Expected Behavior**: Stage 1 (`file-agent`) returns an empty list (`no results`). The parent Skill reports the empty result immediately and halts Stages 2–5 without scanning unrelated folders or inventing sample data.
- **Scenario B — Partially Unreadable Batch (Corrupted or Password-Locked PDF)**:
  - **Trigger**: Batch contains 3 valid invoices and 1 corrupted or password-locked file (`INV-locked.pdf`).
  - **Expected Behavior**: `document-agent` processes the 3 readable documents and reports a targeted extraction error for `INV-locked.pdf`. The Audit Ledger preserves the verified reconciliation for the 3 valid files and lists `INV-locked.pdf` in the Unresolved Exceptions section without fabricating its contents.
- **Scenario C — Mid-Workflow Approval Denial (`cancelled` after `waiting_approval`)**:
  - **Trigger**: User reviews the reconciliation report and declines the Stage 5 archive move approval prompt.
  - **Expected Behavior**: Stage 5 transitions from `waiting_approval` to `cancelled`. All source files remain untouched in their original directories, and the Skill outputs the completed read-only reconciliation findings alongside a clear notice that tagging and archiving were cancelled by the user.

## 4. Delegation State Handling Matrix

| Delegation Status | Parent Skill Action | Downstream Impact | User-Facing Feedback |
| :--- | :--- | :--- | :--- |
| `completed` | Validate returned paths, digests, or extracted fields. | Pass verified business output to the next dependent stage. | Present stage progress or final verified Audit Summary. |
| `waiting_user` | Pause orchestration and surface the clarifying prompt. | Hold dependent delegations until user responds. | Ask the user for the missing scope, disambiguation, or confirmation. |
| `waiting_approval` | Pause at the gateway or workflow approval boundary. | Do not invoke subsequent write/tag/move steps yet. | Explain which files/paths require approval and why. |
| `cancelled` | Terminate active and dependent write steps cleanly. | Preserve prior `completed` read/ledger outputs. | Report completed stages and confirm that cancelled actions made no changes. |
| `failed` | Record diagnostic error and affected file paths. | Halt steps that depend on the failed output; preserve partial batch results. | Report the exact failure cause and remediation steps honestly. |
