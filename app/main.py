from fastapi import FastAPI

from app.routes.pipeline import router as pipeline_router

app = FastAPI()

app.include_router(pipeline_router, prefix="/api")


@app.get("/")
def get_pipeline_status():
    return {"status": "API go brrrr"}

