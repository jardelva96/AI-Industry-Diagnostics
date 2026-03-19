"""Serviço de gerenciamento de avaliações de maturidade."""

from __future__ import annotations

from sqlalchemy.orm import Session

from aidiag.data.dimensions import DIMENSION_KEYS, SCORE_FIELD_MAP
from aidiag.models import Assessment, AssessmentAnswer, Company
from aidiag.schemas import AssessmentCreate


def create_assessment(db: Session, payload: AssessmentCreate, author_id: str) -> Assessment:
    """Cria uma nova avaliação e calcula os scores por dimensão."""
    assessment = Assessment(
        company_id=payload.company_id,
        author_id=author_id,
        notes=payload.notes,
    )

    # Agrupa respostas por dimensão e calcula média
    dim_scores: dict[str, list[int]] = {k: [] for k in DIMENSION_KEYS}
    for ans in payload.answers:
        if ans.dimension in dim_scores:
            dim_scores[ans.dimension].append(ans.score)

    for dim_key, scores in dim_scores.items():
        field = SCORE_FIELD_MAP[dim_key]
        avg = sum(scores) / len(scores) if scores else 1.0
        setattr(assessment, field, round(avg, 2))

    db.add(assessment)
    db.flush()

    # Persiste respostas individuais
    for ans in payload.answers:
        db.add(AssessmentAnswer(
            assessment_id=assessment.id,
            dimension=ans.dimension,
            question_id=ans.question_id,
            score=ans.score,
        ))

    db.commit()
    db.refresh(assessment)
    return assessment


def list_assessments(db: Session, company_id: str | None = None) -> list[Assessment]:
    """Lista avaliações, opcionalmente filtradas por empresa."""
    query = db.query(Assessment)
    if company_id:
        query = query.filter(Assessment.company_id == company_id)
    return query.order_by(Assessment.created_at.desc()).all()


def get_assessment(db: Session, assessment_id: str) -> Assessment | None:
    """Busca uma avaliação por ID."""
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()


def get_company_latest(db: Session, company_id: str) -> Assessment | None:
    """Retorna a avaliação mais recente de uma empresa."""
    return (
        db.query(Assessment)
        .filter(Assessment.company_id == company_id)
        .order_by(Assessment.created_at.desc())
        .first()
    )


def list_companies(db: Session) -> list[Company]:
    """Lista todas as empresas cadastradas."""
    return db.query(Company).order_by(Company.name).all()


def create_company(db: Session, **kwargs) -> Company:
    """Cadastra uma nova empresa."""
    company = Company(**kwargs)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
