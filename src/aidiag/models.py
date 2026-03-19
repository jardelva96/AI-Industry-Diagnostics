"""Modelos ORM do banco de dados."""

from __future__ import annotations

import datetime
import uuid

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aidiag.database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class User(Base):
    """Usuário da plataforma."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255), default="")
    role: Mapped[str] = mapped_column(String(20), default="analyst")  # admin | analyst | viewer
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    assessments: Mapped[list[Assessment]] = relationship(back_populates="author")


class Company(Base):
    """Empresa avaliada."""

    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(255), index=True)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=True)
    sector: Mapped[str] = mapped_column(String(100))
    size: Mapped[str] = mapped_column(String(30))  # micro | pequena | media | grande
    city: Mapped[str] = mapped_column(String(120), default="")
    state: Mapped[str] = mapped_column(String(2), default="SP")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    assessments: Mapped[list[Assessment]] = relationship(back_populates="company")


class Assessment(Base):
    """Avaliação de maturidade em IA de uma empresa."""

    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"))
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    notes: Mapped[str] = mapped_column(Text, default="")

    # Scores por dimensão (1-5)
    score_data: Mapped[float] = mapped_column(Float, default=1.0)
    score_algorithms: Mapped[float] = mapped_column(Float, default=1.0)
    score_governance: Mapped[float] = mapped_column(Float, default=1.0)
    score_talent: Mapped[float] = mapped_column(Float, default=1.0)
    score_process: Mapped[float] = mapped_column(Float, default=1.0)
    score_strategy: Mapped[float] = mapped_column(Float, default=1.0)

    company: Mapped[Company] = relationship(back_populates="assessments")
    author: Mapped[User] = relationship(back_populates="assessments")
    answers: Mapped[list[AssessmentAnswer]] = relationship(back_populates="assessment", cascade="all, delete-orphan")

    @property
    def overall_score(self) -> float:
        """Média geral de maturidade."""
        scores = [
            self.score_data,
            self.score_algorithms,
            self.score_governance,
            self.score_talent,
            self.score_process,
            self.score_strategy,
        ]
        return sum(scores) / len(scores)

    @property
    def maturity_level(self) -> str:
        """Nível de maturidade textual."""
        avg = self.overall_score
        if avg < 1.5:
            return "Inicial"
        if avg < 2.5:
            return "Básico"
        if avg < 3.5:
            return "Intermediário"
        if avg < 4.5:
            return "Avançado"
        return "Líder"


class AssessmentAnswer(Base):
    """Resposta individual do questionário."""

    __tablename__ = "assessment_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id"))
    dimension: Mapped[str] = mapped_column(String(50))
    question_id: Mapped[str] = mapped_column(String(20))
    score: Mapped[int] = mapped_column(Integer)

    assessment: Mapped[Assessment] = relationship(back_populates="answers")


class AuditLog(Base):
    """Log de auditoria de ações na plataforma."""

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(32), nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    target: Mapped[str] = mapped_column(String(255), default="")
    detail: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
