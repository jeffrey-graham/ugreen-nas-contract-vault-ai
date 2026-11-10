# UGREEN Hackathon 2026 on AI NAS — Round 1 Project Proposal

- **Skill Name**: `contract-invoice-vault-auditor`
- **Track**: Automate Your Workflow *(also eligible for Open Innovation & Most Creative Skills Award)*
- **Target Platform**: UGREEN AI NAS (UGOS / Uliya `kimage-planb` full `main-agent` profile)
- **Substantive Word Count (Questions 1–10 Responses)**: **427 English words** *(strictly <= 500-word limit)*

---

## Substantive Responses (Questions 1–10)

### 1. One sentence: What does the Skill do?
`contract-invoice-vault-auditor` is a local-first UGREEN AI NAS Skill that reconciles project contracts, vendor invoices, receipt photos, and meeting voice memos into a SHA-256-verified audit ledger and approval-gated archive vault.

### 2. Who is the target user and problem?
Freelancers, studios, and small businesses store PDF contracts, invoices, receipt photos, and meeting recordings across scattered NAS folders. Reconciling billing before tax filing or audits takes hours, misses duplicate invoices, or forces uploading confidential records to cloud tools.

### 3. What is your proposed solution?
A five-stage Uliya workflow on UGREEN AI NAS that hashes and deduplicates project files, extracts receipt totals via local OCR and VLM, reconciles contract caps against invoices, verifies verbal change orders from audio recordings, saves a Markdown Audit Ledger, and tags/archives files after approval.

### 4. What is the Core User Flow?
The user provides a project folder and optional receipt album. The Skill inventories and hashes files, extracts receipt and document figures, reconciles totals against contracts and audio transcripts, pauses at approval prompts to save the Audit Ledger, and tags/archives verified or discrepant files.

### 5. Substantive difference vs. existing tools?
Cloud bookkeepers require uploading private contracts off-device and ignore voice memos or duplicates, while generic chatbots cannot safely orchestrate NAS storage. Our Skill performs four-way local reconciliation across documents, receipt photos, audio transcripts, and SHA-256 digests on-NAS with strict approval gates.

### 6. UGREEN AI NAS capabilities used at each step?
Stage 1 (`file-agent`): `file-workflow` (`get-user-dir`), `ug-filesystem` (`find`, `ls`, `stat`, `sha256sum`), `ug-filemgr` (`scan-dedupe`). Stage 2 (`photo-agent`): `ug-photo` (`search-picture`, `search-screen`, `meta`, `vision-ocr`, `vision-vlm`). Stage 3 (`document-agent`): `ug-document` (`page-count`, `metadata`, `extract`, `reconcile`, `qa`). Stage 4 (`knowledge-agent`): `ug-knowledge` (`audio-transcription`, `collect-evidence`, `save-text`). Stage 5 (`file-agent`): `ug-filemgr` (`tag-get-by-name`, `tag-add`, `tag-add-file`), `ug-filesystem` (`mkdir`, `cpmv`), `file-workflow` (`batch-move`).

### 7. What was your technical approach?
Following Uliya Standard v2.0.0 (`kimage-planb` full `main-agent`), `SKILL.md` delegates tasks to `file-agent`, `photo-agent`, `document-agent`, and `knowledge-agent`. Inputs are source folder, optional receipt album, and archive path. Read stages run first; write actions enforce `waiting_approval` and `waiting_user` gates. Local UGOS AI models process all data on-NAS.

### 8. What is the current development status?
Implemented in Round 1: `SKILL.md` entry point, five-stage delegation workflow, capability evidence mapping, state/error handling, and four reference guides (CLI matrix, schemas, test suite, security model), passing `check-skill.mjs` with zero errors or warnings (`static-pass`). Pending Round 2: live testing on UGREEN AI NAS iDX6011 Pro.

### 9. What is your final validation plan?
Core Test 1 validates four-way reconciliation across a contract PDF, two invoices (one with a 500 USD rush fee), two receipt photos, and a voice memo approving the fee. Core Test 2 validates SHA-256 duplicate detection across nested folders. Edge Case validates empty-folder stopping, corrupted PDF partial reporting, and cancelled approval recovery.

### 10. Known limitations, risks, or external dependencies?
Blurry receipt photos may lower `vision-ocr` accuracy, and noisy audio may reduce `audio-transcription` precision; the Skill mitigates both by flagging low-confidence items for manual review instead of guessing. Zero external runtime API dependencies exist, relying solely on built-in UGOS expert agents.

---

## Excluded Declarations & License Disclosures
*(Excluded from the 500-word limit per Section 4 of the Official Rules)*

### A. Entrant & Team Consent Declaration
- **Submission Type**: Individual Entrant (Representative: Jeffrey Graham / Jeffrey Graham Labs (Canada))
- **Consent & Originality Declaration**: I hereby declare that I am the sole author and authorized Representative of this Submission (`contract-invoice-vault-auditor`), that the Skill and its core workflow were newly developed during the UGREEN Hackathon 2026 on AI NAS submission period, and that I consent to the Official Rules of the Hackathon.
- **Electronic Signature**: `/s/ Jeffrey Graham` — Date: November 2026

### B. Third-Party Components, Open-Source Licenses & Data Flows
1. **Runtime Third-Party Dependencies & External Data Flows**: **None.** The Skill package (`contract-invoice-vault-auditor`) consists strictly of compliant Markdown orchestration files (`SKILL.md` and `references/*.md`), invokes only built-in UGOS registered expert agents (`file-agent`, `photo-agent`, `document-agent`, `knowledge-agent`), and performs zero external network calls or cloud data transfers.
2. **Official UGREEN Development Tools**: Built and validated using the official UGREEN `uliya-skill-kit` v0.7.3 (`capability-catalog.json` v2.0.0 and `scripts/check-skill.mjs`) provided in the UGREEN Hackathon Starter Kit under the UGREEN SkillHub User Agreement and Official Rules.
3. **Local Development Tooling**: Node.js v20+ (MIT License, OpenJS Foundation) used locally to run `check-skill.mjs`; Google Chrome Headless / Python 3 (BSD / PSF License) used locally to render this `project-proposal.pdf`.
4. **AI Tools Disclosure**: Claude Code / Antigravity AI coding assistant was used during development to inspect `capability-catalog.json`, format Markdown reference tables, and verify static compliance against `check-skill.mjs`. All architectural design, workflow logic, and proposal answers were human-directed and verified.
