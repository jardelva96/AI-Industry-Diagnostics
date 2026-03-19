"""Rotas de roadmap de adoção de IA."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from aidiag.auth import get_current_user
from aidiag.database import get_db
from aidiag.models import User
from aidiag.schemas import RoadmapOut
from aidiag.services.assessment_service import get_assessment
from aidiag.services.roadmap_service import generate_roadmap

router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])


@router.get("/{assessment_id}", response_model=RoadmapOut)
def get_roadmap(
    assessment_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Gera roadmap de adoção de IA baseado na avaliação."""
    assessment = get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return generate_roadmap(assessment)
