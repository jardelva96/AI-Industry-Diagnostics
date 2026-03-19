"""Rotas de diagnóstico e benchmark."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from aidiag.auth import get_current_user
from aidiag.database import get_db
from aidiag.models import User
from aidiag.schemas import DiagnosticReport
from aidiag.services.assessment_service import get_assessment
from aidiag.services.benchmark_service import compare_with_benchmark
from aidiag.services.diagnostic_service import generate_diagnostic

router = APIRouter(prefix="/diagnostics", tags=["Diagnósticos"])


@router.get("/{assessment_id}", response_model=DiagnosticReport)
def get_diagnostic(
    assessment_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Gera relatório de diagnóstico para uma avaliação."""
    assessment = get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return generate_diagnostic(assessment)


@router.get("/{assessment_id}/benchmark")
def get_benchmark_comparison(
    assessment_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Compara avaliação com benchmark do setor."""
    assessment = get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return compare_with_benchmark(assessment)
