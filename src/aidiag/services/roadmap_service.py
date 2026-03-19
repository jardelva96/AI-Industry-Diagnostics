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
    """Gera roadmap em 4 fases baseado nos gaps identificados.

    Fases:
      1. Quick Wins (0-3 meses) — vitórias rápidas de alta visibilidade
      2. Fundação (3-9 meses) — infraestrutura, governança, equipe
      3. Escala (9-18 meses) — projetos core de IA com ROI medido
      4. Transformação (18-24 meses) — integração company-wide
    """
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
    quick_wins = _get_sector_use_cases(sector, overall)

    # ── Fase 1: Quick Wins (0-3 meses) ──────────────────────────────
    # Foco: ações de baixo custo e alta visibilidade que criam momentum
    phase1_actions = []

    # Ações baseadas na dimensão mais fraca (resultado imediato)
    weakest_key, weakest_label, weakest_score = dim_scores[0]
    if weakest_score < 2.0:
        phase1_actions.append(
            f"[{weakest_label}] Realizar diagnóstico detalhado e criar plano de ação "
            f"emergencial (score atual: {weakest_score:.1f} — abaixo do mínimo aceitável)"
        )
    else:
        phase1_actions.append(
            f"[{weakest_label}] Implementar melhorias rápidas para elevar de "
            f"{weakest_score:.1f} para {min(weakest_score + 0.5, 5.0):.1f}"
        )

    phase1_actions.append(
        "Mapear todas as iniciativas de IA existentes (formais e informais) e consolidar "
        "em inventário único — eliminar shadow AI e duplicação de esforço"
    )
    phase1_actions.append(
        "Realizar workshop de alinhamento com liderança (4h) para definir visão e "
        "prioridades de IA — sem sponsor executivo, projetos morrem na primeira barreira"
    )
    phase1_actions.append(
        "Publicar política de uso aceitável de IA e comunicar a toda a empresa — "
        "estabelece regras do jogo e reduz risco de uso inadequado"
    )

    if quick_wins:
        phase1_actions.append(
            f"Iniciar piloto de '{quick_wins[0]}' com equipe reduzida e escopo controlado "
            f"— primeiro resultado tangível para demonstrar valor ao C-level"
        )

    phase1_actions.append(
        "Definir KPIs de sucesso para cada iniciativa de IA (antes de começar) — "
        "sem baseline e métrica, é impossível provar ROI depois"
    )

    phases.append(RoadmapPhase(
        phase=1,
        title="Quick Wins",
        horizon="0 – 3 meses",
        actions=phase1_actions,
        expected_impact=(
            "Primeiros resultados visíveis que constroem confiança na liderança, "
            "base de governança estabelecida e equipe alinhada na direção estratégica"
        ),
        investment="Baixo",
        risks=[
            "Resistência cultural à mudança — mitigar com comunicação e quick wins visíveis",
            "Falta de sponsor executivo — garantir patrocínio de pelo menos um VP/diretor",
            "Expectativas irrealistas de resultados imediatos — gerenciar com comunicação clara",
        ],
        kpis=[
            "Inventário de iniciativas de IA concluído (sim/não)",
            "Política de uso de IA publicada e comunicada (sim/não)",
            "Pelo menos 1 piloto iniciado com KPIs definidos",
            "Workshop de alinhamento realizado com liderança (sim/não)",
            "NPS interno de satisfação com as primeiras iniciativas",
        ],
    ))

    # ── Fase 2: Fundação (3-9 meses) ────────────────────────────────
    # Foco: infraestrutura de dados, governança, formação de equipe
    phase2_actions = []

    # Foca nas 2 dimensões mais fracas para construir base sólida
    for _dim_key, label, score in dim_scores[:2]:
        if score < 2.0:
            phase2_actions.append(
                f"[{label}] Estabelecer fundamentos: contratar competências, "
                f"implantar ferramentas e definir processos básicos "
                f"(elevar de {score:.1f} para {min(score + 1.0, 5.0):.1f})"
            )
        elif score < 3.0:
            phase2_actions.append(
                f"[{label}] Consolidar e formalizar práticas existentes com "
                f"padrões, documentação e automação "
                f"(elevar de {score:.1f} para {min(score + 1.0, 5.0):.1f})"
            )
        else:
            phase2_actions.append(
                f"[{label}] Otimizar processos existentes e preparar para escala "
                f"(elevar de {score:.1f} para {min(score + 0.5, 5.0):.1f})"
            )

    phase2_actions.append(
        "Implementar data warehouse/data lake centralizado com governança de acesso — "
        "dados unificados são pré-requisito para qualquer projeto de IA com escala"
    )
    phase2_actions.append(
        "Contratar ou formar equipe dedicada de dados/IA (mínimo 2-3 pessoas: "
        "engenheiro de dados, cientista de dados, analista) — sem equipe dedicada, "
        "IA fica como 'projeto paralelo' e nunca ganha tração"
    )
    phase2_actions.append(
        "Definir framework de governança de IA com comitê multidisciplinar — "
        "jurídico, TI, negócio e compliance devem participar das decisões"
    )
    phase2_actions.append(
        "Implementar programa de data literacy para gestores e equipe operacional — "
        "decisões baseadas em dados só acontecem quando as pessoas entendem os dados"
    )

    if len(quick_wins) > 1:
        phase2_actions.append(
            f"Escalar e consolidar piloto: '{quick_wins[1]}' — aplicar lições "
            f"aprendidas do primeiro piloto para acelerar entrega"
        )

    phases.append(RoadmapPhase(
        phase=2,
        title="Fundação",
        horizon="3 – 9 meses",
        actions=phase2_actions,
        expected_impact=(
            "Infraestrutura de dados operacional, equipe formada e capacitada, "
            "governança estabelecida e primeiros pipelines de dados automatizados"
        ),
        investment="Médio",
        risks=[
            "Dificuldade em contratar talentos de dados/IA — considerar formação interna "
            "e parcerias com consultorias especializadas",
            "Resistência de áreas em compartilhar dados — mitigar com governança clara "
            "e demonstração de valor para cada área",
            "Escopo de infraestrutura crescer além do necessário — começar com MVP e "
            "expandir conforme demanda real",
            "Budget insuficiente para ferramentas e equipe — apresentar business case "
            "com ROI dos pilotos da Fase 1",
        ],
        kpis=[
            "Data warehouse/lake operacional com pelo menos 3 fontes integradas",
            "Equipe de dados/IA contratada e operando (headcount vs. plano)",
            "Pelo menos 80% dos gestores concluíram treinamento de data literacy",
            "Framework de governança documentado e aprovado pelo comitê",
            "Tempo médio de preparação de dados reduzido em 30%+ vs. baseline",
            "Pelo menos 2 projetos de IA com ROI mensurado e positivo",
        ],
    ))

    # ── Fase 3: Escala (9-18 meses) ─────────────────────────────────
    # Foco: projetos core de IA com ROI medido, MLOps, integração
    phase3_actions = []

    for _dim_key, label, score in dim_scores[2:4]:
        target = min(score + 1.0, 5.0)
        phase3_actions.append(
            f"[{label}] Avançar para nível intermediário/avançado "
            f"(de {score:.1f} para {target:.1f}) com práticas maduras e métricas de impacto"
        )

    phase3_actions.append(
        "Implementar pipeline de MLOps completo (versionamento, CI/CD, monitoramento, "
        "retraining) — sem MLOps, cada deploy é artesanal e cada modelo em produção é "
        "uma bomba-relógio"
    )
    phase3_actions.append(
        "Criar programa estruturado de capacitação em IA com trilhas por role "
        "(analista, engenheiro, líder de produto) e certificações — retenção de talentos "
        "exige crescimento profissional visível"
    )
    phase3_actions.append(
        "Integrar modelos de IA nos sistemas core (ERP, CRM, MES) via APIs — "
        "predições que não se conectam a ações automáticas são apenas exercícios acadêmicos"
    )
    phase3_actions.append(
        "Estabelecer processo formal de medição de ROI para cada projeto de IA com "
        "revisão trimestral — projetos sem retorno claro devem ser descontinuados "
        "para liberar recursos para os que geram valor"
    )

    if len(quick_wins) > 2:
        phase3_actions.append(
            f"Expandir portfólio de IA: iniciar projeto de '{quick_wins[2]}' — "
            f"diversificar aplicações demonstra maturidade e amplia impacto no negócio"
        )

    phases.append(RoadmapPhase(
        phase=3,
        title="Escala",
        horizon="9 – 18 meses",
        actions=phase3_actions,
        expected_impact=(
            "IA integrada nos processos-chave de negócio com impacto mensurável no P&L, "
            "plataforma de MLOps operacional e equipe autônoma para desenvolver e manter modelos"
        ),
        investment="Alto",
        risks=[
            "Complexidade de integração com sistemas legados — planejar APIs e middleware "
            "com antecedência, considerar modernização gradual",
            "Modelos em produção degradando sem monitoramento — implementar alertas de "
            "data drift e performance drift antes de escalar",
            "Dependência excessiva de fornecedores únicos — manter portabilidade e evitar "
            "vendor lock-in em decisões de plataforma",
            "Burnout da equipe de dados por excesso de demandas — priorizar projetos com "
            "framework claro e proteger tempo de inovação",
        ],
        kpis=[
            "Número de modelos em produção com monitoramento ativo",
            "ROI agregado dos projetos de IA (meta: positivo em pelo menos 70% dos projetos)",
            "Tempo médio de deploy de modelo (do experimento à produção) — meta: < 4 semanas",
            "Percentual de decisões de negócio críticas suportadas por modelos de IA",
            "Índice de retenção de talentos de dados/IA (meta: > 85% ao ano)",
            "Redução de custos operacionais atribuível a projetos de IA",
        ],
    ))

    # ── Fase 4: Transformação (18-24 meses) ──────────────────────────
    # Foco: IA company-wide, vantagem competitiva, liderança setorial
    phase4_actions = []

    for _dim_key, label, score in dim_scores[4:]:
        target = min(score + 1.5, 5.0)
        phase4_actions.append(
            f"[{label}] Atingir nível Avançado/Líder "
            f"(de {score:.1f} para {target:.1f}) — posicionar como referência no setor"
        )

    phase4_actions.append(
        "Criar Centro de Excelência em IA (CoE) com squads multidisciplinares atendendo "
        "todas as áreas de negócio — centralizar conhecimento e padrões, descentralizar "
        "execução"
    )
    phase4_actions.append(
        "Integrar IA no planejamento estratégico corporativo como pilar de transformação "
        "— IA deixa de ser 'projeto de TI' e se torna capacidade estratégica do negócio"
    )
    phase4_actions.append(
        "Estabelecer parcerias com universidades para pesquisa aplicada e programa de "
        "mestrado/doutorado corporativo — acesse a fronteira do conhecimento e forme a "
        "próxima geração de líderes em IA"
    )
    phase4_actions.append(
        "Implementar plataforma self-service de IA para que áreas de negócio criem e "
        "gerenciem modelos simples sem depender do time central — democratize IA e "
        "multiplique o impacto"
    )
    phase4_actions.append(
        "Publicar resultados e cases em conferências do setor — posicione a empresa como "
        "referência, atraia talentos de primeiro nível e fortaleça employer branding"
    )
    phase4_actions.append(
        "Investir em P&D de IA proprietária focada em vantagem competitiva — modelos e "
        "datasets únicos do seu domínio são mais valiosos que qualquer solução genérica "
        "de mercado"
    )

    phases.append(RoadmapPhase(
        phase=4,
        title="Transformação",
        horizon="18 – 24 meses",
        actions=phase4_actions,
        expected_impact=(
            "Organização AI-driven com vantagem competitiva sustentável, cultura de "
            "inovação orientada por dados em todas as áreas e posicionamento como "
            "referência setorial em IA"
        ),
        investment="Alto",
        risks=[
            "Perda de foco estratégico ao tentar transformar tudo ao mesmo tempo — "
            "priorizar áreas de maior impacto competitivo",
            "Risco regulatório com uso extensivo de IA — manter governança e compliance "
            "atualizados com regulações emergentes (EU AI Act, LGPD)",
            "Dificuldade em manter cultura de inovação em escala — investir em "
            "reconhecimento, autonomia e tolerância a falhas controladas",
            "Competidores copiando soluções de IA — proteger propriedade intelectual e "
            "focar em dados proprietários como diferencial",
        ],
        kpis=[
            "Percentual da receita influenciada por decisões de IA (meta: > 30%)",
            "Número de áreas de negócio com pelo menos 1 caso de uso de IA em produção",
            "Score de maturidade geral da empresa (meta: > 4.0/5.0)",
            "Publicações e participações em conferências do setor sobre IA",
            "Índice de satisfação dos colaboradores com ferramentas de IA (pesquisa interna)",
            "Time-to-market de novos produtos/serviços habilitados por IA",
            "Posição em rankings setoriais de inovação e transformação digital",
        ],
    ))

    return RoadmapOut(
        assessment_id=assessment.id,
        company_name=company_name,
        maturity_level=assessment.maturity_level,
        phases=phases,
    )
