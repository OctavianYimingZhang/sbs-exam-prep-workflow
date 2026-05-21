#!/usr/bin/env python3
"""Read-only source inventory and text extraction for SBS exam workflow inputs."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover
    fitz = None

try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover
    PdfReader = None

try:
    from docx import Document  # type: ignore
except Exception:  # pragma: no cover
    Document = None


TEXT_EXTS = {".txt", ".md", ".markdown", ".yaml", ".yml", ".py", ".json", ".csv", ".tsv"}
SUPPORTED_EXTS = TEXT_EXTS | {".pdf", ".docx", ".pptx", ".ppsx"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".heic"}


@dataclass
class ExtractedFile:
    path: str
    name: str
    extension: str
    role: str
    unit_code: str | None
    unit_name: str | None
    year: int | None
    source_trust_level: str
    evidence_use: str
    analysis_context: str
    allowed_factual_use: bool
    allowed_prediction_use: bool
    allowed_style_use: bool
    allowed_layout_use: bool
    allowed_transferable_example_use: bool
    status: str
    method: str
    text_path: str | None
    char_count: int
    page_count: int | None = None
    slide_count: int | None = None
    image_count: int | None = None
    limitations: list[str] = field(default_factory=list)
    preview: str = ""


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
        else:
            files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def detect_year(path: Path, text: str, role: str | None = None) -> int | None:
    filename_matches = re.findall(r"\b(20\d{2}|19\d{2})\b", path.name)
    if filename_matches:
        return int(filename_matches[-1])

    # Lecture decks often contain citation/reference years in slide text. Do
    # not treat those as source years; use metadata or explicit file names in
    # downstream code if a lecture-source year is required.
    if role in {"lecture_slide", "lecture_note", "annotated_lecture_slide", "essay_guidance"}:
        return None

    header = text[:3000]
    contextual = re.findall(
        r"(?:examination|exam|paper|assessment|semester|academic year|year)\D{0,80}\b(20\d{2}|19\d{2})\b",
        header,
        flags=re.IGNORECASE,
    )
    if contextual:
        return int(contextual[-1])
    return None


def detect_unit(path: Path, text: str, unit_hint: str | None) -> tuple[str | None, str | None]:
    haystack = (str(path) + "\n" + text[:5000]).lower()
    # These aliases support regression examples and filename normalization only.
    # They must not control question-type routing, prediction, or output mode.
    patterns = [
        ("BIOL21332", "Motor Systems", ["biol21332", "motor system", "motor systems"]),
        ("BIOL21172", "Principles of Developmental Biology", ["biol21172", "principles of developmental biology"]),
        ("BIOL21101", "Genome Maintenance and Regulation", ["biol21101", "genome maintenance", "genome maintenance and regulation"]),
        ("BIOL21111", "Proteins", ["biol21111", "proteins"]),
        ("BIOL21202", "Plants for the Future", ["biol21202", "plants for the future"]),
        ("BIOL21451", "How to Make a Brain", ["biol21451", "how to make a brain"]),
        ("BIOL21242", "Immunology", ["biol21242", "immunology"]),
    ]
    if unit_hint:
        hint = unit_hint.lower()
        for code, name, needles in patterns:
            if hint in {code.lower(), name.lower()} or any(needle in hint for needle in needles):
                return code, name
    for code, name, needles in patterns:
        if any(needle in haystack for needle in needles):
            return code, name
    generic_code = re.search(r"\b([a-z]{4}\d{5}[a-z]?)\b", haystack, flags=re.IGNORECASE)
    if generic_code:
        return generic_code.group(1).upper(), None
    return (unit_hint, None) if unit_hint else (None, None)


def detect_role(path: Path, text: str, unit_hint: str | None = None) -> str:
    name = path.name.lower()
    path_text = str(path).lower()
    suffix = path.suffix.lower()
    body = (name + "\n" + text[:4000].lower())
    if suffix in IMAGE_EXTS:
        if "lecture" in name or "slide" in name:
            return "annotated_lecture_slide"
        exemplar_terms = (
            "exemplar",
            "model",
            "answer",
            "essay",
            "draft",
            "example",
            "handwritten",
            "rewrite",
        )
        if any(term in body or term in path_text for term in exemplar_terms):
            return "exemplar_image"
        # Hashed WeChat/RWTemp images supplied alongside a single unit are
        # usually handwritten answer examples. Keep them style-only; factual
        # claims still require lecture/source verification.
        if unit_hint and ("xwechat_files" in path_text or "rwtemp" in path_text):
            return "exemplar_image"
        return "unknown"
    if suffix in {".py", ".js", ".mjs", ".sh"}:
        return "helper_script"
    if suffix in {".yaml", ".yml", ".json"}:
        return "source_policy" if "policy" in name else "output_protocol" if "protocol" in name else "helper_script"
    if suffix in {".pptx", ".ppsx"}:
        if any(term in name for term in ("essay writing", "tutorial", "exam guidance", "course information", "course info")):
            return "essay_guidance"
        if any(term in name for term in ("quiz", "spotter", "formative", "practice", "mock", "problem sheet")):
            return "mock_exam" if "mock" in name else "practice_paper"
        return "lecture_slide"
    if ("past paper" in path_text or "past papers" in path_text) and re.search(r"\b(20\d{2}|19\d{2})\b", name):
        return "formal_past_paper"
    if any(term in body for term in ("marking criteria", "rubric", "criteria for marking")):
        return "marking_criteria"
    if any(term in body for term in ("exemplar", "model answer", "example answer")):
        return "exemplar_answer"
    if any(term in body for term in ("course information", "course info", "exam guidance", "assessment guidance")):
        return "essay_guidance"
    if any(term in body for term in ("quiz", "spotter", "formative", "practice question", "practice material", "problem sheet", "mcq", "multiple choice", "tutorial")) and not any(
        term in body for term in ("examination", "answer one question", "answer all questions", "section b")
    ):
        return "practice_paper"
    if any(term in body for term in ("examination", "answer one question", "answer all questions", "section a", "section b", "do not turn over")):
        return "formal_past_paper"
    if suffix == ".pdf" and any(term in body for term in ("lecture", "module", "learning objectives", "motor systems", "slide")):
        return "lecture_slide"
    if any(term in name for term in ("notes", "summary", "revision")):
        return "lecture_note"
    return "unknown"


def trust_and_evidence(role: str) -> tuple[str, str]:
    if role in {"lecture_slide", "lecture_note", "annotated_lecture_slide"}:
        return "official_course", "factual_course_content"
    if role == "formal_past_paper":
        return "official_course", "formal_prediction_evidence"
    if role in {"practice_paper", "mock_exam", "answer_key"}:
        return "course_adjacent", "coverage_evidence_only"
    if role in {"exemplar_answer", "exemplar_image"}:
        return "course_adjacent", "answer_style_only"
    if role in {"marking_criteria", "essay_guidance"}:
        return "official_course", "format_rule"
    if role in {"source_policy", "output_protocol", "helper_script"}:
        return "course_adjacent", "excluded"
    return "unsupported" if role == "unsupported_binary" else "student_or_unknown", "excluded"


def _matches_target(unit_code: str | None, unit_name: str | None, target_unit: str | None, target_unit_code: str | None) -> bool:
    code = (unit_code or "").lower()
    name = (unit_name or "").lower()
    target_code = (target_unit_code or "").lower()
    target_name = (target_unit or "").lower()
    return bool(
        (target_code and code == target_code)
        or (target_name and code == target_name)
        or (target_name and (name == target_name or target_name in name or name in target_name))
    )


def infer_analysis_context(
    path: Path,
    role: str,
    unit_code: str | None,
    unit_name: str | None,
    target_unit: str | None,
    target_unit_code: str | None,
    example_mode: bool,
    status: str,
) -> str:
    path_text = str(path).lower()
    if status in {"failed", "unsupported"} or role in {"unknown", "unsupported_binary"}:
        return "unsupported_or_unreadable"
    if "benchmarks" in path_text or "fixture" in path_text or "fixtures" in path_text:
        return "benchmark_fixture"
    if role == "output_protocol":
        return "layout_exemplar"
    if role in {"exemplar_answer", "exemplar_image"}:
        return "style_exemplar"

    has_target = bool(target_unit or target_unit_code)
    same_target = _matches_target(unit_code, unit_name, target_unit, target_unit_code)
    if has_target and not same_target:
        return "cross_unit_example" if example_mode or role in {
            "lecture_slide",
            "lecture_note",
            "annotated_lecture_slide",
            "formal_past_paper",
            "practice_paper",
            "mock_exam",
            "marking_criteria",
            "essay_guidance",
        } else "unsupported_or_unreadable"
    if has_target and same_target:
        if role in {"lecture_slide", "lecture_note", "annotated_lecture_slide", "formal_past_paper", "marking_criteria"}:
            return "target_unit_current_regime"
        return "target_unit_auxiliary"

    if role in {"lecture_slide", "lecture_note", "annotated_lecture_slide", "formal_past_paper", "marking_criteria"}:
        return "target_unit_current_regime"
    if role in {"practice_paper", "mock_exam", "essay_guidance"}:
        return "target_unit_auxiliary"
    return "unsupported_or_unreadable"


def allowed_use_flags(analysis_context: str, role: str) -> dict[str, bool]:
    style_roles = {"exemplar_answer", "exemplar_image", "essay_guidance"}
    if analysis_context == "target_unit_current_regime":
        return {
            "allowed_factual_use": role != "formal_past_paper",
            "allowed_prediction_use": role == "formal_past_paper",
            "allowed_style_use": role in style_roles,
            "allowed_layout_use": False,
            "allowed_transferable_example_use": False,
        }
    if analysis_context == "target_unit_old_or_different_regime":
        return {
            "allowed_factual_use": role in {"lecture_slide", "lecture_note", "annotated_lecture_slide", "marking_criteria"},
            "allowed_prediction_use": False,
            "allowed_style_use": False,
            "allowed_layout_use": False,
            "allowed_transferable_example_use": False,
        }
    if analysis_context == "target_unit_auxiliary":
        return {
            "allowed_factual_use": False,
            "allowed_prediction_use": False,
            "allowed_style_use": role in style_roles,
            "allowed_layout_use": False,
            "allowed_transferable_example_use": False,
        }
    if analysis_context == "cross_unit_example":
        return {
            "allowed_factual_use": False,
            "allowed_prediction_use": False,
            "allowed_style_use": False,
            "allowed_layout_use": False,
            "allowed_transferable_example_use": True,
        }
    if analysis_context == "style_exemplar":
        return {
            "allowed_factual_use": False,
            "allowed_prediction_use": False,
            "allowed_style_use": True,
            "allowed_layout_use": False,
            "allowed_transferable_example_use": False,
        }
    if analysis_context == "layout_exemplar":
        return {
            "allowed_factual_use": False,
            "allowed_prediction_use": False,
            "allowed_style_use": False,
            "allowed_layout_use": True,
            "allowed_transferable_example_use": False,
        }
    return {
        "allowed_factual_use": False,
        "allowed_prediction_use": False,
        "allowed_style_use": False,
        "allowed_layout_use": False,
        "allowed_transferable_example_use": False,
    }


def extract_pdf(path: Path) -> tuple[str, str, int | None, int | None, list[str]]:
    if fitz is not None:
        doc = fitz.open(path)
        pages = [page.get_text("text") for page in doc]
        images = sum(len(page.get_images(full=True)) for page in doc)
        limitations = ["PDF contains images; inspect rendered pages when image text or diagrams matter"] if images else []
        return "\n\n".join(pages), "pymupdf", doc.page_count, images, limitations
    if PdfReader is not None:
        reader = PdfReader(str(path))
        pages = [(page.extract_text() or "") for page in reader.pages]
        return "\n\n".join(pages), "pypdf", len(reader.pages), None, ["image count unavailable with pypdf fallback"]
    raise RuntimeError("no PDF extractor available")


def extract_docx(path: Path) -> tuple[str, str, list[str]]:
    if Document is None:
        raise RuntimeError("python-docx unavailable")
    doc = Document(str(path))
    parts = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" | ".join(cell.text.strip() for cell in row.cells))
    return "\n".join(parts), "python-docx", []


def pptx_xml_text(xml_bytes: bytes) -> list[str]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        raw = xml_bytes.decode("utf-8", errors="ignore")
        return [html.unescape(item) for item in re.findall(r"<a:t>(.*?)</a:t>", raw, flags=re.S)]
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    return [html.unescape(node.text or "") for node in root.findall(".//a:t", ns) if (node.text or "").strip()]


def extract_pptx(path: Path) -> tuple[str, str, int, list[str]]:
    parts: list[str] = []
    limitations = ["PPTX XML extraction captures text but not diagram/image-only content"]
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            (name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)),
            key=lambda name: int(re.search(r"slide(\d+)\.xml", name).group(1)),  # type: ignore[union-attr]
        )
        for idx, name in enumerate(slide_names, start=1):
            texts = [normalise(text) for text in pptx_xml_text(zf.read(name))]
            texts = [text for text in texts if text]
            if texts:
                parts.append(f"SLIDE {idx}: " + " | ".join(texts))
        note_names = sorted(
            (name for name in zf.namelist() if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", name)),
            key=lambda name: int(re.search(r"notesSlide(\d+)\.xml", name).group(1)),  # type: ignore[union-attr]
        )
        for name in note_names:
            note_idx = int(re.search(r"notesSlide(\d+)\.xml", name).group(1))  # type: ignore[union-attr]
            texts = [normalise(text) for text in pptx_xml_text(zf.read(name))]
            texts = [text for text in texts if text and text.lower() != "slide"]
            if texts:
                parts.append(f"SLIDE {note_idx} NOTES: " + " | ".join(texts))
    return "\n".join(parts), "pptx-xml", len(slide_names), limitations


def extract_text(path: Path) -> tuple[str, str, dict[str, Any], list[str]]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text, method, page_count, image_count, limitations = extract_pdf(path)
        return text, method, {"page_count": page_count, "image_count": image_count}, limitations
    if suffix == ".docx":
        text, method, limitations = extract_docx(path)
        return text, method, {}, limitations
    if suffix in {".pptx", ".ppsx"}:
        text, method, slide_count, limitations = extract_pptx(path)
        return text, method, {"slide_count": slide_count}, limitations
    if suffix in TEXT_EXTS:
        return path.read_text(encoding="utf-8", errors="replace"), "text", {}, []
    if suffix in IMAGE_EXTS:
        return "", "image-metadata", {}, ["OCR not performed by this script"]
    raise RuntimeError(f"unsupported extension: {suffix}")


def safe_text_name(path: Path, index: int) -> str:
    base = re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem).strip("_")[:90] or "source"
    return f"{index:03d}_{base}.txt"


def scan(
    paths: list[Path],
    output_dir: Path,
    unit_hint: str | None,
    target_unit: str | None = None,
    target_unit_code: str | None = None,
    example_mode: bool = False,
    benchmark_fixture_config: Path | None = None,
) -> dict[str, Any]:
    text_dir = output_dir / "source_text"
    text_dir.mkdir(parents=True, exist_ok=True)
    rows: list[ExtractedFile] = []
    for index, path in enumerate(iter_files(paths), start=1):
        suffix = path.suffix.lower()
        status = "unsupported"
        method = "none"
        text = ""
        extra: dict[str, Any] = {}
        limitations: list[str] = []
        text_path: str | None = None
        if not path.exists():
            status = "failed"
            limitations = ["path does not exist"]
        elif suffix not in SUPPORTED_EXTS and suffix not in IMAGE_EXTS:
            limitations = [f"unsupported extension: {suffix or '[none]'}"]
            if suffix in {".pyc", ".bin", ".exe"}:
                status = "unsupported"
        else:
            try:
                text, method, extra, limitations = extract_text(path)
                status = "partial" if suffix in IMAGE_EXTS else "ok"
                if text.strip():
                    out = text_dir / safe_text_name(path, index)
                    out.write_text(text, encoding="utf-8")
                    text_path = str(out)
            except Exception as exc:  # pragma: no cover
                status = "failed"
                method = method if method != "none" else suffix.lstrip(".") or "unknown"
                limitations = [f"{type(exc).__name__}: {exc}"]
        unit_code, unit_name = detect_unit(path, text, unit_hint)
        role = detect_role(path, text, unit_hint)
        if status == "unsupported":
            role = "unsupported_binary"
        source_trust_level, evidence_use = trust_and_evidence(role)
        analysis_context = infer_analysis_context(
            path=path,
            role=role,
            unit_code=unit_code,
            unit_name=unit_name,
            target_unit=target_unit or unit_hint,
            target_unit_code=target_unit_code,
            example_mode=example_mode,
            status=status,
        )
        allowed_flags = allowed_use_flags(analysis_context, role)
        if role == "exemplar_image":
            if "visual_inspection_required" not in limitations:
                limitations.append("visual_inspection_required")
            limitations.append(
                "Image exemplar may be used for essay style, paragraph logic, and density only; factual claims require verification from lecture or reliable sources."
            )
        year = detect_year(path, text, role)
        rows.append(
            ExtractedFile(
                path=str(path),
                name=path.name,
                extension=suffix,
                role=role,
                unit_code=unit_code,
                unit_name=unit_name,
                year=year,
                source_trust_level=source_trust_level,
                evidence_use=evidence_use,
                analysis_context=analysis_context,
                allowed_factual_use=allowed_flags["allowed_factual_use"],
                allowed_prediction_use=allowed_flags["allowed_prediction_use"],
                allowed_style_use=allowed_flags["allowed_style_use"],
                allowed_layout_use=allowed_flags["allowed_layout_use"],
                allowed_transferable_example_use=allowed_flags["allowed_transferable_example_use"],
                status=status,
                method=method,
                text_path=text_path,
                char_count=len(text),
                page_count=extra.get("page_count"),
                slide_count=extra.get("slide_count"),
                image_count=extra.get("image_count"),
                limitations=limitations,
                preview=normalise(text[:500]),
            )
        )
    manifest = {
        "inputs": [str(path) for path in paths],
        "unit_hint": unit_hint,
        "target_unit": target_unit,
        "target_unit_code": target_unit_code,
        "example_mode": example_mode,
        "benchmark_fixture_config": str(benchmark_fixture_config) if benchmark_fixture_config else None,
        "file_count": len(rows),
        "files": [asdict(row) for row in rows],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "source_scan.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or directories to scan")
    parser.add_argument("--output", required=True, help="Output directory for manifest and source_text")
    parser.add_argument("--unit-hint", default=None, help="Optional unit code/name hint, e.g. BIOL21332")
    parser.add_argument("--target-unit", default=None, help="Target unit name for AnalysisContext assignment")
    parser.add_argument("--target-unit-code", default=None, help="Target unit code for AnalysisContext assignment")
    parser.add_argument("--example-mode", action="store_true", help="Classify non-target sources as transferable examples")
    parser.add_argument("--benchmark-fixture-config", type=Path, default=None, help="Optional benchmark fixture config path")
    args = parser.parse_args(argv)
    manifest = scan(
        [Path(path).expanduser() for path in args.paths],
        Path(args.output).expanduser(),
        args.unit_hint,
        target_unit=args.target_unit,
        target_unit_code=args.target_unit_code,
        example_mode=args.example_mode,
        benchmark_fixture_config=args.benchmark_fixture_config,
    )
    counts: dict[str, int] = {}
    for row in manifest["files"]:
        counts[row["role"]] = counts.get(row["role"], 0) + 1
    print(json.dumps({"file_count": manifest["file_count"], "role_counts": counts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
