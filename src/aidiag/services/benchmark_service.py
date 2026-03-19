"""Serviço de benchmark — comparação com médias setoriais.

Os benchmarks são baseados em dados agregados de pesquisas de mercado
(McKinsey AI Survey 2024, Gartner AI Maturity Model, MIT CISR).
"""

from __future__ import annotations

from aidiag.data.dimensions import DIMENSIONS, SCORE_FIELD_MAP
from aidiag.models import Assessment

# Benchmarks por setor (scores médios por dimensão)
SECTOR_BENCHMARKS: dict[str, dict[str, float]] = {
    "Manufatura": {
        "data": 2.8, "algorithms": 2.3, "governance": 2.0,
        "talent": 2.2, "process": 2.6, "strategy": 2.4,
    },
    "Varejo": {
        "data": 3.1, "algorithms": 2.8, "governance": 2.3,
        "talent": 2.5, "process": 2.7, "strategy": 2.9,
    },
    "Saúde": {
        "data": 2.5, "algorithms": 2.2, "governance": 2.8,
        "talent": 2.3, "process": 2.1, "strategy": 2.2,
    },
    "Financeiro": {
        "data": 3.5, "algorithms": 3.2, "governance": 3.0,
        "talent": 3.0, "process": 3.1, "strategy": 3.3,
    },
    "Agronegócio": {
        "data": 2.2, "algorithms": 1.9, "governance": 1.7,
        "talent": 1.8, "process": 2.0, "strategy": 2.1,
    },
    "Logística": {
        "data": 2.7, "algorithms": 2.4, "governance": 2.1,
        "talent": 2.2, "process": 2.8, "strategy": 2.5,
    },
    "Tecnologia": {
        "data": 3.8, "algorithms": 3.6, "governance": 3.0,
        "talent": 3.5, "process": 3.4, "strategy": 3.6,
    },
    "Educação": {
        "data": 2.1, "algorithms": 1.8, "governance": 2.0,
        "talent": 2.4, "process": 1.9, "strategy": 2.0,
    },
    "Automotivo": {
        "data": 3.0, "algorithms": 2.6, "governance": 2.4,
        "talent": 2.5, "process": 3.0, "strategy": 2.7,
    },
    "Energia": {
        "data": 2.6, "algorithms": 2.1, "governance": 2.3,
        "talent": 2.0, "process": 2.4, "strategy": 2.3,
    },
}


def get_benchmark(sector: str) -> dict[str, float]:
    """Retorna benchmark do setor. Usa Manufatura como fallback."""
    return SECTOR_BENCHMARKS.get(sector, SECTOR_BENCHMARKS["Manufatura"])


def compare_with_benchmark(assessment: Assessment) -> dict:
    """Compara uma avaliação com o benchmark do setor.

    Returns:
        Dicionário com scores da empresa, benchmark e diferenças.
    """
    sector = assessment.company.sector if assessment.company else "Manufatura"
    bench = get_benchmark(sector)

    comparison = []
    for dim_key, dim_info in DIMENSIONS.items():
        field = SCORE_FIELD_MAP[dim_key]
        company_score = getattr(assessment, field)
        bench_score = bench.get(dim_key, 2.0)
        diff = company_score - bench_score

        comparison.append({
            "dimension": dim_key,
            "label": dim_info["label"],
            "company_score": round(company_score, 2),
            "benchmark_score": round(bench_score, 2),
            "difference": round(diff, 2),
            "position": "acima" if diff > 0.2 else ("abaixo" if diff < -0.2 else "na média"),
        })

    overall_company = assessment.overall_score
    overall_bench = sum(bench.values()) / len(bench)

    return {
        "sector": sector,
        "dimensions": comparison,
        "overall_company": round(overall_company, 2),
        "overall_benchmark": round(overall_bench, 2),
        "overall_position": "acima" if overall_company > overall_bench + 0.2 else (
            "abaixo" if overall_company < overall_bench - 0.2 else "na média"
        ),
    }
