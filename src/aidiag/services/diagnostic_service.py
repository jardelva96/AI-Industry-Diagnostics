"""Serviço de diagnóstico — transforma scores em relatório analítico."""

from __future__ import annotations

from aidiag.data.dimensions import DIMENSIONS, SCORE_FIELD_MAP
from aidiag.models import Assessment
from aidiag.schemas import DiagnosticReport, DimensionDetail

# Recomendações por dimensão e faixa de score
_RECOMMENDATIONS: dict[str, dict[str, list[str]]] = {
    "data": {
        "low": [
            "Centralizar dados em um data warehouse ou data lake",
            "Implementar processos básicos de data quality",
            "Mapear todas as fontes de dados disponíveis",
        ],
        "mid": [
            "Adotar catálogo de dados com metadados padronizados",
            "Implementar pipelines de ETL/ELT automatizados",
            "Desenvolver política de LGPD com DPO designado",
        ],
        "high": [
            "Evoluir para arquitetura data mesh com ownership distribuído",
            "Implementar data quality automatizado com ML",
            "Criar programa de dados abertos e data marketplace interno",
        ],
    },
    "algorithms": {
        "low": [
            "Iniciar com casos de uso simples (classificação, regressão)",
            "Capacitar equipe em ferramentas de ML (scikit-learn, pandas)",
            "Criar ambiente de experimentação (notebooks, sandbox)",
        ],
        "mid": [
            "Implementar MLOps com versionamento de modelos",
            "Adotar práticas de explicabilidade (SHAP, LIME)",
            "Iniciar pilotos com IA generativa em processos internos",
        ],
        "high": [
            "Implementar feature store e model registry",
            "Criar plataforma de AutoML para democratizar ML",
            "Integrar LLMs fine-tuned com RAG em produção",
        ],
    },
    "governance": {
        "low": [
            "Criar política básica de uso de IA na empresa",
            "Designar responsável por ética em IA",
            "Mapear riscos algorítmicos nos processos existentes",
        ],
        "mid": [
            "Estabelecer comitê de ética em IA com revisão periódica",
            "Implementar testes de fairness em modelos críticos",
            "Criar model cards para todos os modelos em produção",
        ],
        "high": [
            "Alinhar framework ao EU AI Act e regulações setoriais",
            "Implementar auditoria externa de modelos",
            "Criar programa de transparência algorítmica com opt-out",
        ],
    },
    "talent": {
        "low": [
            "Contratar primeiro cientista de dados ou analista de IA",
            "Investir em capacitação básica para equipe existente",
            "Criar cultura de dados com workshops e data literacy",
        ],
        "mid": [
            "Formar equipe dedicada de dados/IA (3-5 pessoas)",
            "Criar trilhas de aprendizado por role com certificações",
            "Implementar hackathons internos e tempo para inovação",
        ],
        "high": [
            "Criar centro de excelência em IA (CoE)",
            "Estabelecer parcerias com universidades e programas de mestrado",
            "Desenvolver employer branding focado em dados/IA",
        ],
    },
    "process": {
        "low": [
            "Identificar processos manuais candidatos a automação",
            "Implementar RPA em processos repetitivos de alto volume",
            "Definir KPIs de negócio para projetos de IA",
        ],
        "mid": [
            "Criar APIs de integração entre IA e sistemas core",
            "Implementar CI/CD para modelos com testes automatizados",
            "Medir ROI de cada projeto de IA com baseline definido",
        ],
        "high": [
            "Evoluir para microsserviços de IA com event-driven",
            "Implementar plataforma de MLOps completa",
            "Adotar product-led AI com squads multidisciplinares",
        ],
    },
    "strategy": {
        "low": [
            "Incluir IA na pauta estratégica da liderança",
            "Visitar empresas referência em IA no setor",
            "Definir orçamento inicial para experimentação com IA",
        ],
        "mid": [
            "Criar roadmap de IA integrado ao planejamento estratégico",
            "Designar sponsor executivo para iniciativas de IA",
            "Participar de ecossistemas de inovação e grupos de trabalho",
        ],
        "high": [
            "Posicionar IA como pilar central da estratégia corporativa",
            "Criar venture arm ou programa de co-criação com startups",
            "Publicar resultados e cases em conferências e papers",
        ],
    },
}


def _level_for_score(score: float) -> str:
    """Retorna o nível textual para um score numérico."""
    if score < 1.5:
        return "Inicial"
    if score < 2.5:
        return "Básico"
    if score < 3.5:
        return "Intermediário"
    if score < 4.5:
        return "Avançado"
    return "Líder"


def _recs_for(dim: str, score: float) -> list[str]:
    """Seleciona recomendações baseadas no score."""
    bucket = _RECOMMENDATIONS.get(dim, {})
    if score < 2.5:
        return bucket.get("low", [])
    if score < 4.0:
        return bucket.get("mid", [])
    return bucket.get("high", [])


def generate_diagnostic(assessment: Assessment) -> DiagnosticReport:
    """Gera relatório de diagnóstico completo a partir de uma avaliação."""
    dimensions: list[DimensionDetail] = []
    scores_list: list[tuple[str, float]] = []

    for dim_key, dim_info in DIMENSIONS.items():
        field = SCORE_FIELD_MAP[dim_key]
        score = getattr(assessment, field)
        gap = 5.0 - score
        level = _level_for_score(score)
        recs = _recs_for(dim_key, score)

        dimensions.append(DimensionDetail(
            dimension=dim_key,
            label=dim_info["label"],
            score=round(score, 2),
            level=level,
            gap=round(gap, 2),
            recommendations=recs,
        ))
        scores_list.append((dim_info["label"], score))

    # Ordena para identificar pontos fortes e gaps críticos
    scores_list.sort(key=lambda x: x[1], reverse=True)
    top_strengths = [f"{name} ({s:.1f})" for name, s in scores_list[:2]]
    critical_gaps = [f"{name} ({s:.1f})" for name, s in scores_list[-2:]]

    company_name = assessment.company.name if assessment.company else "N/A"

    return DiagnosticReport(
        assessment_id=assessment.id,
        company_name=company_name,
        overall_score=round(assessment.overall_score, 2),
        maturity_level=assessment.maturity_level,
        dimensions=dimensions,
        top_strengths=top_strengths,
        critical_gaps=critical_gaps,
    )
