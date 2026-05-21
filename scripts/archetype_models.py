"""Typed records for archetype-centric exam prediction outputs."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal


Confidence = Literal["High", "Medium", "Low"]
QuestionFamily = Literal["mcq", "short_answer", "essay", "case_study", "data_problem", "long_answer_project"]
OutputMode = Literal["default_excel_workbook", "docx_example_essay", "excel_evidence_workbook"]
EssayRunSourceType = Literal[
    "lecture_slide_core",
    "official_note",
    "citation_original_source",
    "extra_reading_book",
    "student_visible_transition",
    "question_framing",
]
EssayRunHighlight = Literal["none", "yellow", "green"]
Saturation = Literal["fresh", "partially_tested", "saturated", "unknown"]
AnalysisContext = Literal[
    "target_unit_current_regime",
    "target_unit_old_or_different_regime",
    "target_unit_auxiliary",
    "cross_unit_example",
    "style_exemplar",
    "layout_exemplar",
    "benchmark_fixture",
    "unsupported_or_unreadable",
]


@dataclass
class UnitExampleContribution:
    source_unit: str
    source_materials: list[str]
    observed_unit_pattern: str
    generic_skill_contribution: str
    transferable_rule: str
    future_unit_diagnostic_questions: list[str]
    non_transferable_content: list[str]
    affected_workflows: list[str]
    anti_patterns_prevented: list[str]
    validation_checks: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class QuestionArchetype:
    archetype_id: str
    unit_key: str
    exam_regime: str
    question_family: QuestionFamily
    task_verbs: list[str]
    input_format: str
    cognitive_operation: str
    expected_output: str
    mark_scheme_structure: list[str]
    compatible_kp_families: list[str]
    slots: list[str]
    seen_in: list[dict[str, str | int]]
    saturation: Saturation = "unknown"
    confidence: Confidence = "Medium"
    derived_from_unit_example: str | None = None
    transferable_rule: str | None = None
    non_transferable_content: list[str] = field(default_factory=list)
    format_match_required: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MCQPattern:
    unit_key: str
    exam_regime: str
    year: int | None
    question_no: str
    question_mode: str
    correct_concept: str
    discriminator: str
    distractor_families: list[str]
    trap: str
    compatible_kps: list[str] = field(default_factory=list)
    derived_from_unit_example: str | None = None
    transferable_rule: str | None = None
    non_transferable_content: list[str] = field(default_factory=list)
    format_match_required: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ShortAnswerPattern:
    unit_key: str
    exam_regime: str
    year: int | None
    question_no: str
    marks: int | None
    stem_type: str
    task_verbs: list[str]
    input_format: str
    primary_kp: str
    supporting_kps: list[str]
    operation: list[str]
    answer_schema: list[str]
    archetype_id: str
    derived_from_unit_example: str | None = None
    transferable_rule: str | None = None
    non_transferable_content: list[str] = field(default_factory=list)
    format_match_required: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EssayQuestionAnalysis:
    unit_key: str
    question: str
    question_type: str
    task_verbs: list[str]
    likely_scope: str
    likely_lecturer: str | None
    lecturer_confidence: Confidence
    expected_answer_shape: list[str]
    required_comparison_axes: list[str]
    required_kps: list[str]
    excluded_kps: list[str]
    derived_from_unit_example: str | None = None
    transferable_rule: str | None = None
    non_transferable_content: list[str] = field(default_factory=list)
    format_match_required: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EssayKnowledgeInventory:
    must_use_lecture_content: list[str]
    supportive_lecture_content: list[str]
    cross_module_content: list[str]
    extra_reading_candidates: list[str]
    excluded_content: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EssayParagraphPlan:
    paragraph_number: int
    function: str
    core_claim: str
    lecture_content_used: list[str]
    cross_module_link: str | None
    extra_reading_used: str | None
    why_included: str
    link_back_to_question: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExtraReadingInsert:
    source: str
    verified_author_year: str
    insertion_mode: str
    target_paragraph: int | None
    relevance_to_question: str
    max_sentence_budget: int
    use_decision: Literal["use", "omit", "needs_verification"]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class KnowledgeUseInventory:
    unit_key: str
    lecture_block: str
    must_use_core: list[str]
    should_use_if_space: list[str]
    method_principles: list[str]
    scenario_applications: list[str]
    readout_and_interpretation: list[str]
    controls_or_limitations: list[str]
    cross_module_links: list[str]
    outside_module_but_relevant: list[str]
    exclude: list[str]
    derived_from_unit_example: str | None = None
    transferable_rule: str | None = None
    non_transferable_content: list[str] = field(default_factory=list)
    format_match_required: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LongAnswerProjectPattern:
    unit_key: str
    exam_regime: str
    year: int | None
    question_no: str
    project_context: str
    named_proteins_or_systems: list[str]
    question_parts: list[dict]
    core_archetype: str
    slot_grammar: list[str]
    required_answer_mode: str
    cross_module_links: list[str]
    confidence: Confidence = "Medium"
    derived_from_unit_example: str | None = None
    transferable_rule: str | None = None
    non_transferable_content: list[str] = field(default_factory=list)
    format_match_required: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LongAnswerParagraphPlan:
    paragraph_no: int
    question_part: str
    paragraph_function: str
    claim_or_goal: str
    lecture_kps_used: list[str]
    scenario_facts_used: list[str]
    method_or_mechanism: str
    expected_readout: str
    interpretation: str
    control_or_limitation: str
    extra_reading_use: str | None
    excluded_content: list[str]
    word_budget: int
    derived_from_unit_example: str | None = None
    transferable_rule: str | None = None
    non_transferable_content: list[str] = field(default_factory=list)
    format_match_required: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExtraReadingCandidate:
    source_type: str
    author_year: str | None
    topic: str
    supports: str
    verification_status: Literal["verified", "needs_verification", "rejected"]
    insertion_mode: Literal["omit", "sentence", "short_paragraph"]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LectureAnchor:
    file: str
    slide_or_page_range: str
    lecture_id: str | None = None
    kp_id: str | None = None
    claim_supported: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EssayTextRun:
    text: str
    source_type: EssayRunSourceType
    source_anchor: str | None
    highlight: EssayRunHighlight = "none"
    in_text_citation: str | None = None
    citation_original_read: bool | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.source_type == "citation_original_source":
            if self.highlight != "green":
                errors.append("citation_original_source_requires_green_highlight")
            if not self.in_text_citation:
                errors.append("citation_original_source_requires_in_text_citation")
            if self.citation_original_read is not True:
                errors.append("citation_original_source_requires_read_status_true")
        if self.source_type == "extra_reading_book":
            if self.highlight != "yellow":
                errors.append("extra_reading_book_requires_yellow_highlight")
            if not self.source_anchor:
                errors.append("extra_reading_book_requires_chapter_or_section_anchor")
        if self.highlight == "green" and self.source_type != "citation_original_source":
            errors.append("green_highlight_only_for_citation_original_source")
        if self.highlight == "yellow" and self.source_type != "extra_reading_book":
            errors.append("yellow_highlight_only_for_extra_reading_book")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EssayParagraph:
    paragraph_id: str
    function: str
    text_runs: list[EssayTextRun]
    lecture_anchors: list[LectureAnchor]
    paragraph_alignment: Literal["justify", "center", "left"] = "justify"
    is_title: bool = False
    is_subtitle: bool = False
    is_heading: bool = False

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not (self.is_title or self.is_subtitle or self.is_heading) and not self.lecture_anchors:
            errors.append("body_paragraph_requires_lecture_anchor")
        for run in self.text_runs:
            errors.extend(run.validate())
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExampleEssayDocumentPlan:
    essay_id: str
    question: str
    title: str
    subtitle: str | None
    unit_key: str
    lecture_anchors: list[LectureAnchor]
    paragraphs: list[EssayParagraph]
    total_word_target: int | None = None
    extra_reading_word_target_min: int | None = None
    extra_reading_word_target_max: int | None = None
    output_mode: OutputMode = "docx_example_essay"
    qa_flags: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.output_mode != "docx_example_essay":
            errors.append("example_essay_document_plan_requires_docx_output_mode")
        if not self.lecture_anchors:
            errors.append("essay_requires_lecture_anchors")
        for paragraph in self.paragraphs:
            errors.extend([f"{paragraph.paragraph_id}:{err}" for err in paragraph.validate()])
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LongAnswerQualityCheck:
    answers_all_question_parts: bool
    follows_mark_weighting: bool
    uses_scenario_facts: bool
    explains_method_principles: bool
    gives_expected_readouts: bool
    interprets_readouts: bool
    includes_controls_or_limitations: bool
    lecture_grounded: bool
    extra_reading_verified: bool
    no_generic_padding: bool
    word_limit_respected: bool

    def to_dict(self) -> dict:
        return asdict(self)


def confidence_band(score_terms: dict[str, int | float]) -> Confidence:
    """Map explainable score components to a coarse confidence band."""
    score = sum(float(v) for v in score_terms.values())
    if score >= 7:
        return "High"
    if score >= 4:
        return "Medium"
    return "Low"
