from fastapi import FastAPI
from pydantic import BaseModel
from omas.config import settings
from omas.models import AssetMode
from omas.studio import OMASStudio


app = FastAPI(title="OMAS API", version="0.1.0")
studio = OMASStudio(settings)


class GenerateRequest(BaseModel):
    mode: AssetMode


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/storyboard/validate")
def validate_storyboard() -> dict:
    scenes, errors = studio.load_storyboard()
    return {
        "total_scenes": len(scenes),
        "errors": errors,
    }


@app.post("/generate")
def generate(req: GenerateRequest) -> dict:
    return studio.generate_sync(req.mode)
