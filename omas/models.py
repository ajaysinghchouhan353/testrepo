from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field


class AssetMode(str, Enum):
    IMAGE = "image"
    VIDEO = "video"


class Scene(BaseModel):
    segment_number: int = Field(gt=0)
    script: str
    image_prompt: str
    video_prompt: str


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerationJob(BaseModel):
    scene: Scene
    mode: AssetMode
    prompt: str
    output_path: Path
    provider: str
    retries: int = 0
    status: JobStatus = JobStatus.PENDING
    error: str | None = None
