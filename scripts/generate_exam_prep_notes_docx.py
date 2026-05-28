#!/usr/bin/env python3
"""Generate Academic Exam-Ready Notes DOCX from an ExamPrepNotesPlan."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any

try:
    from docx import Document  # type: ignore
    from docx.enum.text import WD_ALIGN_PARAGRAPH  # type: ignore
    from docx.oxml.ns import qn  # type: ignore
    from docx.shared import Cm, Pt, RGBColor  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"python-docx is required: {exc}")


FORBIDDEN_PUBLIC_PHRASES = [
    "Course-Level Exam Map",
    "assessment includes",
    "summative examination",
    "Section A asks",
    "Section B is",
    "Coverage note:",
    "no mark scheme",
    "historical papers",
    "older papers",
    "current regime",
    "ELM should be checked",
    "source coverage",
    "extraction quality",
]


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_run(run) -> None:
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 0, 0)
    if run._element.rPr is not None:
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")


def normalize_paragraph(paragraph, kind: str) -> None:
    paragraph.paragraph_format.line_spacing = 1.5
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if kind == "title" else WD_ALIGN_PARAGRAPH.LEFT if kind == "heading" else WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in paragraph.runs:
        normalize_run(run)


def set_document_defaults(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    for style_name in ["Normal", "EPNTitle", "EPNHeading", "EPNBody"]:
        if style_name not in doc.styles:
            doc.styles.add_style(style_name, 1)
        style = doc.styles[style_name]
        style.font.name = "Arial"
        style.font.size = Pt(11)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.line_spacing = 1.5


def add_marked_text(paragraph, text: str) -> None:
    for part in re.split(r"(\*\*[^*]+\*\*)", str(text)):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            run = paragraph.add_run(part)
        normalize_run(run)


def add_paragraph(doc: Document, text: str, kind: str = "body"):
    style = {"title": "EPNTitle", "heading": "EPNHeading", "body": "EPNBody"}[kind]
    paragraph = doc.add_paragraph(style=style)
    add_marked_text(paragraph, text)
    if kind in {"title", "heading"}:
        for run in paragraph.runs:
            run.bold = True
    normalize_paragraph(paragraph, kind)
    return paragraph


def add_label_block(doc: Document, label: str, value: Any) -> None:
    if value in (None, "", [], {}):
        return
    add_paragraph(doc, f"{label}:", "heading")
    if isinstance(value, list):
        for item in value:
            add_paragraph(doc, f"- {item}", "body")
    else:
        add_paragraph(doc, str(value), "body")


def visible_text_from_plan(plan: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ["title", "course_knowledge_map"]:
        if plan.get(key):
            parts.append(str(plan[key]))
    for section in plan.get("course_sections", []):
        parts.extend(str(section.get(key, "")) for key in ["section_title", "section_function"])
    for card in plan.get("knowledge_cards", []):
        if not card.get("student_visible", True):
            continue
        visible_keys = [
            "module_title",
            "priority",
            "exam_specificity",
            "core_exam_claim",
            "key_definitions",
            "exam_ready_knowledge_synthesis",
            "criteria_components_steps",
            "mechanism_or_process_logic",
            "canonical_example",
            "exam_use",
            "common_error_or_trap",
            "must_master",
        ]
        for key in visible_keys:
            parts.append(json.dumps(card.get(key, ""), ensure_ascii=False))
    return "\n".join(parts)


def validate_plan(plan: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if plan.get("object_type") != "ExamPrepNotesPlan":
        failures.append("plan_object_type_not_exam_prep_notes_plan")
    cards = [card for card in plan.get("knowledge_cards", []) if card.get("student_visible", True)]
    if not cards:
        failures.append("no_student_visible_knowledge_cards")
    if not plan.get("knowledge_only_student_view_binding"):
        failures.append("missing_knowledge_only_student_view_binding")
    for card in cards:
        for field in ["module_title", "priority", "exam_specificity", "core_exam_claim", "exam_ready_knowledge_synthesis", "must_master"]:
            if not card.get(field):
                failures.append(f"visible_card_missing_{field}:{card.get('card_id', 'unknown')}")
        if card.get("priority") not in {"★★★", "★★", "★"}:
            failures.append(f"visible_card_bad_priority:{card.get('card_id', 'unknown')}")
    visible_text = visible_text_from_plan(plan)
    for phrase in FORBIDDEN_PUBLIC_PHRASES:
        if phrase.lower() in visible_text.lower():
            failures.append(f"forbidden_public_phrase:{phrase}")
    return sorted(set(failures))


def write_docx(plan: dict[str, Any], output_dir: Path, qa_dir: Path, strict: bool) -> dict[str, Any]:
    failures = validate_plan(plan)
    if strict and failures:
        return {"status": "fail", "qa_flags": failures, "documents": []}

    doc = Document()
    set_document_defaults(doc)
    title = str(plan.get("title") or "Academic Exam-Ready Knowledge Notes")
    add_paragraph(doc, title, "title")
    add_paragraph(doc, "Academic Exam-Ready Knowledge Notes", "title")

    add_paragraph(doc, "Course Knowledge Map", "heading")
    course_map = plan.get("course_knowledge_map")
    if course_map:
        add_paragraph(doc, str(course_map), "body")
    else:
        add_paragraph(doc, "The notes are organised by source-backed knowledge sections and modules.", "body")

    if plan.get("course_sections"):
        add_paragraph(doc, "Knowledge Sections", "heading")
        for section in plan.get("course_sections", []):
            title_text = section.get("section_title", "Knowledge Section")
            function = section.get("section_function", "")
            add_paragraph(doc, f"{title_text}: {function}", "body")

    if plan.get("lecture_mapping"):
        add_paragraph(doc, "Lecture Coverage", "heading")
        for lecture in plan.get("lecture_mapping", []):
            add_paragraph(doc, f"{lecture.get('title', 'Lecture')}", "body")

    for card in plan.get("knowledge_cards", []):
        if not card.get("student_visible", True):
            continue
        add_paragraph(doc, f"Module: {card.get('module_title', 'Knowledge Module')}", "heading")
        add_paragraph(doc, f"Priority: {card.get('priority', '')}", "body")
        add_label_block(doc, "Exam Specificity", card.get("exam_specificity"))
        add_label_block(doc, "Core Exam Claim", card.get("core_exam_claim"))
        add_label_block(doc, "Key Definitions", card.get("key_definitions"))
        add_label_block(doc, "Exam-Ready Knowledge Synthesis", card.get("exam_ready_knowledge_synthesis"))
        add_label_block(doc, "Criteria / Components / Steps", card.get("criteria_components_steps"))
        add_label_block(doc, "Mechanism / Process Logic", card.get("mechanism_or_process_logic"))
        add_label_block(doc, "Canonical Example", card.get("canonical_example"))
        add_label_block(doc, "Exam Use", card.get("exam_use"))
        add_label_block(doc, "Common Error / Trap", card.get("common_error_or_trap"))
        add_label_block(doc, "Must Master", card.get("must_master"))

    output_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)
    docx_path = output_dir / "Lecture_Knowledge_Walkthrough.docx"
    doc.save(docx_path)
    manifest = {
        "status": "pass" if not failures else "warn",
        "notes_plan_id": plan.get("notes_plan_id"),
        "target_group_key": plan.get("target_group_key"),
        "qa_flags": failures,
        "documents": [{"docx_path": str(docx_path), "filename": docx_path.name}],
    }
    (qa_dir / "exam_prep_notes_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--qa-dir", type=Path)
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--deliverable-only", action="store_true")
    args = parser.parse_args()

    output_dir = args.output_dir
    qa_dir = args.qa_dir or (output_dir if not args.deliverable_only else output_dir.parent / "exam_prep_notes_internal_qa")
    if args.clean:
        if output_dir.exists():
            shutil.rmtree(output_dir)
        if qa_dir.exists() and qa_dir != output_dir:
            shutil.rmtree(qa_dir)

    result = write_docx(load_plan(args.plan), output_dir, qa_dir, args.strict)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") in {"pass", "warn"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
