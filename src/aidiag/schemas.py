"""Schemas Pydantic para validação de entrada/saída da API."""

from __future__ import annotations

import datetime

from pydantic import BaseModel, Field


# ── Auth ──────────────────────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: str
    password: str = Field(min_length=6)
    full_name: str = ""
    role: str = "analyst"


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


# ── Company ───────────────────────────────────────────────────────────
class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    cnpj: str | None = None
    sector: str
    size: str = Field(pattern=r"^(micro|pequena|media|grande)$")
    city: str = ""
    state: str = "SP"


class CompanyOut(BaseModel):
    id: str
    name: str
    cnpj: str | None
    sector: str
    size: str
    city: str
    state: str
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


# ── Assessment ────────────────────────────────────────────────────────
class AnswerIn(BaseModel):
    dimension: str
    question_id: str
    score: int = Field(ge=1, le=5)


class AssessmentCreate(BaseModel):
    company_id: str
    notes: str = ""
    answers: list[AnswerIn] = []


class AssessmentOut(BaseModel):
    id: str
    company_id: str
    author_id: str
    created_at: datetime.datetime
    notes: str
    score_data: float
    score_algorithms: float
    score_governance: float
    score_talent: float
    score_process: float
    score_strategy: float
    overall_score: float
    maturity_level: str

    model_config = {"from_attributes": True}


# ── Diagnostic ────────────────────────────────────────────────────────
class DimensionDetail(BaseModel):
    dimension: str
    label: str
    score: float
    level: str
    gap: float
    recommendations: list[str]


class DiagnosticReport(BaseModel):
    assessment_id: str
    company_name: str
    overall_score: float
    maturity_level: str
    dimensions: list[DimensionDetail]
    top_strengths: list[str]
    critical_gaps: list[str]


# ── Roadmap ───────────────────────────────────────────────────────────
class RoadmapPhase(BaseModel):
    phase: int
    title: str
    horizon: str
    actions: list[str]
    expected_impact: str


class RoadmapOut(BaseModel):
    assessment_id: str
    company_name: str
    maturity_level: str
    phases: list[RoadmapPhase]
