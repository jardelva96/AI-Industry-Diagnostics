"""Testes para o serviço de diagnóstico."""

from __future__ import annotations

from aidiag.services.diagnostic_service import _level_for_score, generate_diagnostic


def test_level_for_score():
    """Mapeamento score -> nível está correto."""
    assert _level_for_score(1.0) == "Inicial"
    assert _level_for_score(2.0) == "Básico"
    assert _level_for_score(3.0) == "Intermediário"
    assert _level_for_score(4.0) == "Avançado"
    assert _level_for_score(5.0) == "Líder"


def test_generate_diagnostic(sample_assessment):
    """Diagnóstico gera relatório com todas as dimensões."""
    report = generate_diagnostic(sample_assessment)

    assert report.assessment_id == sample_assessment.id
    assert len(report.dimensions) == 6
    assert report.overall_score > 0
    assert report.maturity_level in {"Inicial", "Básico", "Intermediário", "Avançado", "Líder"}


def test_diagnostic_has_recommendations(sample_assessment):
    """Cada dimensão do diagnóstico tem recomendações."""
    report = generate_diagnostic(sample_assessment)

    for dim in report.dimensions:
        assert len(dim.recommendations) > 0
        assert dim.gap >= 0


def test_diagnostic_identifies_strengths_and_gaps(sample_assessment):
    """Diagnóstico identifica pontos fortes e gaps."""
    report = generate_diagnostic(sample_assessment)

    assert len(report.top_strengths) == 2
    assert len(report.critical_gaps) == 2
