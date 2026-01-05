from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.hello import router as hello_router
from app.routes.insights import router as insights_router
from app.routes.checkins import router as checkins_router
from app.routes.health import router as health_router

app = FastAPI(title="AIVA Platform", version="1.0")

app.include_router(hello_router, prefix="/v1")
app.include_router(insights_router, prefix="/v1")
app.include_router(checkins_router, prefix="/v1")
app.include_router(health_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "AIVA is running 🚀"}


@app.get("/transactions/mock")
def get_mock_transactions():
    return load_mock_transactions()
