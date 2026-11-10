# Structured Extraction Schemas & Audit Output Templates

This reference defines the structured extraction schemas and the final Markdown Audit & Reconciliation Ledger template used by `contract-invoice-vault-auditor`.

## 1. Document Extraction Schema (`document-agent` / `ug-document`)

When delegating to `document-agent` in Stage 3, instruct the expert to extract and normalize the following fields from each verified contract, purchase order, or invoice file:

```json
{
  "documentPath": "Workspace/Projects/2026-Q4-Alpha/INV-2026-1042.pdf",
  "documentRole": "vendor-invoice",
  "pageCount": 3,
  "counterpartyName": "Apex Precision Components LLC",
  "referenceId": "INV-2026-1042",
  "linkedContractId": "MSA-2026-089",
  "issueDate": "2026-10-28",
  "dueDate": "2026-11-27",
  "currency": "USD",
  "subtotalAmount": 14500.00,
  "taxRatePercent": 8.25,
  "taxAmount": 1196.25,
  "totalAmount": 15696.25,
  "lineItems": [
    {
      "itemCode": "CNC-STAGE-2",
      "description": "Precision enclosure machining batch 2",
      "quantity": 50,
      "unitPrice": 290.00,
      "lineTotal": 14500.00
    }
  ],
  "clauseCitations": [
    "Page 1, Section 4.2: Milestone 2 cap is 14,000.00 USD unless rush tooling is approved in writing or recorded project review."
  ]
}
```

## 2. Visual Receipt OCR/VLM Schema (`photo-agent` / `ug-photo`)

When delegating to `photo-agent` in Stage 2, instruct the expert to extract structured payment evidence from each matched receipt photo or banking screenshot:

```json
{
  "imagePath": "Albums/2026-Q4-Receipts/IMG_20261029_Wire_Confirmation.jpg",
  "captureTimestamp": "2026-10-29T16:14:08Z",
  "merchantOrPayee": "Apex Precision Components LLC",
  "paymentReference": "WIRE-994821-APC",
  "linkedInvoiceHint": "INV-2026-1042",
  "currency": "USD",
  "taxExtracted": 1196.25,
  "totalPaidAmount": 15696.25,
  "ocrConfidenceSummary": "High-clarity banking screenshot; all numeric totals verified by vision-ocr and vision-vlm."
}
```

## 3. Verbal Change-Order Evidence Schema (`knowledge-agent` / `ug-knowledge`)

When delegating to `knowledge-agent` in Stage 4 to check whether a flagged billing variance was verbally approved in a recorded meeting:

```json
{
  "audioPath": "Workspace/Projects/2026-Q4-Alpha/2026-10-24-Supplier-Sync.m4a",
  "language": "en-US",
  "speakerCount": 2,
  "matchedVarianceId": "VAR-001",
  "linkedInvoiceId": "INV-2026-1042",
  "transcriptExcerpt": "Speaker 1 (Project Lead): We approve the additional 500 USD rush tooling fee on Batch 2 bringing the subtotal to 14,500 USD.",
  "verificationStatus": "Verbal-Approval-Confirmed"
}
```

## 4. Reconciled Audit Ledger Template (`knowledge-agent` / `save-text`)

After workflow approval in Stage 4, `knowledge-agent` saves the final Audit & Reconciliation Ledger using the following Markdown template:

```markdown
# UGREEN AI NAS Cross-Modal Audit & Reconciliation Ledger

- **Audit Scope**: Workspace/Projects/2026-Q4-Alpha
- **Visual Receipt Scope**: Albums/2026-Q4-Receipts
- **Execution Mode**: Local-First Multi-Agent Orchestration (`kimage-planb` full `main-agent`)
- **Overall Status**: Completed (With 1 Variance Explained by Audio Evidence & 1 Duplicate File Flagged)

## 1. Cryptographic File Inventory & Duplicate Scan (`file-agent`)

| File Path | Role | Size (Bytes) | SHA-256 Digest | Duplicate Status | Proposed Tag |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Workspace/Projects/2026-Q4-Alpha/MSA-2026-089.pdf` | Contract | 418,920 | `8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4` | Unique | `Verified-Match` |
| `Workspace/Projects/2026-Q4-Alpha/INV-2026-1042.pdf` | Invoice | 215,040 | `2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae` | Unique | `Variance-Flagged` |
| `Workspace/Projects/2026-Q4-Alpha/INV-2026-1042-copy.pdf` | Invoice Copy | 215,040 | `2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae` | Duplicate of `INV-2026-1042.pdf` | `Duplicate-Candidate` |

## 2. Four-Way Cross-Modal Reconciliation Matrix (`document-agent` + `photo-agent` + `knowledge-agent`)

| Reference | Counterparty | Contract Cap | Invoice Total | Receipt Paid (`vision-ocr`) | Variance | Audio Change-Order Evidence | Final Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `INV-2026-1042` | Apex Precision Components LLC | 14,000.00 USD (Subtotal) | 14,500.00 USD Subtotal / 15,696.25 USD Total | 15,696.25 USD (`WIRE-994821-APC`) | +500.00 USD Subtotal | Confirmed in `2026-10-24-Supplier-Sync.m4a` (+500 USD rush tooling approved) | `Variance-Flagged` (Explained) |

## 3. Unresolved Exceptions & Partial Failures

- If any file failed extraction or lacked a matching receipt, list the exact file path, error code, and required manual follow-up here. (None in this run.)

## 4. Proposed Archive Vault Organization (Requires Explicit Approval)

- `Workspace/Projects/2026-Q4-Alpha/Audit-Vault/Verified/`
- `Workspace/Projects/2026-Q4-Alpha/Audit-Vault/Variance-Review/`
- `Workspace/Projects/2026-Q4-Alpha/Audit-Vault/Duplicate-Quarantine/`
```
