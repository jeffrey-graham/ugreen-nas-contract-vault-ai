# Security, Permission Model & Hackathon Disclosures

This reference documents the data security architecture, permission boundaries, third-party/open-source disclosures, principal newly developed functionality, and AI tool disclosures for `contract-invoice-vault-auditor`.

## 1. Local-First Privacy & Permission Architecture

1. **100% On-NAS Data Residency**: All file discovery (`ug-filesystem`), duplicate analysis (`ug-filemgr`), optical character recognition and visual understanding (`ug-photo` `vision-ocr` and `vision-vlm`), contract/invoice extraction and reconciliation (`ug-document`), and meeting audio transcription (`ug-knowledge` `audio-transcription`) execute through Uliya's registered expert agents on the UGREEN AI NAS (`kimage-planb` full `main-agent` profile). No user files, financial figures, or audio transcripts are transmitted to unauthorized external endpoints.
2. **Scope Confinement**: `file-agent` resolves authorized user directories via `file-workflow` (`get-user-dir`) and restricts all `find`, `ls`, `stat`, `sha256sum`, and `scan-dedupe` operations strictly to the folder scope explicitly requested by the user.
3. **Mandatory Approval Gates for State Changes**:
   - Stages 1, 2, and 3 are strictly read-only (`approval=none`).
   - Stage 4 (`ug-knowledge` `save-text`) requires `workflow` approval before writing the Markdown Audit Ledger.
   - Stage 5 (`ug-filemgr` `tag-add`, `tag-set`, `tag-add-file`, `ug-filesystem` `mkdir`, `cpmv`, and `file-workflow` `batch-move`) requires explicit `gateway`, `conditional`, or `workflow` approval plus user confirmation.
4. **Non-Destructive Default Policy**: Duplicate detection (`scan-dedupe` and `sha256sum`) never deletes files (`del` or `batch-del` are excluded from the default workflow). Duplicate candidates are reported in the Audit Ledger and, only after explicit user confirmation, tagged with `Duplicate-Candidate` and organized into a quarantine archive folder.
5. **Zero Embedded Secrets or Scripts**: The Skill package contains pure Markdown orchestration instructions (`SKILL.md` and `references/*.md`), with zero executable scripts, zero binaries, and zero hardcoded credentials or personal paths.

## 2. Hackathon Disclosures (Official Rules Compliance)

### A. Principal Functionality Newly Developed for This Hackathon

The entire `contract-invoice-vault-auditor` Skill package—including its 5-stage multi-agent orchestration architecture (`SKILL.md`), cross-modal contract-invoice-receipt-audio reconciliation workflow, cryptographic SHA-256 duplicate auditing pipeline, approval-gated vault tagging model, structured extraction schemas ([references/schema-and-output-templates.md](references/schema-and-output-templates.md)), capability matrix ([references/cli-command-matrix.md](references/cli-command-matrix.md)), and validation test suite ([references/test-cases-and-edge-recovery.md](references/test-cases-and-edge-recovery.md))—was newly conceived, designed, and authored specifically during the UGREEN Hackathon 2026 on AI NAS submission period. No pre-existing Skill packages or prior hackathon submissions were reused.

### B. Official Platform Tools & Open-Source / Third-Party Components

| Component / Resource | Source / Provider | License / Terms | Usage in Project |
| :--- | :--- | :--- | :--- |
| **UGOS Skill Creation Tool (`uliya-skill-kit` v0.7.3)** | UGREEN Official Hackathon Starter Kit (`ai.ugreen.com/pages/hackathon-starter-kit`) | UGREEN SkillHub User Agreement & Hackathon Official Rules | Used during development for capability catalog verification (`capability-catalog.json` v2.0.0) and static compliance checking (`check-skill.mjs`). Not bundled inside the submitted Skill ZIP. |
| **Node.js Runtime (v20+)** | OpenJS Foundation (`nodejs.org`) | MIT License | Used locally during development only to execute the official `uliya-skill-kit` static checker (`check-skill.mjs`). |
| **Python 3 & ReportLab / Chromium PDF Renderer** | Python Software Foundation / ReportLab Inc. | PSF License / BSD-3-Clause License | Used locally during development only to render the Round 1 `project-proposal.pdf` submission document. |
| **Runtime External / Third-Party SDKs inside Skill** | None | N/A | The submitted Skill package (`contract-invoice-vault-auditor`) has zero external third-party runtime code dependencies and relies exclusively on built-in UGOS registered expert agents (`file-agent`, `photo-agent`, `document-agent`, `knowledge-agent`). |

### C. AI Tools Used & Principal Uses Disclosure

| AI Tool / Assistant | Principal Use During Development | Human Oversight & Authorship |
| :--- | :--- | :--- |
| **Claude Code / Antigravity AI Coding Assistant** | Used to inspect the `uliya-skill-kit` v0.7.3 capability catalog (`capability-catalog.json`), verify CLI parameter names and approval rules, format Markdown tables, and run iterative static validation checks against `check-skill.mjs`. | The core cross-modal audit concept, 5-stage orchestration design, test cases, and proposal responses were directed, reviewed, and verified for accuracy and rule compliance. |
