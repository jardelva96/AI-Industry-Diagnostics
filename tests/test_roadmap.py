"""Testes para o serviço de roadmap."""

from __future__ import annotations

from aidiag.services.roadmap_service import generate_roadmap


def test_roadmap_has_four_phases(sample_assessment):
    """Roadmap gera exatamente 4 fases."""
    roadmap = generate_roadmap(sample_assessment)

    assert len(roadmap.phases) == 4
    assert roadmap.phases[0].phase == 1
    assert roadmap.phases[1].phase == 2
    assert roadmap.phases[2].phase == 3
    assert roadmap.phases[3].phase == 4


def test_roadmap_phases_have_actions(sample_assessment):
    """Cada fase do roadmap tem ações definidas."""
    roadmap = generate_roadmap(sample_assessment)

    for phase in roadmap.phases:
        assert len(phase.actions) > 0
        assert phase.title
        assert phase.horizon
        assert phase.expected_impact


def test_roadmap_company_info(sample_assessment):
    """Roadmap inclui informações da empresa."""
    roadmap = generate_roadmap(sample_assessment)

    assert roadmap.company_name == "Acme Indústria"
    assert roadmap.maturity_level in {"Inicial", "Básico", "Intermediário", "Avançado", "Líder"}
