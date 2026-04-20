"""Serviço de diagnóstico — transforma scores em relatório analítico."""

from __future__ import annotations

from aidiag.data.dimensions import DIMENSIONS, SCORE_FIELD_MAP
from aidiag.models import Assessment
from aidiag.schemas import DiagnosticReport, DimensionDetail, QuickWin

# ── Recomendações por dimensão e faixa de score ──────────────────────
# Cada recomendação é escrita como conselho direto de um consultor
# para um executivo: acionável, com contexto de negócio e resultado esperado.
_RECOMMENDATIONS: dict[str, dict[str, list[str]]] = {
    "data": {
        "low": [
            "Contrate um assessment de dados em 30 dias: mapeie todas as fontes de dados da empresa, "
            "identifique os 'donos' de cada fonte e documente formatos — isso elimina retrabalho e "
            "reduz em até 40% o tempo de preparação de dados em projetos futuros",
            "Implemente um data warehouse centralizado usando solução gerenciada (BigQuery, Redshift ou "
            "Snowflake) para unificar dados de ERP, CRM e produção — o custo inicial é baixo e o "
            "retorno em visibilidade operacional é imediato",
            "Estabeleça rotinas semanais de validação de qualidade de dados nos 5 campos mais críticos "
            "do negócio (ex: estoque, faturamento, pedidos) — dados confiáveis são pré-requisito para "
            "qualquer iniciativa de IA",
            "Designe um responsável por dados (mesmo que não seja um cargo novo) para ser o ponto focal "
            "de governança — sem ownership claro, dados se deterioram rapidamente",
            "Comece a catalogar os dados mais utilizados pela gestão em um dicionário de dados simples "
            "(planilha já resolve) — quando a empresa crescer, isso vira a base do catálogo corporativo",
        ],
        "mid": [
            "Adote um catálogo de dados corporativo (DataHub, Amundsen ou similar) com metadados "
            "padronizados e busca — reduza o tempo que analistas gastam procurando dados de horas para "
            "minutos",
            "Implemente pipelines de ETL/ELT automatizados com orquestração (Airflow, Prefect) e "
            "alertas de falha — elimine processos manuais de extração que hoje consomem tempo de "
            "profissionais qualificados",
            "Desenvolva política formal de LGPD com DPO designado e processos de anonimização — "
            "proteja a empresa de multas que podem chegar a 2% do faturamento e construa confiança "
            "com clientes",
            "Implemente testes automatizados de qualidade de dados (Great Expectations, dbt tests) em "
            "todos os pipelines críticos — detecte problemas antes que afetem decisões de negócio",
            "Crie um SLA de dados para cada fonte crítica (latência máxima, taxa de completude, "
            "frequência de atualização) — trate dados como produto, não como subproduto de sistemas",
        ],
        "high": [
            "Evolua para arquitetura data mesh com ownership distribuído por domínio de negócio — "
            "cada área se torna responsável pela qualidade e disponibilidade dos seus dados, "
            "acelerando a entrega de produtos de dados em 3-5x",
            "Implemente validação de qualidade de dados automatizada com ML (detecção de anomalias, "
            "drift monitoring) — identifique degradação de dados antes que impacte modelos em produção",
            "Crie um data marketplace interno onde áreas possam descobrir, solicitar e compartilhar "
            "datasets — isso transforma dados de custo operacional em ativo estratégico",
            "Implemente data contracts entre produtores e consumidores de dados — formalize expectativas "
            "e evite quebras em cascata quando schemas mudam",
            "Invista em real-time data streaming (Kafka, Kinesis) para casos de uso que exigem "
            "decisões em segundos — manutenção preditiva, precificação dinâmica e detecção de fraude "
            "dependem de dados em tempo real",
        ],
    },
    "algorithms": {
        "low": [
            "Comece com 1-2 casos de uso simples de ML (classificação ou regressão) que resolvam "
            "um problema real de negócio — previsão de demanda, classificação de tickets ou detecção "
            "de anomalias são bons pontos de partida com ROI rápido",
            "Capacite a equipe técnica existente em ferramentas práticas (scikit-learn, pandas, "
            "SQL avançado) através de treinamentos focados de 40h — é mais rápido e barato que "
            "contratar especialistas para projetos iniciais",
            "Crie um ambiente de experimentação seguro (notebooks na nuvem, sandbox com dados "
            "anonimizados) — a equipe precisa de um espaço para testar hipóteses sem risco para "
            "sistemas de produção",
            "Identifique os 3 relatórios mais demorados de produzir e avalie automatização com "
            "modelos simples — o ganho de produtividade justifica o investimento inicial em IA",
            "Contrate ou designe um 'campeão de IA' que dedique pelo menos 50% do tempo para "
            "liderar os primeiros experimentos — iniciativas sem liderança técnica dedicada fracassam",
        ],
        "mid": [
            "Implemente MLOps básico com versionamento de modelos, dados e código (MLflow, DVC) — "
            "sem rastreabilidade, é impossível reproduzir resultados ou fazer rollback quando um "
            "modelo falha em produção",
            "Adote práticas de explicabilidade (SHAP, LIME) em todos os modelos que afetam decisões "
            "sobre pessoas ou dinheiro — isso não é só compliance, é gestão de risco",
            "Inicie pilotos controlados com IA generativa em processos internos (geração de "
            "relatórios, resumo de documentos, assistente de código) — meça produtividade antes e "
            "depois para quantificar o ganho",
            "Estabeleça critérios claros de 'go/no-go' para colocar modelos em produção (acurácia "
            "mínima, fairness, latência) — sem guardrails, modelos ruins chegam ao cliente",
            "Crie um repositório centralizado de experimentos com resultados documentados — evite "
            "que equipes reinventem a roda e acumule conhecimento institucional",
        ],
        "high": [
            "Implemente feature store (Feast, Tecton) e model registry para reutilização de "
            "features e modelos entre equipes — isso acelera o time-to-market de novos modelos "
            "em 50-70%",
            "Crie uma plataforma de AutoML interna para que analistas de negócio construam modelos "
            "simples sem depender do time de data science — democratize ML e libere os especialistas "
            "para problemas complexos",
            "Integre LLMs fine-tuned com RAG em produção para casos de uso de alto valor (atendimento "
            "ao cliente, análise de contratos, busca semântica em documentação técnica) — empresas "
            "líderes já reportam redução de 30-60% em tempo de processos intensivos em conhecimento",
            "Implemente A/B testing automatizado para modelos em produção com rollback automático — "
            "valide melhorias com dados reais antes de expor 100% dos usuários",
            "Invista em pesquisa aplicada com universidades para desenvolver modelos proprietários "
            "no seu domínio — isso cria barreiras de entrada e vantagem competitiva difícil de copiar",
        ],
    },
    "governance": {
        "low": [
            "Crie uma política de uso aceitável de IA em 2 páginas, aprovada pela diretoria — "
            "não precisa ser perfeita, precisa existir e ser comunicada a todos os colaboradores",
            "Designe um responsável por ética em IA (pode ser acumulado com outra função) que "
            "revise semanalmente como ferramentas de IA estão sendo usadas — sem supervisão, "
            "riscos se acumulam silenciosamente",
            "Faça um inventário de todas as ferramentas de IA já em uso na empresa (inclusive "
            "ChatGPT, Copilot e outras usadas informalmente) — você provavelmente vai se surpreender "
            "com o shadow AI que já existe",
            "Mapeie os 5 maiores riscos algorítmicos nos processos existentes (viés em contratação, "
            "discriminação em crédito, decisões automatizadas sem revisão) — priorize mitigação "
            "pelo impacto potencial",
            "Estabeleça uma regra simples: nenhum modelo que afete clientes ou colaboradores vai "
            "para produção sem revisão humana — isso evita 90% dos problemas sérios de governança",
        ],
        "mid": [
            "Estabeleça um comitê de ética em IA multidisciplinar (TI, jurídico, RH, negócio) com "
            "reuniões mensais e pauta estruturada — decisões de governança precisam de perspectivas "
            "diversas",
            "Implemente testes de fairness (equidade) em modelos que afetam decisões sobre pessoas — "
            "use métricas como demographic parity e equalized odds e defina thresholds aceitáveis",
            "Crie model cards para todos os modelos em produção documentando: propósito, dados de "
            "treino, limitações conhecidas, métricas de performance e responsável — é o 'manual' "
            "de cada modelo",
            "Implemente logging completo de decisões automatizadas com capacidade de explicação "
            "individual — quando um regulador ou cliente perguntar 'por que esta decisão?', você "
            "precisa ter a resposta",
            "Realize treinamentos trimestrais de ética em IA para equipes técnicas e de negócio — "
            "governança só funciona quando está na cultura, não apenas no papel",
        ],
        "high": [
            "Alinhe seu framework de governança ao EU AI Act e regulações setoriais (BACEN, ANVISA, "
            "ANATEL) — mesmo que não sejam obrigatórias hoje, a conformidade antecipada evita custos "
            "de adaptação futuros e abre mercados internacionais",
            "Contrate auditoria externa anual de modelos críticos — uma validação independente "
            "fortalece a confiança de stakeholders e identifica blind spots que equipes internas "
            "não enxergam",
            "Crie um programa de transparência algorítmica com opt-out para clientes — permita "
            "que clientes saibam quando IA está sendo usada e ofereça alternativa humana quando "
            "aplicável",
            "Implemente monitoramento contínuo de viés em produção com alertas automáticos — "
            "modelos que eram justos no treino podem se tornar discriminatórios com mudanças nos "
            "dados",
            "Publique um relatório anual de IA responsável com métricas de fairness, incidentes e "
            "ações corretivas — transparência proativa constrói reputação e antecipa pressão "
            "regulatória",
        ],
    },
    "talent": {
        "low": [
            "Contrate pelo menos um cientista de dados ou analista de IA sênior nos próximos 90 dias "
            "— sem competência técnica interna, a empresa fica refém de consultorias e não acumula "
            "conhecimento",
            "Lance um programa de data literacy para gestores e líderes de área (workshops de 8h) — "
            "líderes que não entendem dados tomam decisões piores e bloqueiam iniciativas de IA",
            "Identifique 2-3 profissionais internos com aptidão analítica e patrocine formação "
            "em dados/IA — profissionais que conhecem o negócio e aprendem IA são mais "
            "valiosos que cientistas de dados sem contexto do setor",
            "Crie uma comunidade interna de dados (canal no Slack/Teams, encontros mensais) para "
            "compartilhar aprendizados e boas práticas — cultura de dados começa com comunidade",
            "Defina um budget anual de capacitação em dados/IA por colaborador (mesmo que modesto) — "
            "sinaliza para a organização que isso é prioridade estratégica",
        ],
        "mid": [
            "Forme uma equipe dedicada de dados/IA com 3-5 pessoas (cientista de dados, engenheiro "
            "de dados, analista de IA) com reporte direto à liderança — times embutidos em TI sem "
            "autonomia perdem velocidade e relevância",
            "Crie trilhas de aprendizado formais por role (analista, engenheiro, líder de produto de "
            "dados) com certificações reconhecidas e progressão de carreira clara — retenção de "
            "talentos em IA exige plano de crescimento visível",
            "Implemente hackathons internos trimestrais focados em problemas reais de negócio — "
            "além de gerar ideias, isso identifica talentos escondidos e energiza a equipe",
            "Reserve 10-20% do tempo da equipe técnica para experimentação e aprendizado (similar "
            "ao '20% time' do Google) — inovação não acontece quando 100% do tempo é consumido "
            "por demandas operacionais",
            "Contrate um líder de dados/IA (Head of Data, CDO) que participe do comitê executivo — "
            "dados e IA precisam de representação na mesa de decisão estratégica",
        ],
        "high": [
            "Crie um Centro de Excelência em IA (CoE) que atenda todas as áreas de negócio com "
            "padrões, ferramentas e mentoria — centralize conhecimento sem centralizar execução",
            "Estabeleça parcerias formais com universidades para programas de mestrado corporativo "
            "e projetos de pesquisa aplicada — acesse talentos de ponta antes do mercado",
            "Desenvolva employer branding focado em dados/IA com presença em conferências, "
            "publicações técnicas e open source — as melhores pessoas querem trabalhar onde há "
            "desafios interessantes e visibilidade",
            "Implemente programa de rotação entre áreas para profissionais de dados — um cientista "
            "de dados que conhece operações, vendas e finanças gera 3x mais valor",
            "Crie programa de mentoria reversa onde profissionais juniores de IA ensinam executivos "
            "seniores — fecha o gap geracional de conhecimento e gera patrocínio orgânico para "
            "iniciativas de IA",
        ],
    },
    "process": {
        "low": [
            "Mapeie os 10 processos mais manuais e repetitivos da empresa e classifique por volume "
            "e custo — os melhores candidatos a automação são aqueles com alto volume, regras claras "
            "e baixa variabilidade",
            "Implemente RPA (Robotic Process Automation) nos 2-3 processos mais óbvios (entrada de "
            "dados, reconciliação, geração de relatórios) — o ROI típico é de 3-6 meses e libera "
            "pessoas para trabalho de maior valor",
            "Defina KPIs de negócio claros para cada projeto de IA antes de começar (redução de "
            "custo, aumento de receita, tempo economizado) — projetos sem métrica de sucesso viram "
            "'projetos de ciência' que nunca chegam a produção",
            "Documente os processos-chave de negócio em formato que permita identificar pontos de "
            "decisão automatizáveis — sem essa visibilidade, a IA é aplicada nos lugares errados",
            "Crie um canal formal para que áreas de negócio submetam demandas de automação/IA — "
            "sem intake estruturado, projetos surgem de forma caótica e desalinhada da estratégia",
        ],
        "mid": [
            "Crie APIs de integração entre modelos de IA e sistemas core (ERP, CRM, MES) para que "
            "predições se tornem ações automáticas — um modelo que ninguém consulta não gera valor",
            "Implemente CI/CD para modelos de ML com testes automatizados (unit tests, integration "
            "tests, performance tests) — trate modelos com o mesmo rigor de software de produção",
            "Meça o ROI real de cada projeto de IA trimestralmente com baseline definido antes do "
            "projeto — dados concretos de retorno garantem continuidade do investimento",
            "Crie um processo de priorização de projetos de IA baseado em impacto x viabilidade "
            "com revisão trimestral — recursos são limitados, aloque nos projetos com maior "
            "potencial de retorno",
            "Implemente monitoramento de modelos em produção (data drift, performance drift, "
            "latência) com alertas — modelos degradam silenciosamente e decisões ruins se acumulam "
            "sem que ninguém perceba",
        ],
        "high": [
            "Evolua para arquitetura de microsserviços de IA com event-driven architecture — "
            "isso permite escalar modelos independentemente e reagir a eventos de negócio em "
            "tempo real",
            "Implemente plataforma de MLOps completa (Kubeflow, SageMaker, Vertex AI) com "
            "governança end-to-end — do experimento ao deploy, passando por validação, "
            "monitoramento e retraining automático",
            "Adote abordagem product-led AI com squads multidisciplinares (PM + data scientist + "
            "engenheiro + domain expert) — trate cada solução de IA como um produto com ciclo de "
            "vida, backlog e stakeholders",
            "Implemente feedback loops automatizados onde resultados de modelos em produção alimentam "
            "retraining contínuo — modelos que aprendem com o ambiente se mantêm relevantes",
            "Crie um catálogo de serviços de IA reutilizáveis (OCR, NLP, previsão de séries "
            "temporais) que áreas de negócio possam compor em soluções — reduza duplicação de "
            "esforço e acelere entrega",
        ],
    },
    "strategy": {
        "low": [
            "Agende uma sessão de 4h com o C-level para apresentar o potencial de IA no setor — "
            "use 3-5 cases de concorrentes ou empresas similares para tangibilizar o impacto e "
            "criar urgência",
            "Visite 2-3 empresas referência em IA no seu setor (presencialmente ou virtualmente) — "
            "ver funciona melhor que ouvir, e executivos voltam dessas visitas com senso de urgência",
            "Defina um orçamento inicial de experimentação com IA (1-3% do budget de TI) protegido "
            "de cortes — sem budget dedicado, IA compete com manutenção de sistemas e sempre perde",
            "Inclua 'potencial de IA' como critério na avaliação de novos projetos e investimentos — "
            "isso força a organização a pensar em IA sistematicamente, não apenas quando alguém "
            "sugere",
            "Crie um comitê de inovação em IA com representantes de cada área de negócio — "
            "iniciativas de IA que nascem apenas em TI raramente resolvem os problemas certos",
        ],
        "mid": [
            "Crie um roadmap de IA de 18-24 meses integrado ao planejamento estratégico anual — "
            "projetos de IA precisam de horizonte mais longo que projetos de TI tradicionais",
            "Designe um sponsor executivo (VP ou C-level) para cada iniciativa de IA relevante — "
            "projetos sem patrocínio executivo morrem na primeira barreira organizacional",
            "Participe ativamente de ecossistemas de inovação (hubs, aceleradoras, associações "
            "setoriais) focados em IA — mantenha o radar ligado para tendências e parcerias",
            "Defina metas de IA no balanced scorecard ou OKRs da empresa — o que não é medido não "
            "é gerenciado, e IA precisa de metas tão claras quanto vendas ou operações",
            "Comunique regularmente (town halls, newsletters) os resultados e aprendizados de "
            "projetos de IA para toda a empresa — transparência constrói apoio e reduz resistência",
        ],
        "high": [
            "Posicione IA como pilar central da estratégia corporativa de 5 anos — articule "
            "publicamente como IA transforma o modelo de negócio, não apenas otimiza operações",
            "Crie um venture arm ou programa de co-criação com startups de IA — acesse inovação "
            "que não é possível desenvolver internamente e construa opcionalidade estratégica",
            "Publique resultados e cases em conferências do setor e papers aplicados — posicione "
            "a empresa como referência e atraia talentos e parceiros de primeiro nível",
            "Invista em P&D de IA com foco em vantagem competitiva proprietária — modelos e "
            "datasets únicos do seu domínio são mais valiosos que qualquer ferramenta genérica",
            "Crie um advisory board de IA com acadêmicos e executivos de referência — perspectivas "
            "externas de alto nível ajudam a antecipar tendências e evitar armadilhas estratégicas",
        ],
    },
}

# ── Quick wins por dimensão ──────────────────────────────────────────
# Ações de baixo esforço e alto impacto para cada dimensão
_QUICK_WINS: dict[str, list[dict[str, str]]] = {
    "data": [
        {
            "action": "Criar dicionário de dados dos 20 campos mais usados pela gestão",
            "effort": "Baixo",
            "timeline": "2 semanas",
            "impact": "Elimina ambiguidade em reuniões e relatórios, reduz retrabalho em análises",
        },
        {
            "action": "Implementar validação automática dos 5 campos mais críticos do ERP",
            "effort": "Baixo",
            "timeline": "3 semanas",
            "impact": "Reduz erros de dados que causam reprocessamento e decisões incorretas",
        },
    ],
    "algorithms": [
        {
            "action": "Implementar modelo de previsão de demanda com dados históricos existentes",
            "effort": "Médio",
            "timeline": "4-6 semanas",
            "impact": "Redução de 10-20% em excesso de estoque ou ruptura, ROI mensurável",
        },
        {
            "action": "Adotar ferramenta de IA generativa para resumo de documentos internos",
            "effort": "Baixo",
            "timeline": "1-2 semanas",
            "impact": "Economia de 2-4h/semana por profissional em tarefas de leitura e síntese",
        },
    ],
    "governance": [
        {
            "action": "Publicar política de uso aceitável de IA em 2 páginas para toda a empresa",
            "effort": "Baixo",
            "timeline": "2 semanas",
            "impact": "Reduz risco de uso inadequado e estabelece expectativas claras",
        },
        {
            "action": "Fazer inventário de todas as ferramentas de IA já em uso (inclusive shadow AI)",
            "effort": "Baixo",
            "timeline": "1 semana",
            "impact": "Visibilidade de riscos desconhecidos e oportunidades de padronização",
        },
    ],
    "talent": [
        {
            "action": "Realizar workshop de data literacy de 8h para líderes de área",
            "effort": "Baixo",
            "timeline": "3 semanas",
            "impact": "Líderes passam a formular perguntas melhores e apoiar iniciativas de dados",
        },
        {
            "action": "Criar canal interno de dados/IA para compartilhamento de boas práticas",
            "effort": "Baixo",
            "timeline": "1 semana",
            "impact": "Começa a construir cultura de dados de forma orgânica e de baixo custo",
        },
    ],
    "process": [
        {
            "action": "Automatizar os 3 relatórios mais demorados com scripts ou RPA",
            "effort": "Médio",
            "timeline": "4 semanas",
            "impact": "Libera 10-20h/mês de profissionais qualificados para trabalho analítico",
        },
        {
            "action": "Definir KPIs de sucesso para os projetos de IA existentes ou planejados",
            "effort": "Baixo",
            "timeline": "1 semana",
            "impact": "Projetos passam a ter critério objetivo de sucesso e priorização",
        },
    ],
    "strategy": [
        {
            "action": "Agendar sessão de benchmarking com 2-3 empresas referência em IA no setor",
            "effort": "Baixo",
            "timeline": "4 semanas",
            "impact": "Cria senso de urgência na liderança e gera ideias concretas de aplicação",
        },
        {
            "action": "Incluir agenda de IA na próxima reunião de planejamento estratégico",
            "effort": "Baixo",
            "timeline": "Próximo ciclo de planejamento",
            "impact": "Coloca IA no radar estratégico da alta liderança de forma estruturada",
        },
    ],
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


def generate_executive_summary(
    company_name: str,
    overall_score: float,
    maturity_level: str,
    dimensions: list[DimensionDetail],
    top_strengths: list[str],
    critical_gaps: list[str],
) -> str:
    """Produz um resumo executivo textual adequado para apresentação ao conselho."""
    # Determina a situação geral
    if overall_score < 2.0:
        situacao = (
            "encontra-se em estágio inicial de maturidade em IA. A empresa ainda não possui "
            "fundamentos estruturados para adoção de Inteligência Artificial, mas isso representa "
            "uma oportunidade significativa de transformação"
        )
        urgencia = (
            "Recomendamos ação imediata para estabelecer as bases, pois concorrentes já estão "
            "avançando nessa direção e a janela de oportunidade se estreita a cada trimestre"
        )
    elif overall_score < 3.0:
        situacao = (
            "está dando os primeiros passos em IA com iniciativas pontuais. Existem fundamentos "
            "que podem ser acelerados, mas ainda falta estrutura para escalar e gerar impacto "
            "consistente no negócio"
        )
        urgencia = (
            "O momento é favorável para consolidar as bases e iniciar projetos com ROI mensurável. "
            "Com investimento focado nos gaps identificados, é possível avançar significativamente "
            "em 12-18 meses"
        )
    elif overall_score < 4.0:
        situacao = (
            "apresenta nível intermediário de maturidade em IA com práticas estabelecidas em "
            "algumas dimensões. A empresa já colhe resultados de iniciativas de IA, mas precisa "
            "escalar e integrar de forma mais profunda nos processos de negócio"
        )
        urgencia = (
            "A empresa está bem posicionada para dar o salto de 'projetos de IA' para 'empresa "
            "orientada por IA'. O foco deve ser em escala, integração e criação de vantagem "
            "competitiva sustentável"
        )
    else:
        situacao = (
            "demonstra maturidade avançada em IA, com práticas sofisticadas e resultados "
            "comprovados. A empresa é referência no setor e deve focar em manter a liderança "
            "e explorar fronteiras de inovação"
        )
        urgencia = (
            "A prioridade é manter a vantagem competitiva através de inovação contínua, "
            "desenvolvimento de propriedade intelectual em IA e atração dos melhores talentos "
            "do mercado"
        )

    # Monta detalhamento por dimensão
    dims_baixas = [d for d in dimensions if d.score < 2.5]
    dims_altas = [d for d in dimensions if d.score >= 3.5]

    destaques_positivos = ""
    if dims_altas:
        labels_altas = ", ".join(d.label for d in dims_altas)
        destaques_positivos = (
            f"\n\nPontos fortes identificados: {labels_altas}. Essas dimensões demonstram "
            f"maturidade acima da média e podem servir como base para alavancar as demais áreas."
        )

    alertas = ""
    if dims_baixas:
        labels_baixas = ", ".join(d.label for d in dims_baixas)
        alertas = (
            f"\n\nÁreas que requerem atenção prioritária: {labels_baixas}. Sem evolução nessas "
            f"dimensões, o potencial das áreas mais maduras fica limitado — a maturidade em IA é "
            f"sistêmica e o elo mais fraco determina o teto de resultados."
        )

    summary = (
        f"RESUMO EXECUTIVO — Diagnóstico de Maturidade em IA\n"
        f"Empresa: {company_name}\n"
        f"Score Geral: {overall_score:.2f}/5.00 | Nível: {maturity_level}\n"
        f"\n"
        f"A {company_name} {situacao}. Com score geral de {overall_score:.2f} em uma escala "
        f"de 5.0, a empresa está classificada no nível '{maturity_level}'."
        f"{destaques_positivos}"
        f"{alertas}\n"
        f"\n"
        f"Pontos fortes: {', '.join(top_strengths)}.\n"
        f"Gaps críticos: {', '.join(critical_gaps)}.\n"
        f"\n"
        f"{urgencia}\n"
        f"\n"
        f"Este diagnóstico deve ser revisado a cada 6 meses para acompanhar a evolução e "
        f"ajustar prioridades conforme o mercado e a organização evoluem."
    )

    return summary


def identify_quick_wins(
    dimensions: list[DimensionDetail],
) -> list[QuickWin]:
    """Retorna as 3-5 melhorias mais rápidas de implementar com maior impacto."""
    # Prioriza dimensões com maior gap (mais espaço para melhoria)
    sorted_dims = sorted(dimensions, key=lambda d: d.score)

    quick_wins: list[QuickWin] = []

    for dim in sorted_dims:
        dim_wins = _QUICK_WINS.get(dim.dimension, [])
        for win in dim_wins:
            if len(quick_wins) >= 5:
                break
            quick_wins.append(QuickWin(
                dimension=dim.label,
                action=win["action"],
                effort=win["effort"],
                expected_timeline=win["timeline"],
                business_impact=win["impact"],
            ))
        if len(quick_wins) >= 5:
            break

    # Se ainda temos espaço, pega das dimensões restantes
    if len(quick_wins) < 3:
        for dim in sorted_dims:
            dim_wins = _QUICK_WINS.get(dim.dimension, [])
            for win in dim_wins:
                already = any(q.action == win["action"] for q in quick_wins)
                if not already and len(quick_wins) < 5:
                    quick_wins.append(QuickWin(
                        dimension=dim.label,
                        action=win["action"],
                        effort=win["effort"],
                        expected_timeline=win["timeline"],
                        business_impact=win["impact"],
                    ))

    return quick_wins[:5]


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
    overall_score = round(assessment.overall_score, 2)
    maturity_level = assessment.maturity_level

    # Gera resumo executivo
    executive_summary = generate_executive_summary(
        company_name=company_name,
        overall_score=overall_score,
        maturity_level=maturity_level,
        dimensions=dimensions,
        top_strengths=top_strengths,
        critical_gaps=critical_gaps,
    )

    # Identifica quick wins
    quick_wins = identify_quick_wins(dimensions)

    return DiagnosticReport(
        assessment_id=assessment.id,
        company_name=company_name,
        overall_score=overall_score,
        maturity_level=maturity_level,
        dimensions=dimensions,
        top_strengths=top_strengths,
        critical_gaps=critical_gaps,
        executive_summary=executive_summary,
        quick_wins=quick_wins,
    )
