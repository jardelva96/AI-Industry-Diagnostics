"""Catálogo de casos de uso de IA por setor industrial.

Casos de uso abrangentes e realistas voltados ao setor produtivo paulista,
cobrindo manufatura, automotivo, agronegócio, logística, varejo, saúde,
financeiro e energia. Cada caso de uso inclui descrição orientada a valor
de negócio, complexidade de implementação, impacto estimado, maturidade
mínima requerida, tecnologias envolvidas, estimativa de ROI e indicação
de quick win.
"""

from __future__ import annotations

USE_CASES: dict[str, list[dict]] = {
    # ------------------------------------------------------------------
    # MANUFATURA (8 casos)
    # ------------------------------------------------------------------
    "Manufatura": [
        {
            "name": "Manutenção Preditiva de Equipamentos",
            "description": (
                "Utiliza dados de sensores IoT (vibração, temperatura, pressão) para "
                "prever falhas em máquinas antes que ocorram, reduzindo paradas não "
                "programadas em até 45% e estendendo a vida útil dos ativos."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": ["Time Series", "Random Forest", "LSTM", "IoT", "Edge Computing"],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Controle de Qualidade Visual com Visão Computacional",
            "description": (
                "Câmeras industriais combinadas com modelos de deep learning inspecionam "
                "100% das peças em linha de produção, detectando defeitos visuais como "
                "trincas, rebarbas e falhas dimensionais com precisão superior a 99%."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": ["CNN", "YOLO", "Transfer Learning", "Edge AI", "GigE Vision"],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Otimização de Processos com Digital Twin",
            "description": (
                "Cria uma réplica virtual da planta produtiva que simula cenários em "
                "tempo real, permitindo testar ajustes de parâmetros sem parar a linha "
                "e identificar gargalos antes que impactem a produção."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.5,
            "technologies": [
                "Digital Twin", "Reinforcement Learning", "Simulation",
                "Physics-Informed ML", "SCADA",
            ],
            "roi_estimate": "12-18 meses",
            "quick_win": False,
        },
        {
            "name": "Planejamento de Produção com Machine Learning",
            "description": (
                "Modelos de ML integram dados de demanda, capacidade de máquinas e "
                "disponibilidade de insumos para gerar planos de produção otimizados, "
                "reduzindo setup time e aumentando o OEE em até 15%."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "XGBoost", "Linear Programming", "Constraint Satisfaction",
                "ERP Integration",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Gestão Inteligente de Energia Industrial",
            "description": (
                "Monitora o consumo energético por máquina e turno, identificando "
                "desperdícios e sugerindo redistribuição de cargas para reduzir a conta "
                "de energia em até 20%, contribuindo também para metas ESG."
            ),
            "complexity": "Baixa",
            "impact": "Médio",
            "min_maturity": 1.5,
            "technologies": ["Time Series", "Clustering", "IoT", "Smart Meters", "Dashboard BI"],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Rastreabilidade Inteligente de Lotes",
            "description": (
                "Combina dados de produção, matéria-prima e logística para rastrear cada "
                "lote do início ao fim da cadeia, agilizando recalls e atendendo requisitos "
                "regulatórios de setores como alimentos e farmacêutico."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "Graph Database", "QR Code / RFID", "Blockchain", "ERP Integration",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Detecção de Anomalias em Linha de Produção",
            "description": (
                "Algoritmos de detecção de anomalias monitoram variáveis de processo em "
                "tempo real, alertando operadores sobre desvios antes que gerem refugo "
                "ou paradas, reduzindo perdas de material em até 30%."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "Isolation Forest", "Autoencoders", "Statistical Process Control",
                "Streaming Analytics",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Otimização de Estoque de Peças de Reposição",
            "description": (
                "Prevê a demanda de peças de reposição com base no histórico de "
                "manutenção e condição dos equipamentos, evitando tanto a falta de peças "
                "críticas quanto o capital empatado em estoque excessivo."
            ),
            "complexity": "Baixa",
            "impact": "Médio",
            "min_maturity": 1.5,
            "technologies": ["Prophet", "Safety Stock Optimization", "ABC Analysis", "ERP API"],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
    ],
    # ------------------------------------------------------------------
    # AUTOMOTIVO (5 casos)
    # ------------------------------------------------------------------
    "Automotivo": [
        {
            "name": "Inspeção Automatizada de Soldas",
            "description": (
                "Sistemas de visão computacional analisam cordões de solda em tempo "
                "real, classificando a qualidade e sinalizando defeitos como porosidade "
                "e falta de fusão, reduzindo retrabalho em até 60%."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": [
                "CNN", "3D Vision", "Laser Profilometry", "Edge AI", "IATF 16949",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Previsão de Demanda de Peças Automotivas",
            "description": (
                "Modelos preditivos combinam histórico de vendas, sazonalidade e dados "
                "macroeconômicos para antecipar a demanda de autopeças, melhorando o "
                "nível de serviço e reduzindo estoque de segurança."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "XGBoost", "Prophet", "Feature Engineering", "ERP Integration",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Otimização de Cadeia de Suprimentos Automotiva",
            "description": (
                "Analisa riscos em fornecedores, lead times e variações logísticas para "
                "recomendar estratégias de compras e estoques que minimizem rupturas na "
                "linha de montagem, especialmente em cadeias JIT/JIS."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": [
                "Network Optimization", "Monte Carlo Simulation", "NLP para Risco",
                "Supplier Scoring",
            ],
            "roi_estimate": "12-18 meses",
            "quick_win": False,
        },
        {
            "name": "Manutenção Preditiva de Robôs Industriais",
            "description": (
                "Coleta dados de torque, corrente e vibração de robôs de solda e "
                "montagem para prever degradação de servomotores e redutores, evitando "
                "paradas que podem custar centenas de milhares de reais por hora."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "LSTM", "Vibration Analysis", "OPC-UA", "Edge Computing",
                "Robotic Controller API",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Controle de Qualidade de Pintura Automotiva",
            "description": (
                "Câmeras multiespectrais e algoritmos de IA detectam defeitos de "
                "pintura como casca de laranja, escorrimento e crateras em tempo real, "
                "garantindo acabamento premium e reduzindo custo de repintura."
            ),
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.5,
            "technologies": [
                "Hyperspectral Imaging", "CNN", "Defect Classification",
                "Inline Inspection", "Color Matching AI",
            ],
            "roi_estimate": "12-18 meses",
            "quick_win": False,
        },
    ],
    # ------------------------------------------------------------------
    # AGRONEGÓCIO (5 casos)
    # ------------------------------------------------------------------
    "Agronegócio": [
        {
            "name": "Agricultura de Precisão com Drones e ML",
            "description": (
                "Drones equipados com câmeras multiespectrais sobrevoam lavouras e "
                "modelos de ML geram mapas de variabilidade para aplicação localizada "
                "de fertilizantes e defensivos, reduzindo custos de insumos em até 25%."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": [
                "Computer Vision", "NDVI", "Multispectral Imaging", "GIS",
                "Drone Autonomy",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Previsão de Safra com Dados Climáticos",
            "description": (
                "Integra dados de satélite, estações meteorológicas e histórico de "
                "produtividade para prever o volume de safra com meses de antecedência, "
                "apoiando decisões de comercialização e hedge."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "Remote Sensing", "Random Forest", "Weather API", "Satellite Imagery",
                "Geospatial ML",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Monitoramento de Pragas com Visão Computacional",
            "description": (
                "Armadilhas inteligentes e câmeras de campo capturam imagens que modelos "
                "de IA classificam automaticamente, identificando pragas e doenças em "
                "estágio inicial e reduzindo aplicações desnecessárias de defensivos."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "CNN", "Transfer Learning", "Mobile Edge", "IoT Traps",
                "Species Classification",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Otimização de Irrigação com IoT e IA",
            "description": (
                "Sensores de umidade do solo e estações climáticas alimentam modelos que "
                "determinam o momento e volume ideais de irrigação por zona, economizando "
                "até 35% de água e aumentando a produtividade por hectare."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "IoT Sensors", "Evapotranspiration Models", "Reinforcement Learning",
                "MQTT", "Pivot Control",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Gestão Inteligente de Frota Agrícola",
            "description": (
                "Telemetria de tratores, colhedoras e caminhões alimenta dashboards com "
                "alertas de manutenção, ociosidade e consumo de combustível, otimizando "
                "o uso da frota e reduzindo custos operacionais em até 20%."
            ),
            "complexity": "Baixa",
            "impact": "Médio",
            "min_maturity": 1.5,
            "technologies": [
                "GPS Tracking", "Telematics", "Anomaly Detection", "Dashboard BI",
                "CAN Bus",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
    ],
    # ------------------------------------------------------------------
    # LOGÍSTICA (5 casos)
    # ------------------------------------------------------------------
    "Logística": [
        {
            "name": "Roteirização Inteligente de Entregas",
            "description": (
                "Otimiza rotas de entrega em tempo real considerando trânsito, janelas "
                "de entrega, capacidade dos veículos e restrições de acesso, reduzindo "
                "quilometragem rodada em até 20% e melhorando o on-time delivery."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": [
                "Vehicle Routing Problem", "OR-Tools", "Reinforcement Learning",
                "Google Maps API", "Real-time Traffic",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Previsão de Demanda Logística",
            "description": (
                "Antecipa volumes de carga e entregas por região e período, permitindo "
                "dimensionar equipes, veículos e espaço de armazenagem com antecedência "
                "e evitando custos de ociosidade ou contratação emergencial."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "XGBoost", "Prophet", "Feature Engineering", "Calendar Effects",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Otimização de Armazenagem e Layout de CD",
            "description": (
                "Analisa padrões de movimentação, frequência de picking e sazonalidade "
                "para definir o posicionamento ideal de SKUs no centro de distribuição, "
                "reduzindo tempo de separação em até 30%."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "Clustering", "Slotting Optimization", "Heatmap Analysis",
                "WMS Integration",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Otimização de Last-Mile Delivery",
            "description": (
                "Combina dados de tentativas de entrega, perfil do destinatário e "
                "geolocalização para prever a melhor janela de entrega e reduzir "
                "devoluções e reentregas, principal fonte de custo do last-mile."
            ),
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": [
                "Gradient Boosting", "Geospatial Features", "Customer Scoring",
                "Route Optimization", "Real-time Tracking",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Rastreamento Preditivo de Cargas",
            "description": (
                "Prevê atrasos e desvios em entregas com base em dados de telemetria, "
                "clima e condições das rodovias, notificando proativamente clientes e "
                "permitindo ações corretivas antes que o problema se concretize."
            ),
            "complexity": "Média",
            "impact": "Médio",
            "min_maturity": 2.0,
            "technologies": [
                "Time Series", "Weather API", "GPS Analytics", "Streaming Processing",
                "Alert Engine",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
    ],
    # ------------------------------------------------------------------
    # VAREJO (5 casos)
    # ------------------------------------------------------------------
    "Varejo": [
        {
            "name": "Previsão de Demanda por SKU",
            "description": (
                "Modelos granulares preveem a demanda de cada SKU por loja e semana, "
                "considerando promoções, feriados e clima, permitindo compras mais "
                "assertivas e reduzindo perdas de perecíveis em até 25%."
            ),
            "complexity": "Média",
            "impact": "Muito Alto",
            "min_maturity": 2.5,
            "technologies": [
                "LightGBM", "Hierarchical Forecasting", "Feature Store",
                "Promotional Uplift Models",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Pricing Dinâmico e Inteligente",
            "description": (
                "Ajusta preços automaticamente com base em elasticidade, estoque, "
                "concorrência e margem-alvo, maximizando receita sem prejudicar a "
                "percepção de preço justo pelo consumidor."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": [
                "Price Elasticity Models", "Causal Inference", "Multi-armed Bandit",
                "Web Scraping", "A/B Testing",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Recomendação Personalizada de Produtos",
            "description": (
                "Sistema que combina comportamento de navegação, histórico de compras e "
                "perfil demográfico para recomendar produtos relevantes em e-commerce e "
                "CRM, aumentando ticket médio em até 15%."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "Collaborative Filtering", "Embeddings", "Real-time Feature Serving",
                "A/B Testing",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Análise de Sentimento e Voz do Cliente",
            "description": (
                "Processa reviews, menções em redes sociais e transcrições de SAC com "
                "NLP para identificar tendências de insatisfação, problemas recorrentes "
                "e oportunidades de melhoria de produto ou serviço."
            ),
            "complexity": "Baixa",
            "impact": "Médio",
            "min_maturity": 1.5,
            "technologies": [
                "NLP", "BERT", "Sentiment Analysis", "Topic Modeling", "LLM Summarization",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Prevenção de Rupturas de Gôndola",
            "description": (
                "Monitora dados de ponto de venda e estoque em tempo real para alertar "
                "sobre rupturas iminentes e acionar reposição automática, evitando perda "
                "de vendas que pode representar até 4% do faturamento."
            ),
            "complexity": "Baixa",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "Threshold Alerting", "Time Series", "POS Integration",
                "Replenishment Rules", "Dashboard BI",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
    ],
    # ------------------------------------------------------------------
    # SAÚDE (4 casos)
    # ------------------------------------------------------------------
    "Saúde": [
        {
            "name": "Triagem Inteligente com NLP",
            "description": (
                "Analisa relatos de sintomas em texto livre usando processamento de "
                "linguagem natural para classificar a gravidade e direcionar pacientes "
                "ao fluxo correto, reduzindo tempo de espera e sobrecarga da equipe."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "NLP", "BERT", "Clinical NER", "Classification Models",
                "EHR Integration",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Gestão Preditiva de Leitos Hospitalares",
            "description": (
                "Prevê a ocupação de leitos por ala e especialidade com base em "
                "sazonalidade, agendamentos e perfil de pacientes, permitindo "
                "planejamento antecipado e redução de cirurgias canceladas por falta de vaga."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "Time Series", "Simulation", "Queueing Theory",
                "Hospital Information System",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Previsão de Readmissão Hospitalar",
            "description": (
                "Identifica pacientes com alto risco de readmissão em 30 dias usando "
                "dados clínicos, sociais e de utilização, permitindo intervenções "
                "preventivas que reduzem custos e melhoram os desfechos."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "Logistic Regression", "XGBoost", "SHAP", "EHR / FHIR",
                "Risk Stratification",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Otimização de Estoque Hospitalar",
            "description": (
                "Prevê o consumo de medicamentos, materiais e OPME por especialidade "
                "e sazonalidade, evitando desperdícios por vencimento e garantindo "
                "disponibilidade de itens críticos para cirurgias e emergências."
            ),
            "complexity": "Baixa",
            "impact": "Médio",
            "min_maturity": 1.5,
            "technologies": [
                "Demand Forecasting", "ABC/XYZ Analysis", "Safety Stock Optimization",
                "Pharmacy System Integration",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
    ],
    # ------------------------------------------------------------------
    # FINANCEIRO (4 casos)
    # ------------------------------------------------------------------
    "Financeiro": [
        {
            "name": "Detecção de Fraude em Tempo Real",
            "description": (
                "Analisa transações em milissegundos usando modelos de anomalia e grafos "
                "para bloquear operações fraudulentas antes da aprovação, reduzindo "
                "perdas com fraude em até 70% sem impactar a experiência do cliente legítimo."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": [
                "Graph Neural Networks", "Anomaly Detection", "Real-time Scoring",
                "Feature Store", "Stream Processing",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Credit Scoring com Dados Alternativos",
            "description": (
                "Modelos de ML incorporam dados não tradicionais (comportamento "
                "digital, pagamentos recorrentes, dados abertos) para avaliar risco de "
                "crédito com mais precisão, ampliando a base de clientes atendidos."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": [
                "XGBoost", "SHAP", "Fairness Metrics", "Open Finance API",
                "BACEN Compliance",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Automação Inteligente de Compliance",
            "description": (
                "Combina NLP e regras de negócio para automatizar a análise de "
                "documentos regulatórios, KYC e PLD/FT, reduzindo o tempo de onboarding "
                "de clientes e o custo por análise em até 60%."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": [
                "NLP", "OCR", "Named Entity Recognition", "Rule Engine",
                "LLM Extraction",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
        {
            "name": "Previsão de Churn de Clientes",
            "description": (
                "Identifica clientes com probabilidade de encerrar o relacionamento nos "
                "próximos 90 dias, priorizando ações de retenção personalizadas que "
                "podem reduzir a taxa de churn em até 25%."
            ),
            "complexity": "Baixa",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "Logistic Regression", "Survival Analysis", "CRM Integration",
                "Campaign Automation",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
    ],
    # ------------------------------------------------------------------
    # ENERGIA (4 casos)
    # ------------------------------------------------------------------
    "Energia": [
        {
            "name": "Previsão de Consumo Energético",
            "description": (
                "Prevê a demanda de energia por região, horário e perfil de consumidor, "
                "permitindo melhor contratação no mercado livre, redução de multas por "
                "ultrapassagem de demanda e planejamento de geração distribuída."
            ),
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.0,
            "technologies": [
                "Time Series", "LSTM", "Weather Correlation", "Smart Metering",
                "CCEE Integration",
            ],
            "roi_estimate": "3-6 meses",
            "quick_win": True,
        },
        {
            "name": "Manutenção Preditiva de Transformadores",
            "description": (
                "Analisa dados de cromatografia de gases, temperatura e carga para "
                "prever falhas em transformadores de potência, evitando interrupções "
                "que afetam milhares de consumidores e custam milhões em reparos."
            ),
            "complexity": "Alta",
            "impact": "Muito Alto",
            "min_maturity": 3.0,
            "technologies": [
                "Dissolved Gas Analysis", "Random Forest", "IoT Sensors",
                "Condition-Based Monitoring", "SCADA",
            ],
            "roi_estimate": "12-18 meses",
            "quick_win": False,
        },
        {
            "name": "Otimização de Distribuição de Energia",
            "description": (
                "Modelos de otimização ajustam chaveamento e reconfiguração da rede de "
                "distribuição em tempo real para minimizar perdas técnicas, equilibrar "
                "cargas e melhorar os indicadores DEC e FEC."
            ),
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.5,
            "technologies": [
                "Network Optimization", "SCADA", "Power Flow Analysis",
                "Reinforcement Learning", "GIS",
            ],
            "roi_estimate": "12-18 meses",
            "quick_win": False,
        },
        {
            "name": "Detecção de Perdas Não-Técnicas",
            "description": (
                "Identifica fraudes e furtos de energia analisando padrões anômalos de "
                "consumo em medidores inteligentes, priorizando inspeções de campo com "
                "taxa de acerto superior a 80% e recuperando receita perdida."
            ),
            "complexity": "Média",
            "impact": "Muito Alto",
            "min_maturity": 2.5,
            "technologies": [
                "Anomaly Detection", "Clustering", "Smart Metering",
                "Gradient Boosting", "GIS / Geospatial",
            ],
            "roi_estimate": "6-12 meses",
            "quick_win": False,
        },
    ],
}

SECTORS = list(USE_CASES.keys())
