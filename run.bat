@echo off
setlocal

echo ============================================
echo   AI Industry Diagnostics - Inicializando
echo ============================================

:: Cria venv se nao existe
if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Criando ambiente virtual...
    python -m venv .venv
)

:: Instala dependencias
echo [2/3] Instalando dependencias...
.venv\Scripts\pip.exe install -q -e ".[dev]" 2>nul

:: Configura Streamlit (sem prompt de email)
if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
    echo [general] > "%USERPROFILE%\.streamlit\credentials.toml"
    echo email = "" >> "%USERPROFILE%\.streamlit\credentials.toml"
)

echo [3/3] Iniciando servidor API e Dashboard...
echo.
echo   API:       http://localhost:8000/docs
echo   Dashboard: http://localhost:8501
echo   Login:     admin / admin123
echo.

:: Inicia API em background
start /B .venv\Scripts\python.exe -m uvicorn aidiag.app:app --host 0.0.0.0 --port 8000

:: Aguarda API iniciar
timeout /t 3 /nobreak >nul

:: Inicia Dashboard (abre navegador)
.venv\Scripts\python.exe -m streamlit run src/aidiag/dashboard.py --server.port 8501

endlocal
