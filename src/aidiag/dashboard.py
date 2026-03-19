"""Dashboard Streamlit — interface principal do AI Industry Diagnostics."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from aidiag.data.dimensions import DIMENSIONS, MATURITY_LEVELS
from aidiag.data.use_cases import SECTORS, USE_CASES
from aidiag.services.benchmark_service import SECTOR_BENCHMARKS
from aidiag.services.diagnostic_service import _level_for_score, _recs_for
from aidiag.services.ml_pipeline import train_maturity_classifier
from aidiag.services.roadmap_service import generate_roadmap

# ── Configuração ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Industry Diagnostics",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("AI Industry Diagnostics")
st.markdown(
    "**Plataforma de diagnóstico de maturidade em Inteligência Artificial para o setor produtivo.**  \n"
    "Ferramenta desenvolvida no contexto do CPA CDII (Ciência de Dados para a Indústria Inteligente) — "
    "ICMC-USP / AI2 Advanced Institute for Artificial Intelligence."
)
st.divider()

# ── Sidebar: dados da empresa ─────────────────────────────────────────
st.sidebar.header("Dados da Empresa")
company_name = st.sidebar.text_input("Nome da empresa", "Empresa Demo Ltda")
sector = st.sidebar.selectbox("Setor", SECTORS + ["Tecnologia", "Educação"])
size = st.sidebar.selectbox("Porte", ["micro", "pequena", "media", "grande"], index=2)
city = st.sidebar.text_input("Cidade", "São Paulo")
state = st.sidebar.text_input("Estado (UF)", "SP", max_chars=2)

# ── Tabs ──────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Avaliação",
    "Diagnóstico",
    "Roadmap",
    "Benchmark",
    "Casos de Uso",
    "ML Pipeline",
    "Sobre",
])


# ══════════════════════════════════════════════════════════════════════
# TAB 1: AVALIAÇÃO
# ══════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.header("Avaliação de Maturidade em IA")
    st.markdown(
        "Responda as 30 perguntas abaixo (5 por dimensão) para mapear o nível de maturidade "
        "da empresa em Inteligência Artificial. Cada pergunta é pontuada de 1 (Inicial) a 5 (Líder)."
    )

    with st.expander("Como funciona a pontuação?"):
        score_df = pd.DataFrame([
            {"Nível": v, "Score": k, "Descrição": desc}
            for k, v in MATURITY_LEVELS.items()
            for desc in [
                {
                    1: "Sem iniciativas estruturadas na dimensão avaliada",
                    2: "Primeiros passos com iniciativas isoladas",
                    3: "Práticas estabelecidas com resultados mensuráveis",
                    4: "Excelência operacional com processos otimizados",
                    5: "Referência no mercado com inovação contínua",
                }[k]
            ]
        ])
        st.table(score_df)

    scores: dict[str, float] = {}
    all_answers: dict[str, dict[str, int]] = {}

    for dim_key, dim_info in DIMENSIONS.items():
        st.subheader(f"{dim_info['label']}")
        st.caption(dim_info["description"])

        dim_answers: dict[str, int] = {}
        cols = st.columns(len(dim_info["questions"]))

        for idx, question in enumerate(dim_info["questions"]):
            with cols[idx]:
                options_text = [f"{k} - {v}" for k, v in question["options"].items()]
                selected = st.selectbox(
                    question["text"],
                    options=list(question["options"].keys()),
                    format_func=lambda x, q=question: f"{x} - {q['options'][x][:40]}...",
                    key=f"{dim_key}_{question['id']}",
                )
                dim_answers[question["id"]] = selected

        avg = sum(dim_answers.values()) / len(dim_answers) if dim_answers else 1.0
        scores[dim_key] = round(avg, 2)
        all_answers[dim_key] = dim_answers

    st.divider()
    col_score, col_level = st.columns(2)
    overall = sum(scores.values()) / len(scores)
    with col_score:
        st.metric("Score Geral", f"{overall:.2f} / 5.00")
    with col_level:
        st.metric("Nível de Maturidade", _level_for_score(overall))

    # Salva no session state
    st.session_state["scores"] = scores
    st.session_state["overall"] = overall
    st.session_state["company_name"] = company_name
    st.session_state["sector"] = sector


# ══════════════════════════════════════════════════════════════════════
# TAB 2: DIAGNÓSTICO
# ══════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.header("Relatório de Diagnóstico")
    st.markdown(
        "Visualização analítica dos resultados da avaliação com identificação de "
        "pontos fortes, gaps críticos e recomendações por dimensão."
    )

    sc = st.session_state.get("scores", {})
    if not sc:
        st.info("Preencha a avaliação na aba anterior para gerar o diagnóstico.")
    else:
        ov = st.session_state.get("overall", 0)
        cn = st.session_state.get("company_name", "")

        st.subheader(f"Empresa: {cn}")
        st.metric("Score Geral", f"{ov:.2f}", delta=f"Nível: {_level_for_score(ov)}")

        # Radar chart
        st.subheader("Radar de Maturidade")
        st.caption("Cada eixo representa uma dimensão. A área coberta indica o nível de maturidade geral.")

        labels = [DIMENSIONS[k]["label"] for k in sc]
        values = list(sc.values())

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=cn,
            line={"color": "#1f77b4"},
        ))
        fig_radar.update_layout(
            polar={"radialaxis": {"visible": True, "range": [0, 5]}},
            showlegend=False,
            height=450,
        )
        st.plotly_chart(fig_radar, width="stretch")

        # Barras por dimensão
        st.subheader("Scores por Dimensão")
        st.caption("Barras mostram o score de cada dimensão. Cores indicam o nível: vermelho (baixo) a verde (alto).")

        df_scores = pd.DataFrame([
            {"Dimensão": DIMENSIONS[k]["label"], "Score": v, "Nível": _level_for_score(v)}
            for k, v in sc.items()
        ])
        fig_bar = px.bar(df_scores, x="Dimensão", y="Score", color="Nível", text="Score", height=400)
        fig_bar.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig_bar, width="stretch")

        # Recomendações
        st.subheader("Recomendações por Dimensão")
        for dim_key, score in sc.items():
            label = DIMENSIONS[dim_key]["label"]
            level = _level_for_score(score)
            recs = _recs_for(dim_key, score)
            with st.expander(f"{label} — {score:.1f} ({level})"):
                for r in recs:
                    st.markdown(f"- {r}")

        # Pontos fortes e gaps
        sorted_dims = sorted(sc.items(), key=lambda x: x[1], reverse=True)
        col_str, col_gap = st.columns(2)
        with col_str:
            st.subheader("Pontos Fortes")
            for k, v in sorted_dims[:2]:
                st.success(f"{DIMENSIONS[k]['label']}: {v:.1f}")
        with col_gap:
            st.subheader("Gaps Críticos")
            for k, v in sorted_dims[-2:]:
                st.error(f"{DIMENSIONS[k]['label']}: {v:.1f}")


# ══════════════════════════════════════════════════════════════════════
# TAB 3: ROADMAP
# ══════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.header("Roadmap de Adoção de IA")
    st.markdown(
        "Plano de ação em 4 fases para evolução da maturidade em IA, "
        "gerado automaticamente com base nos gaps identificados na avaliação."
    )

    sc = st.session_state.get("scores", {})
    if not sc:
        st.info("Preencha a avaliação para gerar o roadmap.")
    else:
        ov = st.session_state.get("overall", 0)
        sect = st.session_state.get("sector", "Manufatura")
        cn = st.session_state.get("company_name", "")

        # Simula assessment para o serviço
        class _MockCompany:
            name = cn
            sector = sect

        class _MockAssessment:
            id = "dashboard"
            company = _MockCompany()
            score_data = sc.get("data", 1)
            score_algorithms = sc.get("algorithms", 1)
            score_governance = sc.get("governance", 1)
            score_talent = sc.get("talent", 1)
            score_process = sc.get("process", 1)
            score_strategy = sc.get("strategy", 1)
            overall_score = ov
            maturity_level = _level_for_score(ov)

        roadmap = generate_roadmap(_MockAssessment())

        for phase in roadmap.phases:
            st.subheader(f"Fase {phase.phase}: {phase.title}")
            st.caption(f"Horizonte: {phase.horizon}")

            if phase.investment:
                st.markdown(f"**Investimento estimado:** {phase.investment}")

            for action in phase.actions:
                st.markdown(f"- {action}")

            st.info(f"Impacto esperado: {phase.expected_impact}")

            if phase.kpis:
                with st.expander(f"KPIs da Fase {phase.phase}"):
                    for kpi in phase.kpis:
                        st.markdown(f"- {kpi}")

            if phase.risks:
                with st.expander(f"Riscos da Fase {phase.phase}"):
                    for risk in phase.risks:
                        st.markdown(f"- {risk}")

            st.divider()

        # Timeline visual
        st.subheader("Visão Temporal")
        _phase_starts = [0, 3, 9, 18]
        _phase_durations = [3, 6, 9, 6]
        timeline_df = pd.DataFrame([
            {
                "Fase": f"Fase {p.phase}: {p.title}",
                "Início": _phase_starts[i] if i < len(_phase_starts) else i * 6,
                "Duração": _phase_durations[i] if i < len(_phase_durations) else 6,
            }
            for i, p in enumerate(roadmap.phases)
        ])
        fig_timeline = px.bar(
            timeline_df, x="Duração", y="Fase", orientation="h",
            text="Duração", color="Fase", height=300,
        )
        fig_timeline.update_layout(showlegend=False, xaxis_title="Meses")
        st.plotly_chart(fig_timeline, width="stretch")


# ══════════════════════════════════════════════════════════════════════
# TAB 4: BENCHMARK
# ══════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.header("Benchmark Setorial")
    st.markdown(
        "Compare o nível de maturidade da empresa com a média do setor. "
        "Benchmarks baseados em pesquisas de mercado (McKinsey, Gartner, MIT CISR) "
        "adaptados para o contexto brasileiro."
    )

    sc = st.session_state.get("scores", {})
    sect = st.session_state.get("sector", "Manufatura")

    if not sc:
        st.info("Preencha a avaliação para comparar com o benchmark.")
    else:
        bench = SECTOR_BENCHMARKS.get(sect, SECTOR_BENCHMARKS["Manufatura"])

        labels = [DIMENSIONS[k]["label"] for k in sc]
        company_vals = list(sc.values())
        bench_vals = [bench.get(k, 2.0) for k in sc]

        # Radar comparativo
        st.subheader("Radar Comparativo")
        st.caption(f"Azul: {st.session_state.get('company_name', 'Empresa')} | Vermelho: Média do setor {sect}")

        fig_bench = go.Figure()
        fig_bench.add_trace(go.Scatterpolar(
            r=company_vals + [company_vals[0]],
            theta=labels + [labels[0]],
            fill="toself", name="Empresa", line={"color": "#1f77b4"},
        ))
        fig_bench.add_trace(go.Scatterpolar(
            r=bench_vals + [bench_vals[0]],
            theta=labels + [labels[0]],
            fill="toself", name=f"Média {sect}", line={"color": "#d62728"},
            opacity=0.4,
        ))
        fig_bench.update_layout(
            polar={"radialaxis": {"visible": True, "range": [0, 5]}},
            height=450,
        )
        st.plotly_chart(fig_bench, width="stretch")

        # Tabela comparativa
        st.subheader("Comparação Detalhada")
        comp_data = []
        for dim_key in sc:
            cs = sc[dim_key]
            bs = bench.get(dim_key, 2.0)
            diff = cs - bs
            comp_data.append({
                "Dimensão": DIMENSIONS[dim_key]["label"],
                "Empresa": f"{cs:.1f}",
                "Benchmark": f"{bs:.1f}",
                "Diferença": f"{diff:+.1f}",
                "Posição": "Acima" if diff > 0.2 else ("Abaixo" if diff < -0.2 else "Na média"),
            })
        st.dataframe(pd.DataFrame(comp_data), width="stretch", hide_index=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 5: CASOS DE USO
# ══════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.header("Catálogo de Casos de Uso de IA")
    st.markdown(
        "Casos de uso de IA organizados por setor, com indicação de complexidade, "
        "impacto e nível mínimo de maturidade necessário para implementação."
    )

    selected_sector = st.selectbox("Filtrar por setor", SECTORS, key="uc_sector")
    ov = st.session_state.get("overall", 0)

    cases = USE_CASES.get(selected_sector, [])
    for case in cases:
        viable = ov >= case["min_maturity"] if ov > 0 else True
        icon = "white_check_mark" if viable else "warning"

        with st.expander(f"{'✅' if viable else '⚠️'} {case['name']} — Impacto: {case['impact']}"):
            st.markdown(case["description"])
            col1, col2, col3 = st.columns(3)
            col1.metric("Complexidade", case["complexity"])
            col2.metric("Impacto", case["impact"])
            col3.metric("Maturidade Mínima", f"{case['min_maturity']:.1f}")
            st.markdown(f"**Tecnologias:** {', '.join(case['technologies'])}")
            if not viable:
                st.warning(
                    f"A empresa precisa atingir maturidade {case['min_maturity']:.1f} "
                    f"para este caso de uso (atual: {ov:.1f})."
                )


# ══════════════════════════════════════════════════════════════════════
# TAB 6: ML PIPELINE
# ══════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.header("Pipeline de Machine Learning")
    st.markdown(
        "Demonstração de um pipeline de ML completo: treina classificadores "
        "(Random Forest e Gradient Boosting) para predizer o nível de maturidade "
        "a partir dos 6 scores dimensionais. Inclui cross-validation, feature importance "
        "e comparação de modelos."
    )

    if st.button("Treinar Modelos", type="primary"):
        with st.spinner("Treinando Random Forest e Gradient Boosting..."):
            results = train_maturity_classifier()

        st.success(f"Modelos treinados com {results['n_samples']} amostras sintéticas.")

        # Comparação de modelos
        st.subheader("Comparação de Modelos")
        st.caption("Cross-validation com 5 folds. F1 Macro mede performance balanceada entre classes.")

        model_comp = pd.DataFrame([
            {
                "Modelo": "Random Forest",
                "CV F1 (média)": f"{results['random_forest']['cv_f1_mean']:.4f}",
                "CV F1 (std)": f"{results['random_forest']['cv_f1_std']:.4f}",
                "Acurácia (treino)": f"{results['random_forest']['train_accuracy']:.4f}",
            },
            {
                "Modelo": "Gradient Boosting",
                "CV F1 (média)": f"{results['gradient_boosting']['cv_f1_mean']:.4f}",
                "CV F1 (std)": f"{results['gradient_boosting']['cv_f1_std']:.4f}",
                "Acurácia (treino)": f"{results['gradient_boosting']['train_accuracy']:.4f}",
            },
        ])
        st.dataframe(model_comp, width="stretch", hide_index=True)

        # Feature importances
        st.subheader("Feature Importances")
        st.caption(
            "Quais dimensões mais influenciam na classificação de maturidade. "
            "Importâncias normalizadas (somam 1.0)."
        )

        for model_name, model_key in [("Random Forest", "random_forest"), ("Gradient Boosting", "gradient_boosting")]:
            importances = results[model_key]["feature_importances"]
            fig_imp = px.bar(
                x=list(importances.values()),
                y=list(importances.keys()),
                orientation="h",
                title=model_name,
                labels={"x": "Importância", "y": "Dimensão"},
                height=300,
            )
            st.plotly_chart(fig_imp, width="stretch")

        # Classification report
        st.subheader("Classification Report (Random Forest)")
        report = results["random_forest"]["report"]
        report_rows = []
        for cls in results["label_encoder_classes"]:
            if cls in report:
                r = report[cls]
                report_rows.append({
                    "Classe": cls,
                    "Precision": f"{r['precision']:.3f}",
                    "Recall": f"{r['recall']:.3f}",
                    "F1-Score": f"{r['f1-score']:.3f}",
                    "Support": int(r["support"]),
                })
        st.dataframe(pd.DataFrame(report_rows), width="stretch", hide_index=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 7: SOBRE
# ══════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.header("Sobre o Projeto")
    st.markdown("""
**AI Industry Diagnostics** é uma plataforma de diagnóstico de maturidade em Inteligência Artificial
desenvolvida para o setor produtivo brasileiro.

### Contexto

Este projeto foi desenvolvido no contexto do **CPA CDII — Ciência de Dados para a Indústria Inteligente**,
um Centro de Pesquisa Aplicada apoiado pela FAPESP (processo 2023/14427-8), sediado no
**ICMC-USP** e com parceria do **AI2 — Advanced Institute for Artificial Intelligence**.

O papel do **Consultor de Diagnóstico em IA** é:
- Visitar empresas e mapear oportunidades de uso de IA
- Elaborar roadmaps de adoção personalizados
- Criar a ponte entre as demandas reais do setor produtivo e os pesquisadores do CPA

### Framework de Avaliação

O questionário de 30 perguntas avalia 6 dimensões de maturidade:

| Dimensão | O que avalia |
|---|---|
| **Dados & Infraestrutura** | Qualidade, governança e infra computacional |
| **Algoritmos & Modelos** | Adoção de ML/DL, MLOps e IA generativa |
| **Governança & Ética** | Políticas de uso responsável e compliance |
| **Talentos & Cultura** | Equipe, capacitação e cultura de inovação |
| **Processos & Integração** | Automação, integração e gestão de projetos |
| **Estratégia & Liderança** | Visão, investimento e engajamento executivo |

### Tecnologias

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** Streamlit + Plotly
- **ML:** scikit-learn (Random Forest, Gradient Boosting)
- **Auth:** JWT (python-jose) + bcrypt

### Autor

**Jardel Vieira Alves**
    """)


def main() -> None:
    """Entry point para execução via script."""
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", __file__, "--server.port", "8501"],
        check=True,
    )
