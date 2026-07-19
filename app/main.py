from app.core.logging_config import configurar_logs
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import (
    auth,
    cidades,
    dashboard,
    etapas_trajetoria,
    eventos,
    faixas_etarias,
    filiais,
    filiais_trajetorias,
    kids,
    ministerios,
    pessoas,
    trajetorias,
    trajetorias_etapas,
    vinculos,
)

configurar_logs()

app = FastAPI(
    title="Renascer BSB API",
    description="API do Sistema de Gestao Ministerial da Igreja Renascer BSB",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://renascerbsb.github.io",
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_required = [Depends(auth.obter_usuario_autenticado)]

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(
    pessoas.router,
    prefix="/pessoas",
    tags=["Pessoas"],
    dependencies=auth_required
)
app.include_router(
    kids.router,
    prefix="/kids",
    tags=["Kids"],
    dependencies=auth_required
)
app.include_router(
    eventos.router,
    prefix="/eventos",
    tags=["Eventos"],
    dependencies=auth_required
)
app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=auth_required
)
app.include_router(
    cidades.router,
    prefix="/cidades",
    tags=["Cidades"],
    dependencies=auth_required
)
app.include_router(
    filiais.router,
    prefix="/filiais",
    tags=["Filiais"],
    dependencies=auth_required
)
app.include_router(
    filiais_trajetorias.router,
    prefix="/filiais-trajetorias",
    tags=["Trajetorias das Filiais"],
    dependencies=auth_required
)
app.include_router(
    faixas_etarias.router,
    prefix="/faixas-etarias",
    tags=["Faixas Etarias"],
    dependencies=auth_required
)
app.include_router(
    ministerios.router,
    prefix="/ministerios",
    tags=["Ministerios"],
    dependencies=auth_required
)
app.include_router(
    vinculos.router,
    prefix="/vinculos",
    tags=["Vinculos"],
    dependencies=auth_required
)
app.include_router(
    etapas_trajetoria.router,
    prefix="/etapas-trajetoria",
    tags=["Etapas de Trajetoria"],
    dependencies=auth_required
)
app.include_router(
    trajetorias.router,
    prefix="/trajetorias",
    tags=["Trajetorias"],
    dependencies=auth_required
)
app.include_router(
    trajetorias_etapas.router,
    prefix="/trajetorias-etapas",
    tags=["Etapas das Trajetorias"],
    dependencies=auth_required
)


@app.get("/")
def home():
    return {"mensagem": "API Renascer BSB online"}
