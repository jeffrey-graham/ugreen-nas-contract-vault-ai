#!/usr/bin/env python3
"""
Generates 1080p Architecture Diagram (`assets/architecture.png`) and
1080p H.264 MP4 Demo Video (`assets/ugreen_nas_demo.mp4`) for the
UGREEN Hackathon 2026 on AI NAS submission: `contract-invoice-vault-auditor`.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def draw_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    border_color: tuple[int, int, int],
    fill_color: tuple[int, int, int] = (15, 23, 42),
) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=14, fill=fill_color, outline=border_color, width=3)
    f_title = _load_font(23, bold=True)
    f_body = _load_font(18, bold=False)
    draw.text((x1 + 20, y1 + 16), title, fill=border_color, font=f_title)
    y = y1 + 54
    for line in lines:
        draw.text((x1 + 20, y), line, fill=(235, 242, 250), font=f_body)
        y += 28


def make_architecture_slide() -> Image.Image:
    img = Image.new("RGB", (1920, 1080), (7, 11, 20))
    draw = ImageDraw.Draw(img)

    f_h1 = _load_font(38, bold=True)
    f_sub = _load_font(22, bold=False)
    draw.text(
        (60, 40),
        "UGREEN AI NAS Contract & Invoice Vault Auditor (`contract-invoice-vault-auditor`)",
        fill=(16, 185, 129),
        font=f_h1,
    )
    draw.text(
        (60, 94),
        "UGREEN Hackathon 2026 on AI NAS ($46,000 Pool) | Uliya Standard v2.0.0 (`kimage-planb` full `main-agent`)",
        fill=(148, 163, 184),
        font=f_sub,
    )

    draw_box(
        draw,
        (60, 160, 520, 450),
        "Stage 1: Scope & SHA-256 (`file-agent`)",
        [
            "• file-workflow: get-user-dir",
            "• ug-filesystem: find, ls, stat",
            "• ug-filesystem: sha256sum digest",
            "• ug-filemgr: scan-dedupe (read-only)",
            "• Strict zero-match empty stop gate",
        ],
        border_color=(16, 185, 129),
    )

    draw_box(
        draw,
        (60, 480, 520, 770),
        "Stage 2: Receipt OCR/VLM (`photo-agent`)",
        [
            "• ug-photo: search-picture & search-screen",
            "• ug-photo: meta (EXIF & timestamps)",
            "• ug-photo: vision-ocr (receipt text)",
            "• ug-photo: vision-vlm (total, tax, ref)",
            "• 100% On-Device NPU Vision Parsing",
        ],
        border_color=(6, 182, 212),
    )

    draw_box(
        draw,
        (560, 160, 1340, 770),
        "Stage 3 & 4: Cross-Modal Reconciliation & Audio Evidence",
        [
            "[Stage 3: `document-agent` — Contract vs. Invoice vs. Receipt]",
            "  • ug-document: page-count, metadata, extract (clauses, caps, line items)",
            "  • ug-document: reconcile & qa (flags overbilling, tax errors, duplicates)",
            "       |",
            "[Stage 4: `knowledge-agent` — Verbal Change-Order Verification]",
            "  • ug-knowledge: audio-transcription on meeting/voice memos (.m4a/.mp3)",
            "  • ug-knowledge: collect-evidence matches verbal fee approvals (e.g. +$500 rush)",
            "  • ug-knowledge: save-text persists Markdown Audit & Reconciliation Ledger",
            "",
            "Validation: `check-skill.mjs` -> status: 'static-pass' (0 errors, 0 warnings)",
            "Privacy Guarantee: 0 Bytes Cloud Egress • 100% Local UGOS Pro Execution",
        ],
        border_color=(139, 92, 246),
    )

    draw_box(
        draw,
        (1380, 160, 1860, 450),
        "Stage 5: Vault Archive (`file-agent`)",
        [
            "• Enforces waiting_approval / waiting_user",
            "• ug-filemgr: tag-add & tag-add-file",
            "  - Verified-Match",
            "  - Variance-Flagged",
            "  - Duplicate-Candidate",
            "• file-workflow: batch-move to Vault",
        ],
        border_color=(245, 158, 11),
    )

    draw_box(
        draw,
        (1380, 480, 1860, 770),
        "Audit Benchmark & Deliverables",
        [
            "• Proposal PDF: 427 words (<=500 limit)",
            "• Pre-test ZIP: SKILL.md + 4 references",
            "• Catches $3,200 SHA-256 double billing",
            "• Verifies $500 verbal rush change order",
            "• Flags +$1,450 unapproved variance",
        ],
        border_color=(59, 130, 246),
    )

    draw.rounded_rectangle((60, 815, 1860, 995), radius=14, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.text(
        (90, 840),
        "UGREEN AI NAS Contract & Invoice Vault Auditor — Local Zero-Cloud FinOps & Legal Risk Engine",
        fill=(16, 185, 129),
        font=_load_font(26, bold=True),
    )
    draw.text(
        (90, 890),
        "Track: Automate Your Workflow | Target Hardware: UGREEN AI NAS iDX6011 Pro (64GB) on UGOS Pro",
        fill=(226, 232, 240),
        font=_load_font(21, bold=False),
    )
    draw.text(
        (90, 935),
        "Official Uliya Skill Kit v0.7.3 Validation: 0 Errors • 0 Warnings • 0 Info (`static-pass`)",
        fill=(52, 211, 153),
        font=_load_font(20, bold=True),
    )
    return img


def make_slide(title: str, subtitle: str, bullets: list[str], kpi_banner: str) -> Image.Image:
    img = Image.new("RGB", (1920, 1080), (7, 11, 20))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((60, 50, 1860, 190), radius=14, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    draw.text((95, 75), title, fill=(16, 185, 129), font=_load_font(36, bold=True))
    draw.text((95, 132), subtitle, fill=(148, 163, 184), font=_load_font(23, bold=False))

    draw.rounded_rectangle((60, 230, 1860, 840), radius=14, fill=(12, 18, 34), outline=(38, 54, 84), width=2)
    y = 275
    f_bullet = _load_font(25, bold=False)
    for b in bullets:
        draw.text((105, y), b, fill=(241, 245, 249), font=f_bullet)
        y += 64

    draw.rounded_rectangle((60, 880, 1860, 1010), radius=14, fill=(12, 36, 30), outline=(16, 185, 129), width=3)
    draw.text((95, 925), kpi_banner, fill=(52, 211, 153), font=_load_font(26, bold=True))
    return img


def main() -> None:
    arch_img = make_architecture_slide()
    arch_path = ASSETS_DIR / "architecture.png"
    arch_img.save(arch_path)

    slides = [
        arch_img,
        make_slide(
            "1. The Problem: Scattered NAS Billing Records & Cloud Privacy Risks",
            "Why freelancers, creative studios, and SMBs need a local-first FinOps auditor on UGREEN AI NAS",
            [
                "• Project contracts (PDF), vendor invoices, smartphone receipt photos, and voice memos live in scattered folders",
                "• Manual tax & client audit reconciliation takes hours and misses duplicate invoices across nested folders",
                "• Verbal change-order approvals recorded in meeting audio are forgotten during invoice review",
                "• Uploading confidential client contracts & bank wire screenshots to third-party cloud SaaS violates NDAs",
                "• Generic chatbots cannot safely orchestrate NAS file hashes, OCR/VLM, and approval-gated archiving",
            ],
            "Solution: 100% On-NAS Four-Way Cross-Modal Reconciliation on UGOS Pro (0 Bytes Cloud Egress)",
        ),
        make_slide(
            "2. Stages 1 & 2: Cryptographic Inventory (`file-agent`) & Receipt VLM (`photo-agent`)",
            "Strict upstream-to-downstream real-result handoffs using built-in UGOS registered experts",
            [
                "• Stage 1 (`file-agent`): Resolves user scope via `file-workflow` (`get-user-dir`) and enumerates files",
                "• Computes cryptographic `sha256sum` digests (`ug-filesystem`) & runs read-only `scan-dedupe` (`ug-filemgr`)",
                "• Enforces Empty-Result Gate: stops immediately on zero matches without fabricating paths",
                "• Stage 2 (`photo-agent`): Searches receipt albums via `ug-photo` (`search-picture`, `search-screen`)",
                "• Extracts merchant, date, tax, and paid totals locally via on-device `vision-ocr` and `vision-vlm`",
            ],
            "Cryptographic Integrity: Catches Identical SHA-256 Duplicate Invoices Before Payment",
        ),
        make_slide(
            "3. Stages 3 & 4: Contract Reconciliation (`document-agent`) & Audio Proof (`knowledge-agent`)",
            "Cross-checking PDF clauses against invoices, receipt totals, and transcribed voice memos",
            [
                "• Stage 3 (`document-agent`): Runs `page-count`, `metadata`, `extract`, `reconcile`, and `qa`",
                "• Compares signed contract caps & payment milestones against invoice line items and receipt payments",
                "• Stage 4 (`knowledge-agent`): Transcribes meeting audio via `ug-knowledge` (`audio-transcription`)",
                "• Runs `collect-evidence` to verify if flagged variances (e.g. +$500 rush fee) match verbal approvals",
                "• Compiles and saves the Markdown Audit & Reconciliation Ledger via `save-text` after approval",
            ],
            "Cross-Modal Intelligence: Links PDF Invoices + HEIC/PNG Receipts + M4A Voice Change Orders",
        ),
        make_slide(
            "4. Stage 5: Approval-Gated Semantic Tagging & Vault Organization (`file-agent`)",
            "Zero unapproved writes: strict `waiting_approval` and `waiting_user` state handling",
            [
                "• All write operations (`save-text`, `tag-add`, `tag-add-file`, `mkdir`, `cpmv`, `batch-move`) are gated",
                "• Applies semantic tags: `Verified-Match`, `Variance-Flagged`, and `Duplicate-Candidate`",
                "• Organizes verified records into structured NAS archive vault folders without deleting source files",
                "• Explicitly handles all 5 public states: `completed`, `waiting_user`, `waiting_approval`, `cancelled`, `failed`",
                "• Validated with official `uliya-skill-kit` v0.7.3 (`check-skill.mjs` -> 0 errors, 0 warnings, 0 info)",
            ],
            "Ready for UGREEN AI NAS iDX6011 Pro: Pre-test Skill Package ZIP + 427-Word Proposal PDF",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        concat_lines = []
        for idx, img in enumerate(slides):
            frame_path = tmp / f"slide_{idx:02d}.png"
            img.save(frame_path)
            concat_lines.append(f"file '{frame_path}'\n")
            concat_lines.append("duration 5\n")
        concat_lines.append(f"file '{tmp / f'slide_{len(slides)-1:02d}.png'}'\n")

        concat_file = tmp / "slides.txt"
        concat_file.write_text("".join(concat_lines), encoding="utf-8")

        out_mp4 = ASSETS_DIR / "ugreen_nas_demo.mp4"
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-vf",
            "fps=25,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "22",
            str(out_mp4),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Generated {arch_path} and {out_mp4} ({out_mp4.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
