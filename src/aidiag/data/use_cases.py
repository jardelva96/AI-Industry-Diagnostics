"""Catálogo de casos de uso de IA por setor industrial.

Cada caso de uso inclui descrição, complexidade de implementação,
impacto estimado e dimensões de maturidade requeridas.
"""

from __future__ import annotations

USE_CASES: dict[str, list[dict]] = {
    "Manufatura": [
        {
            "name": "Manutenção Preditiva",
            "description": "Prever falhas em equipamentos usando dados de sensores IoT para reduzir downtime",
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": ["Time Series", "Random Forest", "LSTM", "IoT"],
        },
        {
            "name": "Controle de Qualidade Visual",
            "description": "Inspeção automática de defeitos em linha de produção com visão computacional",
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": ["CNN", "YOLO", "Transfer Learning", "Edge AI"],
        },
        {
            "name": "Otimização de Produção",
            "description": "Ajuste dinâmico de parâmetros de produção para maximizar throughput e reduzir desperdício",
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.5,
            "technologies": ["Reinforcement Learning", "Digital Twin", "Optimization"],
        },
        {
            "name": "Previsão de Demanda",
            "description": "Forecast de demanda para planejamento de produção e estoque",
            "complexity": "Média",
            "impact": "Médio",
            "min_maturity": 2.0,
            "technologies": ["ARIMA", "Prophet", "XGBoost", "Transformer"],
        },
    ],
    "Varejo": [
        {
            "name": "Recomendação de Produtos",
            "description": "Sistema de recomendação personalizado para e-commerce e loja física",
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": ["Collaborative Filtering", "Embeddings", "A/B Testing"],
        },
        {
            "name": "Precificação Dinâmica",
            "description": "Ajuste de preços em tempo real baseado em demanda, concorrência e elasticidade",
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": ["Optimization", "Causal Inference", "Multi-armed Bandit"],
        },
        {
            "name": "Análise de Sentimento",
            "description": "Monitoramento de satisfação do cliente via reviews, redes sociais e SAC",
            "complexity": "Baixa",
            "impact": "Médio",
            "min_maturity": 2.0,
            "technologies": ["NLP", "BERT", "Sentiment Analysis"],
        },
        {
            "name": "Prevenção de Fraude",
            "description": "Detecção de transações fraudulentas em tempo real no e-commerce",
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": ["Anomaly Detection", "Graph Neural Networks", "Real-time ML"],
        },
    ],
    "Saúde": [
        {
            "name": "Diagnóstico Assistido por IA",
            "description": "Auxílio diagnóstico em imagens médicas (raio-X, tomografia, ressonância)",
            "complexity": "Muito Alta",
            "impact": "Alto",
            "min_maturity": 4.0,
            "technologies": ["CNN", "Vision Transformer", "DICOM", "FDA/ANVISA"],
        },
        {
            "name": "Predição de Readmissão",
            "description": "Identificar pacientes com risco de readmissão hospitalar em 30 dias",
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": ["Logistic Regression", "XGBoost", "EHR", "FHIR"],
        },
        {
            "name": "Otimização de Leitos",
            "description": "Previsão de ocupação e alocação inteligente de leitos hospitalares",
            "complexity": "Média",
            "impact": "Médio",
            "min_maturity": 2.5,
            "technologies": ["Time Series", "Simulation", "Optimization"],
        },
    ],
    "Financeiro": [
        {
            "name": "Credit Scoring com ML",
            "description": "Modelos de crédito mais precisos usando dados alternativos e ML",
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": ["XGBoost", "SHAP", "Fairness Metrics", "BACEN"],
        },
        {
            "name": "Detecção de Lavagem de Dinheiro",
            "description": "Identificação de padrões suspeitos em transações financeiras",
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.5,
            "technologies": ["Graph Analytics", "Anomaly Detection", "NLP"],
        },
        {
            "name": "Chatbot Financeiro",
            "description": "Assistente virtual para atendimento ao cliente com processamento de linguagem natural",
            "complexity": "Média",
            "impact": "Médio",
            "min_maturity": 2.5,
            "technologies": ["LLM", "RAG", "Dialog Management"],
        },
    ],
    "Agronegócio": [
        {
            "name": "Agricultura de Precisão",
            "description": "Monitoramento por drone/satélite com IA para otimizar irrigação e aplicação de insumos",
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": ["Computer Vision", "Satellite Imagery", "GIS", "IoT"],
        },
        {
            "name": "Previsão de Safra",
            "description": "Estimativa de produtividade usando dados climáticos, solo e imagens",
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": ["Remote Sensing", "Random Forest", "Weather API"],
        },
        {
            "name": "Detecção de Pragas",
            "description": "Identificação precoce de pragas e doenças via imagens de plantas",
            "complexity": "Média",
            "impact": "Alto",
            "min_maturity": 2.5,
            "technologies": ["CNN", "Transfer Learning", "Mobile Edge"],
        },
    ],
    "Logística": [
        {
            "name": "Roteirização Inteligente",
            "description": "Otimização de rotas de entrega considerando trânsito, janelas e capacidade",
            "complexity": "Alta",
            "impact": "Alto",
            "min_maturity": 3.0,
            "technologies": ["Vehicle Routing Problem", "OR-Tools", "Reinforcement Learning"],
        },
        {
            "name": "Previsão de Atrasos",
            "description": "Prever atrasos em entregas com base em dados históricos e condições atuais",
            "complexity": "Média",
            "impact": "Médio",
            "min_maturity": 2.0,
            "technologies": ["Gradient Boosting", "Weather API", "Real-time Data"],
        },
    ],
}

SECTORS = list(USE_CASES.keys())
