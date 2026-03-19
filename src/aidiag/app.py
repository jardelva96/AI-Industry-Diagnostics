"""Aplicação FastAPI principal."""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from aidiag.api.assessments import router as assessments_router
from aidiag.api.diagnostics import router as diagnostics_router
from aidiag.api.roadmaps import router as roadmaps_router
from aidiag.auth import create_access_token, hash_password, verify_password
from aidiag.config import settings
from aidiag.database import get_db, init_db
from aidiag.models import AuditLog, User
from aidiag.schemas import Token, UserCreate, UserOut
from aidiag.services.ml_pipeline import predict_maturity, train_maturity_classifier

app = FastAPI(
    title="AI Industry Diagnostics",
    description="API de diagnóstico de maturidade em IA para o setor produtivo",
    version="0.1.0",
)

app.include_router(assessments_router, prefix="/api")
app.include_router(diagnostics_router, prefix="/api")
app.include_router(roadmaps_router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    """Inicializa banco e cria admin padrão."""
    init_db()
    db = next(get_db())
    try:
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                email="admin@aidiag.local",
                hashed_password=hash_password("admin123"),
                full_name="Administrador",
                role="admin",
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


# ── Auth ──────────────────────────────────────────────────────────────
@app.post("/api/auth/login", response_model=Token, tags=["Autenticação"])
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica usuário e retorna JWT."""
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    db.add(AuditLog(user_id=user.id, action="login", target=user.username))
    db.commit()
    token = create_access_token({"sub": user.username})
    return Token(access_token=token)


@app.post("/api/auth/register", response_model=UserOut, status_code=201, tags=["Autenticação"])
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """Registra novo usuário."""
    if db.query(User).filter(User.username == payload.username).first():
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="Usuário já existe")
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── ML ────────────────────────────────────────────────────────────────
@app.get("/api/ml/train", tags=["Machine Learning"])
def ml_train():
    """Treina classificador de maturidade e retorna métricas."""
    return train_maturity_classifier()


@app.post("/api/ml/predict", tags=["Machine Learning"])
def ml_predict(scores: list[float]):
    """Prediz nível de maturidade a partir de 6 scores."""
    return predict_maturity(scores)


# ── Health ────────────────────────────────────────────────────────────
@app.get("/health", tags=["Sistema"])
def health():
    """Health check."""
    return {"status": "ok", "app": settings.app_name}


def main() -> None:
    """Inicia servidor uvicorn."""
    import uvicorn

    uvicorn.run("aidiag.app:app", host="0.0.0.0", port=settings.api_port, reload=True)
