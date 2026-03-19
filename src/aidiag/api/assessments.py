"""Rotas de avaliação de maturidade em IA."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from aidiag.auth import get_current_user, require_role
from aidiag.database import get_db
from aidiag.models import AuditLog, Company, User
from aidiag.schemas import AssessmentCreate, AssessmentOut, CompanyCreate, CompanyOut
from aidiag.services.assessment_service import (
    create_assessment,
    create_company,
    get_assessment,
    list_assessments,
    list_companies,
)

router = APIRouter(prefix="/assessments", tags=["Avaliações"])


# ── Companies ─────────────────────────────────────────────────────────
@router.get("/companies", response_model=list[CompanyOut])
def get_companies(db: Session = Depends(get_db), _user: User = Depends(get_current_user)):
    """Lista todas as empresas cadastradas."""
    return list_companies(db)


@router.post("/companies", response_model=CompanyOut, status_code=status.HTTP_201_CREATED)
def add_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin", "analyst")),
):
    """Cadastra uma nova empresa."""
    company = create_company(
        db,
        name=payload.name,
        cnpj=payload.cnpj,
        sector=payload.sector,
        size=payload.size,
        city=payload.city,
        state=payload.state,
    )
    db.add(AuditLog(user_id=user.id, action="create_company", target=company.id, detail=company.name))
    db.commit()
    return company


# ── Assessments ───────────────────────────────────────────────────────
@router.get("/", response_model=list[AssessmentOut])
def get_assessments(
    company_id: str | None = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Lista avaliações, opcionalmente filtradas por empresa."""
    return list_assessments(db, company_id=company_id)


@router.get("/{assessment_id}", response_model=AssessmentOut)
def get_assessment_detail(
    assessment_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Detalha uma avaliação específica."""
    assessment = get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return assessment


@router.post("/", response_model=AssessmentOut, status_code=status.HTTP_201_CREATED)
def create_new_assessment(
    payload: AssessmentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin", "analyst")),
):
    """Cria uma nova avaliação de maturidade."""
    company = db.query(Company).filter(Company.id == payload.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    assessment = create_assessment(db, payload, author_id=user.id)
    db.add(AuditLog(user_id=user.id, action="create_assessment", target=assessment.id, detail=company.name))
    db.commit()
    return assessment
