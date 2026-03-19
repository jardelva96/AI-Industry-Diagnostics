#!/usr/bin/env bash
set -e

echo "============================================"
echo "  AI Industry Diagnostics - Inicializando"
echo "============================================"

# Cria venv se nao existe
if [ ! -f ".venv/bin/python" ]; then
    echo "[1/3] Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Instala dependencias
echo "[2/3] Instalando dependencias..."
.venv/bin/pip install -q -e ".[dev]" 2>/dev/null

# Configura Streamlit
mkdir -p "$HOME/.streamlit"
if [ ! -f "$HOME/.streamlit/credentials.toml" ]; then
    printf '[general]\nemail = ""\n' > "$HOME/.streamlit/credentials.toml"
fi

echo "[3/3] Iniciando servidor API e Dashboard..."
echo ""
echo "  API:       http://localhost:8000/docs"
echo "  Dashboard: http://localhost:8501"
echo "  Login:     admin / admin123"
echo ""

# Inicia API em background
.venv/bin/python -m uvicorn aidiag.app:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Aguarda API
sleep 3

# Inicia Dashboard
.venv/bin/python -m streamlit run src/aidiag/dashboard.py --server.port 8501

# Cleanup
kill $API_PID 2>/dev/null
