"""Dashboard Streamlit — interface de diagnóstico de maturidade em IA para indústria."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from aidiag.data.dimensions import DIMENSIONS, MATURITY_LEVELS
from aidiag.data.use_cases import SECTORS, USE_CASES
from aidiag.schemas import DimensionDetail
from aidiag.services.benchmark_service import SECTOR_BENCHMARKS
from aidiag.services.diagnostic_service import (
    _level_for_score,
    _recs_for,
    generate_executive_summary,
    identify_quick_wins,
)
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
    "**Plataforma de diagnóstico de maturidade em Inteligência Artificial para o setor produtivo.**"
)
st.caption(
    "Fluxo recomendado: preencha a **Avaliação** → consulte o **Diagnóstico** → "
    "veja os **Quick Wins** → explore o **Roadmap** completo."
)
st.divider()

# ── Sidebar: dados da empresa ─────────────────────────────────────────
st.sidebar.header("Dados da Empresa")
company_name = st.sidebar.text_input("Nome da empresa", "Empresa Demo Ltda")
sector = st.sidebar.selectbox("Setor", SECTORS)
size = st.sidebar.selectbox("Porte", ["micro", "pequena", "media", "grande"], index=2)
city = st.sidebar.text_input("Cidade", "São Paulo")
state = st.sidebar.text_input("Estado (UF)", "SP", max_chars=2)

st.sidebar.divider()
st.sidebar.caption(
    "Esta ferramenta foi projetada para uso em visitas de diagnóstico a empresas. "
    "Os dados inseridos aqui contextualizam a avaliação e o roadmap gerado."
)

# ── Tabs ──────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Avaliação",
    "Diagnóstico",
    "Quick Wins",
    "Roadmap",
    "Benchmark Setorial",
    "Casos de Uso",
    "Sobre",
])


# ══════════════════════════════════════════════════════════════════════
# TAB 1: AVALIAÇÃO
# ══════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.header("Avaliação de Maturidade em IA")
    st.markdown(
        "Este questionário avalia **6 dimensões** da maturidade em Inteligência Artificial "
        "da empresa, com **5 perguntas por dimensão** (30 no total). A avaliação é projetada "
        "para ser preenchida durante uma visita de diagnóstico, em conversa com gestores "
        "de diferentes áreas."
    )
    st.info(
        "**Dica para o consultor:** aplique as perguntas em entrevistas de 60-90 minutos "
        "com representantes de TI, operações, RH e diretoria. Scores devem refletir a "
        "realidade atual, não planos futuros."
    )

    with st.expander("Escala de pontuação — o que cada nível significa"):
        score_df = pd.DataFrame([
            {
                "Nível": v,
                "Score": k,
                "O que significa na prática": {
                    1: "Sem iniciativas estruturadas. A empresa não utiliza IA de forma intencional.",
                    2: "Primeiros passos com iniciativas isoladas, geralmente lideradas por indivíduos.",
                    3: "Práticas estabelecidas com resultados mensuráveis em pelo menos uma área.",
                    4: "Excelência operacional com processos otimizados e IA integrada ao negócio.",
                    5: "Referência no setor com inovação contínua e IA como vantagem competitiva.",
                }[k],
            }
            for k, v in MATURITY_LEVELS.items()
        ])
        st.table(score_df)

    scores: dict[str, float] = {}
    all_answers: dict[str, dict[str, int]] = {}
    total_questions = sum(len(d["questions"]) for d in DIMENSIONS.values())
    answered = 0

    for dim_key, dim_info in DIMENSIONS.items():
        st.subheader(f"{dim_info['label']}")
        st.caption(dim_info["description"])

        dim_answers: dict[str, int] = {}
        cols = st.columns(len(dim_info["questions"]))

        for idx, question in enumerate(dim_info["questions"]):
            with cols[idx]:
                selected = st.selectbox(
                    question["text"],
                    options=list(question["options"].keys()),
                    format_func=lambda x, q=question: f"{x} - {q['options'][x][:40]}...",
                    key=f"{dim_key}_{question['id']}",
                )
                dim_answers[question["id"]] = selected
                answered += 1

        avg = sum(dim_answers.values()) / len(dim_answers) if dim_answers else 1.0
        scores[dim_key] = round(avg, 2)
        all_answers[dim_key] = dim_answers

    st.divider()

    # Resultado da avaliação
    overall = sum(scores.values()) / len(scores)
    level = _level_for_score(overall)

    col_score, col_level, col_progress = st.columns(3)
    with col_score:
        st.metric("Score Geral", f"{overall:.2f} / 5.00")
    with col_level:
        st.metric("Nível de Maturidade", level)
    with col_progress:
        st.metric("Perguntas respondidas", f"{answered}/{total_questions}")

    # Interpretação do resultado
    if overall < 2.0:
        st.warning(
            f"**{company_name}** está no nível **Inicial** de maturidade em IA. "
            "A empresa precisa estabelecer fundamentos básicos antes de investir em projetos "
            "de IA. Recomendamos começar pelos Quick Wins na próxima aba."
        )
    elif overall < 3.0:
        st.info(
            f"**{company_name}** está no nível **Básico**. Existem iniciativas pontuais "
            "que podem ser aceleradas. O foco deve ser em consolidar infraestrutura e "
            "governança para escalar."
        )
    elif overall < 4.0:
        st.success(
            f"**{company_name}** está no nível **Intermediário**. A empresa já colhe "
            "resultados de IA e está pronta para escalar e integrar de forma mais profunda."
        )
    else:
        st.success(
            f"**{company_name}** está no nível **Avançado/Líder**. A empresa é referência "
            "e deve focar em inovação contínua e vantagem competitiva sustentável."
        )

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

    sc = st.session_state.get("scores", {})
    if not sc:
        st.info("Preencha a avaliação na aba anterior para gerar o diagnóstico.")
    else:
        ov = st.session_state.get("overall", 0)
        cn = st.session_state.get("company_name", "")

        # ── Sumário Executivo ──
        st.subheader("Sumário Executivo")
        st.caption(
            "Este resumo pode ser apresentado diretamente à diretoria da empresa. "
            "Ele sintetiza o diagnóstico em linguagem de negócio."
        )

        # Monta dados para o sumário
        dims: list[DimensionDetail] = []
        for dim_key, score in sc.items():
            dims.append(DimensionDetail(
                dimension=dim_key,
                label=DIMENSIONS[dim_key]["label"],
                score=score,
                level=_level_for_score(score),
                gap=round(5.0 - score, 2),
                recommendations=_recs_for(dim_key, score),
            ))

        sorted_dims = sorted(dims, key=lambda d: d.score, reverse=True)
        top_str = [f"{d.label} ({d.score:.1f})" for d in sorted_dims[:2]]
        crit_gaps = [f"{d.label} ({d.score:.1f})" for d in sorted_dims[-2:]]

        exec_summary = generate_executive_summary(
            company_name=cn,
            overall_score=ov,
            maturity_level=_level_for_score(ov),
            dimensions=dims,
            top_strengths=top_str,
            critical_gaps=crit_gaps,
        )

        st.text_area(
            "Resumo para apresentação executiva",
            value=exec_summary,
            height=300,
            disabled=True,
        )

        st.divider()

        # ── Radar de Maturidade ──
        st.subheader("Radar de Maturidade")
        st.caption(
            "Cada eixo representa uma dimensão estratégica. A área coberta indica "
            "o nível geral — quanto mais preenchido, mais madura a empresa em IA."
        )

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

        # ── Barras por dimensão ──
        st.subheader("Scores por Dimensão")
        st.caption(
            "Verde = ponto forte da empresa. Amarelo = nível intermediário. "
            "Vermelho = gap crítico que precisa de atenção prioritária."
        )

        df_scores = pd.DataFrame([
            {"Dimensão": DIMENSIONS[k]["label"], "Score": v, "Nível": _level_for_score(v)}
            for k, v in sc.items()
        ])
        fig_bar = px.bar(
            df_scores, x="Dimensão", y="Score", color="Nível",
            text="Score", height=400,
            color_discrete_map={
                "Inicial": "#d32f2f", "Básico": "#ff9800",
                "Intermediário": "#fdd835", "Avançado": "#4caf50", "Líder": "#1b5e20",
            },
        )
        fig_bar.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig_bar, width="stretch")

        # ── Recomendações por Dimensão ──
        st.subheader("Recomendações por Dimensão")
        st.caption(
            "Cada recomendação é uma ação concreta que a empresa pode tomar. "
            "As recomendações são calibradas pelo nível atual de maturidade."
        )

        for dim_key, score in sc.items():
            label = DIMENSIONS[dim_key]["label"]
            level_txt = _level_for_score(score)
            recs = _recs_for(dim_key, score)
            with st.expander(f"{label} — {score:.1f} ({level_txt})"):
                for r in recs:
                    st.markdown(f"- {r}")

        # ── Pontos fortes e gaps ──
        sorted_sc = sorted(sc.items(), key=lambda x: x[1], reverse=True)
        col_str, col_gap = st.columns(2)
        with col_str:
            st.subheader("Pontos Fortes")
            for k, v in sorted_sc[:2]:
                st.success(f"{DIMENSIONS[k]['label']}: {v:.1f}")
        with col_gap:
            st.subheader("Gaps Críticos")
            for k, v in sorted_sc[-2:]:
                st.error(f"{DIMENSIONS[k]['label']}: {v:.1f}")


# ══════════════════════════════════════════════════════════════════════
# TAB 3: QUICK WINS
# ══════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.header("Quick Wins — Ações de Impacto Rápido")
    st.markdown(
        "Ações de **baixo esforço e alto impacto** que a empresa pode implementar "
        "nos próximos **30 a 90 dias**. Essas vitórias rápidas constroem confiança "
        "na liderança e criam momentum para projetos maiores."
    )

    sc = st.session_state.get("scores", {})
    if not sc:
        st.info("Preencha a avaliação para identificar os quick wins.")
    else:
        # Monta dimensions para o serviço
        dims_for_qw: list[DimensionDetail] = []
        for dim_key, score in sc.items():
            dims_for_qw.append(DimensionDetail(
                dimension=dim_key,
                label=DIMENSIONS[dim_key]["label"],
                score=score,
                level=_level_for_score(score),
                gap=round(5.0 - score, 2),
                recommendations=[],
            ))

        quick_wins = identify_quick_wins(dims_for_qw)

        if quick_wins:
            for i, qw in enumerate(quick_wins, 1):
                with st.container():
                    st.subheader(f"{i}. {qw.action}")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Dimensão", qw.dimension)
                    col2.metric("Esforço", qw.effort)
                    col3.metric("Prazo estimado", qw.expected_timeline)
                    st.markdown(f"**Impacto no negócio:** {qw.business_impact}")
                    st.divider()
        else:
            st.success(
                "A empresa já apresenta maturidade elevada em todas as dimensões. "
                "Consulte o Roadmap para ações de otimização avançada."
            )

        # Quick wins de casos de uso do setor
        sect = st.session_state.get("sector", "Manufatura")
        sector_cases = USE_CASES.get(sect, [])
        qw_cases = [c for c in sector_cases if c.get("quick_win", False)]

        if qw_cases:
            st.subheader(f"Quick Wins por Setor — {sect}")
            st.caption(
                "Casos de uso de IA classificados como rápidos de implementar "
                "no setor da empresa avaliada."
            )
            for case in qw_cases:
                with st.expander(
                    f"✅ {case['name']} — ROI: {case.get('roi_estimate', 'N/A')}"
                ):
                    st.markdown(case["description"])
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Complexidade", case["complexity"])
                    c2.metric("Impacto", case["impact"])
                    c3.metric("Maturidade Mínima", f"{case['min_maturity']:.1f}")
                    st.markdown(f"**Tecnologias:** {', '.join(case['technologies'])}")


# ══════════════════════════════════════════════════════════════════════
# TAB 4: ROADMAP
# ══════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.header("Roadmap de Adoção de IA")
    st.markdown(
        "Plano de ação em **4 fases** para evolução da maturidade em IA, "
        "gerado automaticamente com base nos gaps identificados. Cada fase inclui "
        "ações, investimento estimado, riscos e indicadores de sucesso (KPIs)."
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

        # Visão geral das fases
        st.subheader("Visão Geral")
        phase_overview = pd.DataFrame([
            {
                "Fase": f"{p.phase}. {p.title}",
                "Horizonte": p.horizon,
                "Investimento": p.investment,
                "Nº Ações": len(p.actions),
            }
            for p in roadmap.phases
        ])
        st.dataframe(phase_overview, width="stretch", hide_index=True)

        # Timeline visual
        st.subheader("Linha do Tempo")
        st.caption("Horizonte de cada fase em meses.")

        timeline_data = []
        start_months = [0, 3, 9, 18]
        durations = [3, 6, 9, 6]
        for i, p in enumerate(roadmap.phases):
            timeline_data.append({
                "Fase": f"Fase {p.phase}: {p.title}",
                "Início (mês)": start_months[i] if i < len(start_months) else i * 6,
                "Duração (meses)": durations[i] if i < len(durations) else 6,
            })

        fig_timeline = px.bar(
            pd.DataFrame(timeline_data),
            x="Duração (meses)", y="Fase", orientation="h",
            text="Duração (meses)", color="Fase", height=280,
        )
        fig_timeline.update_layout(showlegend=False, xaxis_title="Meses")
        st.plotly_chart(fig_timeline, width="stretch")

        st.divider()

        # Detalhamento por fase
        investment_colors = {"Baixo": "🟢", "Médio": "🟡", "Alto": "🔴"}

        for phase in roadmap.phases:
            inv_icon = investment_colors.get(phase.investment, "⚪")
            st.subheader(f"Fase {phase.phase}: {phase.title}")
            st.caption(
                f"Horizonte: {phase.horizon} | "
                f"Investimento: {inv_icon} {phase.investment}"
            )

            # Ações
            st.markdown("**Ações:**")
            for action in phase.actions:
                st.markdown(f"- {action}")

            st.info(f"**Impacto esperado:** {phase.expected_impact}")

            # KPIs e Riscos em colunas
            col_kpi, col_risk = st.columns(2)

            with col_kpi:
                st.markdown("**KPIs de Sucesso:**")
                for kpi in phase.kpis:
                    st.markdown(f"- {kpi}")

            with col_risk:
                st.markdown("**Riscos e Mitigação:**")
                for risk in phase.risks:
                    st.markdown(f"- ⚠️ {risk}")

            st.divider()


# ══════════════════════════════════════════════════════════════════════
# TAB 5: BENCHMARK SETORIAL
# ══════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.header("Benchmark Setorial")
    st.markdown(
        "Compare o nível de maturidade da empresa com a **média do setor** no Brasil. "
        "Benchmarks baseados em pesquisas de mercado (McKinsey, Gartner, MIT CISR) "
        "adaptados para o contexto do **setor produtivo brasileiro**."
    )
    st.caption(
        "O benchmark responde à pergunta mais frequente da liderança: "
        "'estamos atrás ou à frente dos concorrentes em IA?'"
    )

    sc = st.session_state.get("scores", {})
    sect = st.session_state.get("sector", "Manufatura")

    if not sc:
        st.info("Preencha a avaliação para comparar com o benchmark.")
    else:
        bench = SECTOR_BENCHMARKS.get(sect, SECTOR_BENCHMARKS.get("Manufatura", {}))

        labels = [DIMENSIONS[k]["label"] for k in sc]
        company_vals = list(sc.values())
        bench_vals = [bench.get(k, 2.0) for k in sc]

        # Radar comparativo
        st.subheader("Radar Comparativo")
        cn = st.session_state.get("company_name", "Empresa")
        st.caption(f"🔵 {cn} | 🔴 Média do setor {sect}")

        fig_bench = go.Figure()
        fig_bench.add_trace(go.Scatterpolar(
            r=company_vals + [company_vals[0]],
            theta=labels + [labels[0]],
            fill="toself", name=cn, line={"color": "#1f77b4"},
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
        st.caption(
            "Diferença positiva = empresa acima da média do setor. "
            "Diferença negativa = oportunidade de melhoria prioritária."
        )

        comp_data = []
        for dim_key in sc:
            cs = sc[dim_key]
            bs = bench.get(dim_key, 2.0)
            diff = cs - bs
            comp_data.append({
                "Dimensão": DIMENSIONS[dim_key]["label"],
                "Empresa": f"{cs:.1f}",
                "Média Setor": f"{bs:.1f}",
                "Diferença": f"{diff:+.1f}",
                "Posição": (
                    "✅ Acima" if diff > 0.2
                    else ("❌ Abaixo" if diff < -0.2 else "➡️ Na média")
                ),
            })
        st.dataframe(
            pd.DataFrame(comp_data), width="stretch", hide_index=True,
        )

        # Contexto setorial
        above = sum(1 for d in comp_data if "Acima" in d["Posição"])
        below = sum(1 for d in comp_data if "Abaixo" in d["Posição"])

        if above > below:
            st.success(
                f"A empresa está **acima da média** em {above} de 6 dimensões. "
                "Posição competitiva favorável em IA no setor."
            )
        elif below > above:
            st.warning(
                f"A empresa está **abaixo da média** em {below} de 6 dimensões. "
                "É preciso acelerar a adoção para não perder competitividade."
            )
        else:
            st.info(
                "A empresa está **na média** do setor. "
                "Há oportunidade de se diferenciar."
            )


# ══════════════════════════════════════════════════════════════════════
# TAB 6: CASOS DE USO
# ══════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.header("Catálogo de Casos de Uso de IA")
    st.markdown(
        "Casos de uso de IA organizados por **setor industrial**, com indicação de "
        "complexidade, impacto no negócio, maturidade mínima e estimativa de ROI. "
        "Use este catálogo nas visitas para apresentar oportunidades concretas."
    )

    selected_sector = st.selectbox("Filtrar por setor", SECTORS, key="uc_sector")
    ov = st.session_state.get("overall", 0)

    show_only_viable = st.checkbox(
        "Mostrar apenas casos viáveis para o nível atual de maturidade",
        value=False,
    )
    show_quick_wins_first = st.checkbox(
        "Priorizar quick wins (implementáveis em até 3 meses)",
        value=True,
    )

    cases = USE_CASES.get(selected_sector, [])

    # Filtra e ordena
    if show_only_viable and ov > 0:
        cases = [c for c in cases if c["min_maturity"] <= ov]

    if show_quick_wins_first:
        cases = sorted(
            cases,
            key=lambda c: (not c.get("quick_win", False), c["min_maturity"]),
        )

    if not cases:
        st.info("Nenhum caso de uso encontrado para os filtros selecionados.")
    else:
        for case in cases:
            viable = ov >= case["min_maturity"] if ov > 0 else True
            is_qw = case.get("quick_win", False)
            icon = "✅" if viable else "⚠️"
            qw_badge = " 🚀 Quick Win" if is_qw else ""

            with st.expander(
                f"{icon} {case['name']} — Impacto: {case['impact']}{qw_badge}"
            ):
                st.markdown(case["description"])

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Complexidade", case["complexity"])
                col2.metric("Impacto", case["impact"])
                col3.metric("Maturidade Mín.", f"{case['min_maturity']:.1f}")
                col4.metric(
                    "ROI estimado", case.get("roi_estimate", "N/A"),
                )

                st.markdown(
                    f"**Tecnologias:** {', '.join(case['technologies'])}",
                )

                if not viable:
                    st.warning(
                        f"A empresa precisa atingir maturidade "
                        f"**{case['min_maturity']:.1f}** "
                        f"para este caso de uso (atual: {ov:.1f})."
                    )


# ══════════════════════════════════════════════════════════════════════
# TAB 7: SOBRE
# ══════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.header("Sobre o Projeto")
    st.markdown("""
### Visão Geral

O **AI Industry Diagnostics** é uma plataforma de diagnóstico de maturidade em
Inteligência Artificial voltada ao setor produtivo. Oferece um framework estruturado
para avaliar onde a empresa está hoje, identificar oportunidades de maior impacto e
construir um roadmap realista de adoção.

### O Papel do Consultor de Diagnóstico em IA

O consultor atua como **ponte entre tecnologia e negócio**:
- **Visita empresas** e mapeia oportunidades reais de uso de IA
- **Aplica o framework** de diagnóstico de 30 perguntas em 6 dimensões
- **Elabora roadmaps** de adoção personalizados com fases, KPIs e riscos
- **Apresenta resultados** à diretoria com linguagem executiva

### Metodologia de Diagnóstico

| Etapa | Descrição | Duração |
|---|---|---|
| **1. Entrevista Inicial** | Conversa com liderança para entender contexto | 1-2h |
| **2. Avaliação Estruturada** | Aplicação do questionário com gestores | 2-4h |
| **3. Diagnóstico Analítico** | Análise com radar, benchmark e gaps | 1 dia |
| **4. Roadmap Personalizado** | Plano de 4 fases com KPIs e riscos | 1 dia |
| **5. Apresentação Executiva** | Entrega do relatório à diretoria | 1-2h |

### Setores Atendidos

Manufatura, Automotivo, Agronegócio, Logística, Varejo, Saúde, Financeiro e Energia.

### Autor

**Jardel Vieira Alves**
Consultor de Diagnóstico em IA
    """)


def main() -> None:
    """Entry point para execução via script."""
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", __file__, "--server.port", "8501"],
        check=True,
    )
