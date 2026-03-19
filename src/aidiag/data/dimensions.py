"""Dimensões de maturidade em IA e questionário de avaliação.

Cada dimensão contém 5 perguntas objetivas, pontuadas de 1 (Inicial) a 5 (Líder).
O framework é baseado em modelos de maturidade reconhecidos (Gartner, MIT CISR,
AI Maturity Model do OECD) adaptados para o contexto industrial brasileiro.
"""

from __future__ import annotations

MATURITY_LEVELS = {
    1: "Inicial",
    2: "Básico",
    3: "Intermediário",
    4: "Avançado",
    5: "Líder",
}

DIMENSIONS: dict[str, dict] = {
    "data": {
        "label": "Dados & Infraestrutura",
        "icon": "database",
        "description": (
            "Avalia a qualidade, disponibilidade e governança dos dados, "
            "além da infraestrutura computacional disponível."
        ),
        "questions": [
            {
                "id": "D1",
                "text": "Como estão organizados os dados da empresa?",
                "options": {
                    1: "Planilhas avulsas sem padronização",
                    2: "Bancos de dados departamentais isolados",
                    3: "Data warehouse centralizado com ETL básico",
                    4: "Data lake com pipelines automatizados e catálogo",
                    5: "Data mesh / lakehouse com governança distribuída",
                },
            },
            {
                "id": "D2",
                "text": "Qual o nível de qualidade dos dados?",
                "options": {
                    1: "Sem processos de validação — dados frequentemente incorretos",
                    2: "Validações manuais esporádicas",
                    3: "Rotinas de data quality com alertas básicos",
                    4: "Monitoramento contínuo com métricas de qualidade definidas",
                    5: "Data quality automatizado com ML e auto-remediação",
                },
            },
            {
                "id": "D3",
                "text": "Qual a infraestrutura computacional disponível?",
                "options": {
                    1: "Apenas desktops locais",
                    2: "Servidor on-premise básico",
                    3: "Cloud parcial (IaaS/PaaS) para alguns projetos",
                    4: "Cloud nativa com GPU sob demanda e CI/CD",
                    5: "Multi-cloud com Kubernetes, MLOps e auto-scaling",
                },
            },
            {
                "id": "D4",
                "text": "Como são integrados dados de fontes externas?",
                "options": {
                    1: "Não há integração com dados externos",
                    2: "Importação manual de arquivos de parceiros",
                    3: "APIs pontuais para algumas fontes",
                    4: "Integrações automatizadas com múltiplas fontes (IoT, ERP, CRM)",
                    5: "Plataforma de dados abertos com streaming em tempo real",
                },
            },
            {
                "id": "D5",
                "text": "Existe política de privacidade e proteção de dados (LGPD)?",
                "options": {
                    1: "Sem política definida",
                    2: "Política básica em fase de elaboração",
                    3: "LGPD implementada com DPO designado",
                    4: "Programa completo de privacy by design com auditorias",
                    5: "Certificações de privacidade e compliance automatizado",
                },
            },
        ],
    },
    "algorithms": {
        "label": "Algoritmos & Modelos",
        "icon": "cpu",
        "description": (
            "Avalia o uso atual de técnicas de machine learning, "
            "deep learning e IA generativa nos processos da empresa."
        ),
        "questions": [
            {
                "id": "A1",
                "text": "Qual o nível de adoção de ML/IA na empresa?",
                "options": {
                    1: "Nenhum uso de ML/IA",
                    2: "Experimentos isolados em sandbox",
                    3: "1-3 modelos em produção em áreas específicas",
                    4: "Múltiplos modelos em produção com monitoramento",
                    5: "IA integrada nos processos core com retraining automático",
                },
            },
            {
                "id": "A2",
                "text": "Como são desenvolvidos os modelos?",
                "options": {
                    1: "Sem desenvolvimento de modelos",
                    2: "Scripts ad-hoc em notebooks",
                    3: "Pipelines estruturados com versionamento de código",
                    4: "MLOps com versionamento de dados, modelos e experimentos",
                    5: "Plataforma de ML completa com AutoML e feature store",
                },
            },
            {
                "id": "A3",
                "text": "Qual o nível de validação dos modelos?",
                "options": {
                    1: "Sem validação formal",
                    2: "Split treino/teste básico",
                    3: "Cross-validation com métricas padronizadas",
                    4: "A/B testing em produção com monitoramento de drift",
                    5: "Champion/challenger automatizado com rollback",
                },
            },
            {
                "id": "A4",
                "text": "A empresa utiliza IA generativa?",
                "options": {
                    1: "Não utiliza e não tem planos",
                    2: "Uso informal de ferramentas como ChatGPT",
                    3: "Piloto estruturado com caso de uso definido",
                    4: "Integração de LLMs em produtos/processos internos",
                    5: "Modelos fine-tuned ou RAG em produção com governança",
                },
            },
            {
                "id": "A5",
                "text": "Como é tratada a explicabilidade dos modelos?",
                "options": {
                    1: "Modelos são caixas-pretas sem explicação",
                    2: "Documentação básica das features usadas",
                    3: "SHAP/LIME para modelos críticos",
                    4: "Dashboard de explicabilidade para stakeholders",
                    5: "Explicabilidade como requisito obrigatório com auditoria",
                },
            },
        ],
    },
    "governance": {
        "label": "Governança & Ética",
        "icon": "shield-check",
        "description": (
            "Avalia políticas de uso responsável de IA, "
            "gestão de riscos algorítmicos e conformidade regulatória."
        ),
        "questions": [
            {
                "id": "G1",
                "text": "Existe um framework de governança de IA?",
                "options": {
                    1: "Não existe governança de IA",
                    2: "Diretrizes informais de uso",
                    3: "Política formal de IA aprovada pela liderança",
                    4: "Comitê de ética em IA com revisão periódica",
                    5: "Framework completo com risk assessment e auditoria externa",
                },
            },
            {
                "id": "G2",
                "text": "Como são tratados vieses algorítmicos?",
                "options": {
                    1: "Sem consciência sobre vieses",
                    2: "Reconhecimento do problema sem ação formal",
                    3: "Testes de fairness em modelos críticos",
                    4: "Pipeline de detecção e mitigação de viés",
                    5: "Monitoramento contínuo com métricas de equidade",
                },
            },
            {
                "id": "G3",
                "text": "Qual o nível de documentação dos modelos?",
                "options": {
                    1: "Sem documentação",
                    2: "README básico por projeto",
                    3: "Model cards com métricas e limitações",
                    4: "Registro centralizado com lineage completo",
                    5: "Documentação automatizada com compliance check",
                },
            },
            {
                "id": "G4",
                "text": "Como é gerenciado o risco de IA?",
                "options": {
                    1: "Sem gestão de risco específica para IA",
                    2: "IA incluída no risco geral de TI",
                    3: "Classificação de risco por caso de uso",
                    4: "Framework de risco dedicado com impacto e probabilidade",
                    5: "Gestão de risco alinhada ao EU AI Act / regulações",
                },
            },
            {
                "id": "G5",
                "text": "Existe transparência sobre o uso de IA com clientes?",
                "options": {
                    1: "Clientes não sabem que IA é utilizada",
                    2: "Menção genérica em termos de uso",
                    3: "Comunicação proativa sobre uso de IA em serviços",
                    4: "Explicações acessíveis sobre decisões automatizadas",
                    5: "Direito a explicação implementado com opt-out",
                },
            },
        ],
    },
    "talent": {
        "label": "Talentos & Cultura",
        "icon": "people",
        "description": (
            "Avalia a capacidade da equipe em ciência de dados e IA, "
            "programas de treinamento e cultura de inovação."
        ),
        "questions": [
            {
                "id": "T1",
                "text": "Qual a composição do time de dados/IA?",
                "options": {
                    1: "Sem profissionais dedicados a dados/IA",
                    2: "1-2 analistas que fazem IA como tarefa secundária",
                    3: "Equipe pequena dedicada (3-5 pessoas)",
                    4: "Centro de excelência com especialistas diversos",
                    5: "Organização data-driven com cientistas em cada unidade",
                },
            },
            {
                "id": "T2",
                "text": "Como é feita a capacitação em IA?",
                "options": {
                    1: "Sem programa de capacitação",
                    2: "Cursos online individuais sem direcionamento",
                    3: "Programa de treinamento estruturado anual",
                    4: "Trilhas de aprendizado por role com certificações",
                    5: "Parceria com universidades e programa de mestrado",
                },
            },
            {
                "id": "T3",
                "text": "Qual a fluência em dados da liderança?",
                "options": {
                    1: "Liderança sem conhecimento de dados/IA",
                    2: "Consciência superficial sobre o tema",
                    3: "Liderança usa dashboards e KPIs data-driven",
                    4: "C-level com formação em analytics e IA",
                    5: "Chief Data/AI Officer com assento no board",
                },
            },
            {
                "id": "T4",
                "text": "Como é a cultura de experimentação?",
                "options": {
                    1: "Cultura avessa a risco — sem espaço para experimentos",
                    2: "Iniciativas isoladas toleradas mas não incentivadas",
                    3: "Hackathons e tempo dedicado para inovação",
                    4: "Processo formal de experimentação com budget",
                    5: "Fail-fast culture com labs de inovação integrados",
                },
            },
            {
                "id": "T5",
                "text": "A empresa consegue reter talentos em IA?",
                "options": {
                    1: "Alta rotatividade — dificuldade em contratar",
                    2: "Consegue contratar mas perde para big techs",
                    3: "Retenção razoável com benefícios competitivos",
                    4: "Employer branding forte na comunidade de dados",
                    5: "Referência no mercado — atrai talentos top",
                },
            },
        ],
    },
    "process": {
        "label": "Processos & Integração",
        "icon": "gear",
        "description": (
            "Avalia o nível de automação dos processos, integração "
            "de IA no fluxo operacional e maturidade de MLOps."
        ),
        "questions": [
            {
                "id": "P1",
                "text": "Qual o nível de automação dos processos?",
                "options": {
                    1: "Processos majoritariamente manuais",
                    2: "Automação básica (macros, scripts simples)",
                    3: "RPA em processos repetitivos selecionados",
                    4: "Automação inteligente com IA em processos-chave",
                    5: "Hyperautomation com orquestração end-to-end",
                },
            },
            {
                "id": "P2",
                "text": "Como a IA é integrada aos sistemas existentes?",
                "options": {
                    1: "IA isolada dos sistemas corporativos",
                    2: "Integração manual (exporta resultado, importa no ERP)",
                    3: "APIs de integração com sistemas principais",
                    4: "Microsserviços de IA plugados na arquitetura",
                    5: "AI-native architecture com event-driven integration",
                },
            },
            {
                "id": "P3",
                "text": "Qual a maturidade de MLOps?",
                "options": {
                    1: "Sem práticas de MLOps",
                    2: "Deploy manual de modelos",
                    3: "CI/CD para modelos com testes automatizados",
                    4: "Plataforma de MLOps com monitoramento e retraining",
                    5: "MLOps completo com feature store e model registry",
                },
            },
            {
                "id": "P4",
                "text": "Como é medido o impacto da IA nos processos?",
                "options": {
                    1: "Sem métricas de impacto",
                    2: "Métricas técnicas apenas (acurácia, latência)",
                    3: "KPIs de negócio vinculados a projetos de IA",
                    4: "ROI calculado por projeto com baseline definido",
                    5: "P&L de IA com atribuição causal de valor",
                },
            },
            {
                "id": "P5",
                "text": "Como são gerenciados os projetos de IA?",
                "options": {
                    1: "Sem metodologia — projetos ad-hoc",
                    2: "Waterfall adaptado para IA",
                    3: "Agile/CRISP-DM para projetos de dados",
                    4: "Portfolio management com priorização por valor",
                    5: "Product-led AI com squads multidisciplinares",
                },
            },
        ],
    },
    "strategy": {
        "label": "Estratégia & Liderança",
        "icon": "graph-up-arrow",
        "description": (
            "Avalia o alinhamento estratégico da IA com os objetivos "
            "de negócio, investimento e visão de longo prazo."
        ),
        "questions": [
            {
                "id": "S1",
                "text": "Existe uma estratégia formal de IA?",
                "options": {
                    1: "Sem estratégia — IA não está no radar",
                    2: "Interesse da liderança sem plano definido",
                    3: "Estratégia de IA documentada com objetivos claros",
                    4: "Roadmap de IA integrado ao planejamento estratégico",
                    5: "IA como pilar central da estratégia corporativa",
                },
            },
            {
                "id": "S2",
                "text": "Qual o investimento em IA?",
                "options": {
                    1: "Sem orçamento dedicado",
                    2: "Budget pontual para projetos específicos",
                    3: "Orçamento anual definido para IA (< 2% do revenue)",
                    4: "Investimento significativo (2-5% do revenue)",
                    5: "Investimento estratégico (> 5%) com venture arm",
                },
            },
            {
                "id": "S3",
                "text": "Como a liderança se engaja com IA?",
                "options": {
                    1: "Liderança desconectada do tema",
                    2: "Apoio passivo — 'façam se quiserem'",
                    3: "Sponsor executivo para iniciativas de IA",
                    4: "C-level defende IA publicamente e aloca recursos",
                    5: "CEO é evangelista de IA com visão transformacional",
                },
            },
            {
                "id": "S4",
                "text": "A empresa participa de ecossistemas de inovação em IA?",
                "options": {
                    1: "Sem participação em ecossistemas",
                    2: "Participa de eventos como ouvinte",
                    3: "Membro de associações e grupos de trabalho",
                    4: "Parcerias com startups, aceleradoras e universidades",
                    5: "Co-criação com ecossistema e publicações acadêmicas",
                },
            },
            {
                "id": "S5",
                "text": "Qual a visão de longo prazo para IA?",
                "options": {
                    1: "Sem visão — vive o presente",
                    2: "Consciência de que IA será importante no futuro",
                    3: "Plano de 2-3 anos para adoção de IA",
                    4: "Visão de 5 anos com cenários e contingências",
                    5: "Visão transformacional com IA reshaping o modelo de negócio",
                },
            },
        ],
    },
}

DIMENSION_KEYS = list(DIMENSIONS.keys())

SCORE_FIELD_MAP: dict[str, str] = {
    "data": "score_data",
    "algorithms": "score_algorithms",
    "governance": "score_governance",
    "talent": "score_talent",
    "process": "score_process",
    "strategy": "score_strategy",
}
