from fastapi import FastAPI

from app.api.routes import eventos, membros,  kids, dashboard, cidades, filiais, ministerios, vinculos

app = FastAPI(
    title="Renascer BSB API",
    description="API do Sistema de Gestão Ministerial da Igreja Renascer BSB",
    version="0.1.0"
)

app.include_router(membros.router, prefix="/membros", tags=["Membros"])
app.include_router(kids.router, prefix="/kids", tags=["Kids"])
app.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(cidades.router, prefix="/cidades", tags=["Cidades"])
app.include_router(filiais.router, prefix="/filiais", tags=["Filiais"])
app.include_router(ministerios.router, prefix="/ministerios", tags=["Ministérios"])
app.include_router(vinculos.router, prefix="/vinculos", tags=["Vínculos"])


@app.get("/")
def home():
    return {"mensagem": "API Renascer BSB online"}