# UGREEN $46,000 AI NAS Hackathon — Round 1 60-Second Submission Guide

- **Hackathon Portal**: [https://ugreenhackathon.devpost.com/](https://ugreenhackathon.devpost.com/)
- **Round 1 Deadline**: Sunday, November 15, 2026 @ 11:45 PM PT
- **Prize Pool**: $46,000 USD in Cash ($20,000 Gold, $10,000 Silver, $6,000 Bronze, 2x $5,000 Most Creative Skills)
- **Live Interactive Demo (GitHub Pages)**: [https://jeffrey-graham.github.io/ugreen-nas-contract-vault-ai/](https://jeffrey-graham.github.io/ugreen-nas-contract-vault-ai/)
- **GitHub Repository**: [https://github.com/jeffrey-graham/ugreen-nas-contract-vault-ai](https://github.com/jeffrey-graham/ugreen-nas-contract-vault-ai)
- **1080p Demo Video (MP4)**: `/home/jeff/.gemini/antigravity/scratch/freelancework/ugreen-ai-nas-hackathon/assets/ugreen_nas_demo.mp4`
- **Validation Status**: `status: "static-pass"` (`0 errors, 0 warnings, 0 info` on official UGREEN `uliya-skill-kit` v0.7.3 `check-skill.mjs`)

---

## 1. Ready-to-Upload Files (In This Folder)

1. **Project Proposal (PDF)**:
   - Path: `/home/jeff/.gemini/antigravity/scratch/freelancework/ugreen-ai-nas-hackathon/project-proposal.pdf`
   - Size: **136 KB** *(Limit: <= 1 MB)*
   - Word Count: **427 English words** across the 10 substantive responses *(Limit: <= 500 English words)* + Excluded Consent & Open-Source/AI Disclosures.
2. **Pre-test Skill Package (ZIP)**:
   - Path: `/home/jeff/.gemini/antigravity/scratch/freelancework/ugreen-ai-nas-hackathon/pretest-skill-package.zip` *(also saved as `contract-invoice-vault-auditor.zip`)*
   - Size: **15 KB** *(Limit: <= 10 MB total, <= 1 MB per file)*
   - Contents:
     - `contract-invoice-vault-auditor/SKILL.md` (13.7 KB)
     - `contract-invoice-vault-auditor/references/cli-command-matrix.md` (7.4 KB)
     - `contract-invoice-vault-auditor/references/test-cases-and-edge-recovery.md` (6.2 KB)
     - `contract-invoice-vault-auditor/references/security-and-permission-model.md` (5.1 KB)
     - `contract-invoice-vault-auditor/references/schema-and-output-templates.md` (5.1 KB)

---

## 2. Step-by-Step Devpost Form Copy-Paste Values

### Step 1: Register & Start Submission
1. Open [https://ugreenhackathon.devpost.com/](https://ugreenhackathon.devpost.com/) and click **Join hackathon** / **Enter a Submission**.

### Step 2: Project Overview Fields

- **Project Name**:
  ```text
  contract-invoice-vault-auditor
  ```
- **Elevator Pitch / Tagline** *(<= 200 characters)*:
  ```text
  Local-first UGREEN AI NAS Skill that reconciles contracts, invoices, receipt photos, and meeting voice memos into a SHA-256-verified audit ledger and approval-gated archive vault.
  ```
- **Track Selection**:
  ```text
  Automate Your Workflow
  ```
  *(Note: All tracks compete for Gold/Silver/Bronze and the two $5,000 Most Creative Skills Awards.)*

- **Built With Tags**:
  ```text
  ugreen-ai-nas, ugos, uliya-skill-kit, markdown, multi-agent-orchestration, ocr, vlm, document-ai
  ```

### Step 3: Full Project Description ("About the Project" Markdown Box)

Copy and paste the block below into the Devpost **Project Story / Description** field:

```markdown
## Inspiration
Freelancers, creative studios, and small businesses store PDF contracts, vendor invoices, smartphone receipt photos, and recorded client/supplier voice memos across scattered NAS folders. Reconciling project billing before tax filing or client audits takes hours of manual cross-checking, catches duplicate invoices too late, or forces users to upload confidential contracts and bank receipts to third-party cloud SaaS tools.

## What it does
`contract-invoice-vault-auditor` is a local-first UGREEN AI NAS orchestration Skill built to the Uliya Skill Development Standard v2.0.0 (`kimage-planb` full `main-agent` profile). It performs **four-way cross-modal reconciliation** across documents, receipt photos, meeting audio recordings, and SHA-256 file hashes entirely on-NAS:
1. **Stage 1 — Scope Discovery, Cryptographic Inventory & Duplicate Scan (`file-agent`)**: Resolves authorized workspace directories (`file-workflow` `get-user-dir`), computes `sha256sum` digests (`ug-filesystem`), and scans for duplicate invoices (`ug-filemgr` `scan-dedupe`) without deleting files.
2. **Stage 2 — Visual Receipt & Screenshot OCR/VLM Extraction (`photo-agent`)**: Searches NAS photo/screenshot albums (`ug-photo` `search-picture`, `search-screen`) and extracts payment totals, taxes, dates, and wire references via on-device `vision-ocr` and `vision-vlm`.
3. **Stage 3 — Multi-Document Extraction & Reconciliation (`document-agent`)**: Reads `page-count` and `metadata`, extracts structured clauses and line items (`ug-document` `extract`), and reconciles contract caps against invoice totals and receipt payments (`reconcile`, `qa`).
4. **Stage 4 — Verbal Change-Order Verification & Audit Ledger Persistence (`knowledge-agent`)**: Transcribes meeting recordings (`ug-knowledge` `audio-transcription`), correlates verbal fee approvals (`collect-evidence`), and saves a Markdown Audit & Reconciliation Ledger (`save-text`) after workflow approval.
5. **Stage 5 — Approval-Gated Semantic Tagging & Vault Archiving (`file-agent`)**: Strictly after user and gateway/workflow approval (`waiting_approval` / `waiting_user`), attaches semantic audit tags (`Verified-Match`, `Variance-Flagged`, `Duplicate-Candidate`) via `ug-filemgr` and organizes files into structured vault folders via `ug-filesystem` (`mkdir`, `cpmv`) and `file-workflow` (`batch-move`).

## How we built it
We designed `contract-invoice-vault-auditor` using the official UGREEN `uliya-skill-kit` v0.7.3 and verified every capability against `capability-catalog.json` (v2.0.0). The package includes `SKILL.md` and four directly linked reference specifications (`cli-command-matrix.md`, `schema-and-output-templates.md`, `test-cases-and-edge-recovery.md`, and `security-and-permission-model.md`), passing `scripts/check-skill.mjs` with `"status": "static-pass"` (0 errors, 0 warnings, 0 info).

## Challenges we ran into
Designing a multi-agent workflow that chains four distinct experts (`file-agent`, `photo-agent`, `document-agent`, `knowledge-agent`) while guaranteeing strict upstream-to-downstream real-result handoffs, explicit empty-result (`zero matches`) termination, partial-batch failure isolation, and mandatory `waiting_approval` boundaries before any state-changing operation.

## Accomplishments that we're proud of
- **Four-way cross-modal verification** (PDF contracts/invoices + OCR/VLM receipt photos + transcribed voice memos + SHA-256 deduplication) 100% locally on UGREEN AI NAS.
- **Zero-error, zero-warning `static-pass`** on the official UGREEN `uliya-skill-kit` validator.

## What's next for contract-invoice-vault-auditor
In Round 2, we will validate the full 5-stage workflow on the assigned UGREEN AI NAS iDX6011 Pro (64GB) environment across our synthetic multi-modal contract/invoice/receipt/audio test suites and record the 3-minute live runtime demonstration video.
```

### Step 4: Upload the Two Required Files
1. Upload **`project-proposal.pdf`** (`136 KB`) to the **Project Proposal (PDF)** upload slot.
2. Upload **`pretest-skill-package.zip`** (`15 KB`) to the **Pre-test Skill Package (ZIP)** upload slot.
   *(Note: Round 1 does NOT require a NAS device, external code repository link, or demo video link.)*
3. Click **Save & Submit** before **November 15, 2026 @ 11:45 PM PT**.
