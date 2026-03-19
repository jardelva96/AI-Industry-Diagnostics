"""Testes para o serviço de avaliação."""

from __future__ import annotations

from aidiag.schemas import AnswerIn, AssessmentCreate
from aidiag.services.assessment_service import (
    create_assessment,
    create_company,
    get_assessment,
    list_assessments,
    list_companies,
)


def test_create_company(db):
    """Criação de empresa persiste no banco."""
    company = create_company(db, name="TestCo", sector="Varejo", size="pequena", city="SP", state="SP")
    assert company.id
    assert company.name == "TestCo"


def test_list_companies(db, sample_company):
    """Listagem retorna empresas cadastradas."""
    companies = list_companies(db)
    assert len(companies) >= 1
    assert any(c.name == "Acme Indústria" for c in companies)


def test_create_assessment_with_answers(db, sample_user, sample_company):
    """Avaliação com respostas calcula scores corretamente."""
    answers = [
        AnswerIn(dimension="data", question_id="D1", score=3),
        AnswerIn(dimension="data", question_id="D2", score=4),
        AnswerIn(dimension="data", question_id="D3", score=3),
        AnswerIn(dimension="data", question_id="D4", score=2),
        AnswerIn(dimension="data", question_id="D5", score=3),
        AnswerIn(dimension="algorithms", question_id="A1", score=2),
        AnswerIn(dimension="algorithms", question_id="A2", score=2),
    ]
    payload = AssessmentCreate(company_id=sample_company.id, notes="Teste", answers=answers)
    assessment = create_assessment(db, payload, author_id=sample_user.id)

    assert assessment.score_data == 3.0  # (3+4+3+2+3)/5
    assert assessment.score_algorithms == 2.0  # (2+2)/2
    assert len(assessment.answers) == 7


def test_get_assessment(db, sample_assessment):
    """Busca por ID retorna avaliação correta."""
    found = get_assessment(db, sample_assessment.id)
    assert found is not None
    assert found.id == sample_assessment.id


def test_list_assessments_filter(db, sample_assessment, sample_company):
    """Filtragem por empresa funciona."""
    results = list_assessments(db, company_id=sample_company.id)
    assert len(results) >= 1
    assert all(r.company_id == sample_company.id for r in results)


def test_overall_score(sample_assessment):
    """Cálculo do score geral está correto."""
    expected = (3.2 + 2.4 + 1.8 + 2.6 + 3.0 + 2.2) / 6
    assert abs(sample_assessment.overall_score - expected) < 0.01


def test_maturity_level(sample_assessment):
    """Nível de maturidade textual corresponde ao score."""
    assert sample_assessment.maturity_level == "Intermediário"
