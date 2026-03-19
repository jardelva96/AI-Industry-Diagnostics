"""Testes para o pipeline de ML."""

from __future__ import annotations

import pytest

from aidiag.services.ml_pipeline import (
    FEATURE_NAMES,
    predict_maturity,
    train_maturity_classifier,
)


def test_train_returns_both_models():
    """Treinamento retorna métricas para RF e GB."""
    results = train_maturity_classifier()

    assert "random_forest" in results
    assert "gradient_boosting" in results
    assert results["n_samples"] == 500


def test_cv_f1_above_threshold():
    """Cross-validation F1 acima de 0.80 (sanity check)."""
    results = train_maturity_classifier()

    assert results["random_forest"]["cv_f1_mean"] > 0.80
    assert results["gradient_boosting"]["cv_f1_mean"] > 0.80


def test_feature_importances():
    """Feature importances têm as 6 dimensões."""
    results = train_maturity_classifier()

    for model_key in ("random_forest", "gradient_boosting"):
        importances = results[model_key]["feature_importances"]
        assert len(importances) == 6
        assert all(name in importances for name in FEATURE_NAMES)
        assert abs(sum(importances.values()) - 1.0) < 0.01


def test_predict_maturity():
    """Predição retorna nível de maturidade válido."""
    result = predict_maturity([3.0, 3.0, 3.0, 3.0, 3.0, 3.0])

    assert result["predicted_level"] in {"Inicial", "Básico", "Intermediário", "Avançado", "Líder"}
    assert len(result["probabilities"]) == 5
    assert len(result["scores_input"]) == 6


def test_predict_invalid_input():
    """Predição com input inválido levanta ValueError."""
    with pytest.raises(ValueError, match="Esperados 6 scores"):
        predict_maturity([1.0, 2.0])


def test_reproducibility():
    """Resultados são reproduzíveis com mesma seed."""
    r1 = train_maturity_classifier(seed=42)
    r2 = train_maturity_classifier(seed=42)

    assert r1["random_forest"]["cv_f1_mean"] == r2["random_forest"]["cv_f1_mean"]
