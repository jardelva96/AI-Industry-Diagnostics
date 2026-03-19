"""Pipeline de Machine Learning para classificação de maturidade.

Demonstra um pipeline completo de ML aplicado ao próprio domínio:
dado um conjunto de scores de avaliação, prediz o nível de maturidade
e identifica as features mais importantes para a classificação.
"""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder

FEATURE_NAMES = [
    "Dados & Infra",
    "Algoritmos & Modelos",
    "Governança & Ética",
    "Talentos & Cultura",
    "Processos & Integração",
    "Estratégia & Liderança",
]

MATURITY_LABELS = ["Inicial", "Básico", "Intermediário", "Avançado", "Líder"]


def _generate_synthetic_data(n_samples: int = 500, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """Gera dados sintéticos realistas de avaliações de maturidade.

    Simula o comportamento esperado: empresas tendem a ter scores correlacionados
    entre dimensões, com alguma variância.
    """
    rng = np.random.default_rng(seed)

    features_list = []
    labels = []

    for _ in range(n_samples):
        # Base de maturidade da empresa (determina o perfil geral)
        base = rng.uniform(1.0, 5.0)
        # Cada dimensão varia em torno da base
        scores = np.clip(base + rng.normal(0, 0.6, size=6), 1.0, 5.0)
        features_list.append(scores)

        avg = float(np.mean(scores))
        if avg < 1.5:
            labels.append("Inicial")
        elif avg < 2.5:
            labels.append("Básico")
        elif avg < 3.5:
            labels.append("Intermediário")
        elif avg < 4.5:
            labels.append("Avançado")
        else:
            labels.append("Líder")

    return np.array(features_list), np.array(labels)


def train_maturity_classifier(seed: int = 42) -> dict:
    """Treina um classificador de nível de maturidade e retorna métricas.

    Returns:
        Dicionário com modelo, métricas, feature importances e report.
    """
    x_data, y_data = _generate_synthetic_data(seed=seed)
    le = LabelEncoder()
    le.fit(MATURITY_LABELS)
    y_encoded = le.transform(y_data)

    # Treina dois modelos para comparação
    rf = RandomForestClassifier(n_estimators=100, random_state=seed, max_depth=8)
    gb = GradientBoostingClassifier(n_estimators=100, random_state=seed, max_depth=5, learning_rate=0.1)

    # Cross-validation
    rf_scores = cross_val_score(rf, x_data, y_encoded, cv=5, scoring="f1_macro")
    gb_scores = cross_val_score(gb, x_data, y_encoded, cv=5, scoring="f1_macro")

    # Treina no dataset completo para feature importances
    rf.fit(x_data, y_encoded)
    gb.fit(x_data, y_encoded)

    rf_pred = rf.predict(x_data)
    gb_pred = gb.predict(x_data)

    # Feature importances
    rf_importances = dict(zip(FEATURE_NAMES, rf.feature_importances_.tolist(), strict=True))
    gb_importances = dict(zip(FEATURE_NAMES, gb.feature_importances_.tolist(), strict=True))

    return {
        "random_forest": {
            "cv_f1_mean": float(np.mean(rf_scores)),
            "cv_f1_std": float(np.std(rf_scores)),
            "train_accuracy": float(accuracy_score(y_encoded, rf_pred)),
            "train_f1": float(f1_score(y_encoded, rf_pred, average="macro")),
            "feature_importances": rf_importances,
            "report": classification_report(y_encoded, rf_pred, target_names=le.classes_, output_dict=True),
        },
        "gradient_boosting": {
            "cv_f1_mean": float(np.mean(gb_scores)),
            "cv_f1_std": float(np.std(gb_scores)),
            "train_accuracy": float(accuracy_score(y_encoded, gb_pred)),
            "train_f1": float(f1_score(y_encoded, gb_pred, average="macro")),
            "feature_importances": gb_importances,
            "report": classification_report(y_encoded, gb_pred, target_names=le.classes_, output_dict=True),
        },
        "feature_names": FEATURE_NAMES,
        "label_encoder_classes": le.classes_.tolist(),
        "n_samples": len(x_data),
    }


def predict_maturity(scores: list[float], seed: int = 42) -> dict:
    """Prediz o nível de maturidade a partir de 6 scores de dimensão.

    Args:
        scores: Lista com 6 scores (1.0-5.0), um por dimensão.

    Returns:
        Dicionário com predição, probabilidades e explicação.
    """
    if len(scores) != 6:
        msg = f"Esperados 6 scores, recebidos {len(scores)}"
        raise ValueError(msg)

    x_data, y_data = _generate_synthetic_data(seed=seed)
    le = LabelEncoder()
    le.fit(MATURITY_LABELS)
    y_encoded = le.transform(y_data)

    rf = RandomForestClassifier(n_estimators=100, random_state=seed, max_depth=8)
    rf.fit(x_data, y_encoded)

    x_input = np.array(scores).reshape(1, -1)
    pred_encoded = rf.predict(x_input)[0]
    probas = rf.predict_proba(x_input)[0]

    pred_label = le.inverse_transform([pred_encoded])[0]
    proba_dict = dict(zip(le.classes_.tolist(), probas.tolist(), strict=True))

    return {
        "predicted_level": pred_label,
        "probabilities": proba_dict,
        "scores_input": dict(zip(FEATURE_NAMES, scores, strict=True)),
    }
