"""Serviço de geração de roadmap de adoção de IA."""

from __future__ import annotations

from aidiag.data.dimensions import DIMENSIONS, SCORE_FIELD_MAP
from aidiag.data.use_cases import USE_CASES
from aidiag.models import Assessment
from aidiag.schemas import RoadmapOut, RoadmapPhase


def _get_sector_use_cases(sector: str, maturity: float) -> list[str]:
    """Retorna casos de uso viáveis para o setor e nível de maturidade."""
    cases = USE_CASES.get(sector, [])
    return [c["name"] for c in cases if c["min_maturity"] <= maturity + 0.5]


def generate_roadmap(assessment: Assessment) -> RoadmapOut:
    """Gera roadmap em 3 fases baseado nos gaps identificados."""
    # Coleta scores e identifica gaps
    dim_scores: list[tuple[str, str, float]] = []
    for dim_key, dim_info in DIMENSIONS.items():
        field = SCORE_FIELD_MAP[dim_key]
        score = getattr(assessment, field)
        dim_scores.append((dim_key, dim_info["label"], score))

    # Ordena por score (prioriza os mais baixos)
    dim_scores.sort(key=lambda x: x[2])
    overall = assessment.overall_score
    company_name = assessment.company.name if assessment.company else "N/A"
    sector = assessment.company.sector if assessment.company else "Manufatura"

    phases: list[RoadmapPhase] = []

    # ── Fase 1: Fundação (0-6 meses) ─────────────────────────────────
    phase1_actions = []
    # Foca nas 2 dimensões mais fracas
    for _dim_key, label, score in dim_scores[:2]:
        if score < 2.0:
            phase1_actions.append(f"[{label}] Estabelecer fundamentos básicos (score atual: {score:.1f})")
        elif score < 3.0:
            phase1_actions.append(f"[{label}] Consolidar práticas existentes (score atual: {score:.1f})")
        else:
            phase1_actions.append(f"[{label}] Otimizar e escalar (score atual: {score:.1f})")

    phase1_actions.append("Realizar assessment detalhado com todas as áreas da empresa")
    phase1_actions.append("Definir governança de dados e políticas de privacidade (LGPD)")
    quick_wins = _get_sector_use_cases(sector, overall)
    if quick_wins:
        phase1_actions.append(f"Quick win: iniciar piloto de {quick_wins[0]}")

    phases.append(RoadmapPhase(
        phase=1,
        title="Fundação & Quick Wins",
        horizon="0 – 6 meses",
        actions=phase1_actions,
        expected_impact="Bases sólidas para IA + primeiros resultados tangíveis",
    ))

    # ── Fase 2: Escala (6-12 meses) ──────────────────────────────────
    phase2_actions = []
    for _dim_key, label, score in dim_scores[2:4]:
        phase2_actions.append(f"[{label}] Avançar de {score:.1f} para {min(score + 1.0, 5.0):.1f}")

    phase2_actions.append("Implementar pipeline de MLOps para deploy e monitoramento de modelos")
    phase2_actions.append("Criar programa de capacitação em IA para líderes e equipe técnica")
    if len(quick_wins) > 1:
        phase2_actions.append(f"Escalar caso de uso: {quick_wins[1]}")
    phase2_actions.append("Estabelecer métricas de ROI para cada projeto de IA")

    phases.append(RoadmapPhase(
        phase=2,
        title="Escala & Integração",
        horizon="6 – 12 meses",
        actions=phase2_actions,
        expected_impact="IA integrada nos processos-chave com impacto mensurável",
    ))

    # ── Fase 3: Transformação (12-24 meses) ───────────────────────────
    phase3_actions = []
    for _dim_key, label, score in dim_scores[4:]:
        target = min(score + 1.5, 5.0)
        phase3_actions.append(f"[{label}] Atingir nível Avançado/Líder (de {score:.1f} para {target:.1f})")

    phase3_actions.append("Criar centro de excelência em IA (CoE) com squads multidisciplinares")
    phase3_actions.append("Integrar IA no planejamento estratégico corporativo")
    phase3_actions.append("Estabelecer parcerias com universidades e ecossistema de inovação")
    phase3_actions.append("Publicar resultados e cases em conferências do setor")

    phases.append(RoadmapPhase(
        phase=3,
        title="Transformação & Liderança",
        horizon="12 – 24 meses",
        actions=phase3_actions,
        expected_impact="Organização AI-driven com vantagem competitiva sustentável",
    ))

    return RoadmapOut(
        assessment_id=assessment.id,
        company_name=company_name,
        maturity_level=assessment.maturity_level,
        phases=phases,
    )
