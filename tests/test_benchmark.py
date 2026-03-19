"""Testes para o serviço de benchmark."""

from __future__ import annotations

from aidiag.services.benchmark_service import compare_with_benchmark, get_benchmark


def test_get_benchmark_known_sector():
    """Benchmark retorna dados para setor conhecido."""
    bench = get_benchmark("Financeiro")
    assert len(bench) == 6
    assert all(1.0 <= v <= 5.0 for v in bench.values())


def test_get_benchmark_unknown_sector():
    """Setor desconhecido retorna Manufatura como fallback."""
    bench = get_benchmark("Setor Inexistente")
    assert bench == get_benchmark("Manufatura")


def test_compare_with_benchmark(sample_assessment):
    """Comparação gera dados para todas as dimensões."""
    result = compare_with_benchmark(sample_assessment)

    assert result["sector"] == "Manufatura"
    assert len(result["dimensions"]) == 6
    assert result["overall_company"] > 0
    assert result["overall_benchmark"] > 0
    assert result["overall_position"] in {"acima", "abaixo", "na média"}


def test_comparison_positions(sample_assessment):
    """Cada dimensão tem posição relativa definida."""
    result = compare_with_benchmark(sample_assessment)

    for dim in result["dimensions"]:
        assert dim["position"] in {"acima", "abaixo", "na média"}
        assert "company_score" in dim
        assert "benchmark_score" in dim
