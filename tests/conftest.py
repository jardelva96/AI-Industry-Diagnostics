"""Fixtures compartilhadas para testes."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aidiag.auth import hash_password
from aidiag.database import Base
from aidiag.models import Assessment, Company, User


@pytest.fixture()
def db():
    """Banco de dados em memória para testes."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_cls = sessionmaker(bind=engine)
    session = session_cls()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def sample_user(db):
    """Usuário de teste."""
    user = User(
        username="testuser",
        email="test@test.com",
        hashed_password=hash_password("test123"),
        full_name="Test User",
        role="analyst",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture()
def sample_company(db):
    """Empresa de teste."""
    company = Company(
        name="Acme Indústria",
        cnpj="12.345.678/0001-90",
        sector="Manufatura",
        size="media",
        city="São Paulo",
        state="SP",
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@pytest.fixture()
def sample_assessment(db, sample_user, sample_company):
    """Avaliação de teste com scores predefinidos."""
    assessment = Assessment(
        company_id=sample_company.id,
        author_id=sample_user.id,
        notes="Avaliação de teste",
        score_data=3.2,
        score_algorithms=2.4,
        score_governance=1.8,
        score_talent=2.6,
        score_process=3.0,
        score_strategy=2.2,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment
