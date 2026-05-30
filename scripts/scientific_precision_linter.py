#!/usr/bin/env python3
"""Lint scientific prose for category precision and claim-strength failures."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from docx import Document  # type: ignore
except Exception:  # pragma: no cover
    Document = None  # type: ignore

CATEGORY_WORDS = {
    "gene": {"gene", "genes", "mutation", "mutations", "variant", "variants", "repeat", "expansion"},
    "protein": {"protein", "proteins", "enzyme", "enzymes", "aggregate", "aggregates"},
    "receptor_or_channel": {"receptor", "receptors", "channel", "channels", "transporter", "transporters", "ligand", "ligands"},
    "cell_type": {"neuron", "neurons", "astrocyte", "astrocytes", "microglia", "cell", "cells"},
    "pathway_or_process": {"pathway", "pathways", "signalling", "transport", "inflammation", "metabolism", "proteolysis"},
    "assay_or_method": {"assay", "assays", "model", "models", "cohort", "cohorts", "screen", "screens", "sequencing"},
    "company_or_case": {"company", "companies", "platform", "platforms", "case", "cases", "firm", "firms"},
}

MIXED_LIST_INTRO_RE = re.compile(r"\b(?:including|such as|through|via)\s+([^.;:]+)", re.I)
CLAIM_OVERSTRENGTH_RE = re.compile(
    r"\b(?:association|correlation|cohort|review|observational|abundance|expression)\b[^.?!]{0,90}\b(?:proves|prove|causes|cause|demonstrates|demonstrate)\b|"
    r"\b(?:proves|prove|causes|cause|demonstrates|demonstrate)\b[^.?!]{0,90}\b(?:association|correlation|cohort|review|observational|abundance|expression)\b",
    re.I,
)
FUNCTION_WORDS = re.compile(
    r"\b(?:because|therefore|thereby|which|so that|supports|support|indicates|indicate|links|link|distinguishes|distinguish|explains|explain|tests|test|measures|measure|changes|change|reduces|reduce|increases|increase|limits|limit)\b",
    re.I,
)
SENTENCE_RE = re.compile(r"[^.?!]+[.?!]?")


def iter_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(
            child
            for child in path.rglob("*")
            if child.is_file() and child.suffix.lower() in {".docx", ".md", ".txt"}
        )
    return []


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        if Document is None:
            raise RuntimeError("python-docx is required to lint DOCX files")
        doc = Document(path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
    return path.read_text(encoding="utf-8", errors="ignore")


def classify_term(term: str) -> str | None:
    words = {word.strip(" ,;:()[]{}\t\n").casefold() for word in re.split(r"\s+", term) if word.strip()}
    for category, markers in CATEGORY_WORDS.items():
        if words & markers:
            return category
    return None


def split_list_items(value: str) -> list[str]:
    parts = re.split(r",|\band\b|/", value, flags=re.I)
    return [part.strip() for part in parts if part.strip()]


def mixed_category_list_hits(sentence: str) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for match in MIXED_LIST_INTRO_RE.finditer(sentence):
        items = split_list_items(match.group(1))
        categories = {category for item in items if (category := classify_term(item))}
        if len(categories) > 1 and not FUNCTION_WORDS.search(sentence):
            hits.append({"items": items, "categories": sorted(categories)})
    return hits


def named_catalogue_without_function(sentence: str) -> bool:
    categories = []
    for words in CATEGORY_WORDS.values():
        for marker in words:
            if re.search(rf"\b{re.escape(marker)}\b", sentence, re.I):
                categories.append(marker)
    return len(set(categories)) >= 4 and not FUNCTION_WORDS.search(sentence)


def lint_text(text: str, *, reference: str = "<text>") -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for index, raw_sentence in enumerate(SENTENCE_RE.findall(text), start=1):
        sentence = raw_sentence.strip()
        if not sentence:
            continue
        for hit in mixed_category_list_hits(sentence):
            failures.append({"type": "mixed_entity_category_list", "reference": reference, "sentence": index, **hit})
        if CLAIM_OVERSTRENGTH_RE.search(sentence):
            failures.append({"type": "claim_strength_overstated", "reference": reference, "sentence": index, "text": sentence[:180]})
        if named_catalogue_without_function(sentence):
            failures.append({"type": "named_catalogue_without_function", "reference": reference, "sentence": index, "text": sentence[:180]})
    return failures


def lint_paths(paths: list[Path]) -> dict[str, Any]:
    files: list[Path] = []
    for path in paths:
        files.extend(iter_files(path))
    failures: list[dict[str, Any]] = []
    if not files:
        failures.append({"type": "no_supported_files", "paths": [str(path) for path in paths]})
    for file_path in files:
        try:
            failures.extend(lint_text(read_text(file_path), reference=str(file_path)))
        except Exception as exc:
            failures.append({"type": "read_error", "reference": str(file_path), "error": str(exc)})
    return {"status": "pass" if not failures else "fail", "counts": {"files": len(files)}, "failures": failures}


def self_test() -> dict[str, Any]:
    bad_text = (
        "The association proves disease causation in every patient. "
        "The answer lists genes, receptors, assays and disease cohorts. "
        "The pathway includes genes, protein aggregates, patient cohorts and companies."
    )
    good_text = (
        "The mutation reduces transporter expression, which decreases glutamate uptake and raises extracellular glutamate. "
        "Patient evidence supports relevance, while the cell model tests whether altered uptake can injure motor neurons."
    )
    bad_failures = lint_text(bad_text, reference="bad_fixture")
    good_failures = lint_text(good_text, reference="good_fixture")
    failures: list[dict[str, Any]] = []
    if not bad_failures:
        failures.append({"type": "self_test_bad_fixture_not_rejected"})
    if good_failures:
        failures.append({"type": "self_test_good_fixture_rejected", "failures": good_failures})
    return {
        "status": "pass" if not failures else "fail",
        "bad_fixture_failures": bad_failures,
        "good_fixture_failures": good_failures,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = self_test() if args.self_test else lint_paths(args.paths)
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
