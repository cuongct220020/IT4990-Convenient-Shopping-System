from core.database import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
from models.ingredient import Ingredient, IngredientTag

app = FastAPI(
    title="Ingredient Service",
    description="API for managing ingredients",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)