# AI Industry Diagnostics

**Plataforma de diagnóstico de maturidade em Inteligência Artificial para o setor produtivo brasileiro.**

Desenvolvida no contexto do CPA **CDII — Ciência de Dados para a Indústria Inteligente** (FAPESP 2023/14427-8), sediado no ICMC-USP com parceria do AI2 — Advanced Institute for Artificial Intelligence.

[![CI](https://github.com/jardelva96/AI-Industry-Diagnostics/actions/workflows/ci.yml/badge.svg)](https://github.com/jardelva96/AI-Industry-Diagnostics/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Início Rápido

```bash
# Clone o repositório
git clone https://github.com/jardelva96/AI-Industry-Diagnostics.git
cd AI-Industry-Diagnostics

# Execute (Windows)
.\run.bat

# Execute (Linux/Mac)
chmod +x run.sh && ./run.sh
```

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| Dashboard | http://localhost:8501 | — |
| API Swagger | http://localhost:8000/docs | admin / admin123 |

---

## O que é?

Uma ferramenta para **Consultores de Diagnóstico em IA** que precisam:

1. **Avaliar** o nível de maturidade em IA de empresas industriais
2. **Diagnosticar** pontos fortes e gaps críticos em 6 dimensões
3. **Gerar roadmaps** de adoção de IA personalizados
4. **Comparar** com benchmarks setoriais (McKinsey, Gartner, MIT CISR)
5. **Mapear** casos de uso viáveis por setor e nível de maturidade

---

## Framework de Avaliação

O questionário de **30 perguntas** avalia 6 dimensões, cada uma pontuada de 1 (Inicial) a 5 (Líder):

| Dimensão | O que avalia |
|----------|-------------|
| **Dados & Infraestrutura** | Qualidade, governança de dados e infra computacional |
| **Algoritmos & Modelos** | Adoção de ML/DL, MLOps e IA generativa |
| **Governança & Ética** | Políticas de uso responsável e compliance (LGPD, EU AI Act) |
| **Talentos & Cultura** | Equipe de dados, capacitação e cultura de experimentação |
| **Processos & Integração** | Automação, integração sistêmica e gestão de projetos |
| **Estratégia & Liderança** | Visão estratégica, investimento e engajamento executivo |

### Níveis de Maturidade

| Score | Nível | Descrição |
|-------|-------|-----------|
| 1.0 – 1.4 | Inicial | Sem iniciativas estruturadas |
| 1.5 – 2.4 | Básico | Primeiros passos com ações isoladas |
| 2.5 – 3.4 | Intermediário | Práticas estabelecidas com resultados |
| 3.5 – 4.4 | Avançado | Excelência operacional e otimização |
| 4.5 – 5.0 | Líder | Referência no mercado com inovação contínua |

---

## Funcionalidades

### Dashboard Interativo
- Questionário de avaliação com 30 perguntas
- Radar de maturidade com visualização por dimensão
- Recomendações contextualizadas por nível

### Diagnóstico Analítico
- Identificação de pontos fortes e gaps críticos
- Recomendações priorizadas por dimensão
- Comparação com benchmarks setoriais

### Roadmap de Adoção
- Plano em 3 fases: Fundação (0-6m), Escala (6-12m), Transformação (12-24m)
- Ações específicas baseadas nos gaps identificados
- Timeline visual com impacto esperado

### Benchmark Setorial
- Comparação com médias de 8 setores industriais
- Radar comparativo empresa vs. setor
- Posicionamento relativo por dimensão

### Catálogo de Casos de Uso
- 20+ casos de uso de IA por setor (Manufatura, Varejo, Saúde, Financeiro, Agro, Logística)
- Classificação por complexidade, impacto e maturidade mínima
- Tecnologias recomendadas por caso de uso

### Pipeline de ML
- Classificadores Random Forest e Gradient Boosting
- Cross-validation com F1 macro
- Feature importance por dimensão
- Demonstração de pipeline completo de ML

---

## Arquitetura

```
src/aidiag/
├── app.py                  # FastAPI — API REST principal
├── dashboard.py            # Streamlit — interface interativa
├── models.py               # SQLAlchemy — modelos ORM
├── schemas.py              # Pydantic — validação de dados
├── auth.py                 # JWT — autenticação e autorização
├── config.py               # Configurações centrais
├── database.py             # Conexão com banco de dados
├── api/
│   ├── assessments.py      # CRUD de avaliações e empresas
│   ├── diagnostics.py      # Geração de diagnósticos
│   └── roadmaps.py         # Geração de roadmaps
├── services/
│   ├── assessment_service.py    # Lógica de avaliação
│   ├── diagnostic_service.py    # Análise diagnóstica
│   ├── roadmap_service.py       # Geração de roadmap
│   ├── ml_pipeline.py           # Pipeline de ML
│   └── benchmark_service.py     # Benchmarks setoriais
└── data/
    ├── dimensions.py       # Questionário de 30 perguntas
    └── use_cases.py        # Catálogo de casos de uso
```

## Tecnologias

| Componente | Tecnologia |
|------------|------------|
| API REST | FastAPI |
| Dashboard | Streamlit + Plotly |
| Banco de dados | SQLAlchemy + SQLite |
| Machine Learning | scikit-learn |
| Autenticação | JWT (python-jose) + bcrypt |
| Validação | Pydantic |
| Testes | pytest |
| Lint | ruff |
| CI/CD | GitHub Actions |

---

## Autor

**Jardel Vieira Alves**
