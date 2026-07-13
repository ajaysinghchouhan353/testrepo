from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OMAS_", extra="ignore")

    project_root: Path = Field(default=Path("project"))
    storyboard_file: str = "storyboard.md"
    default_image_provider: str = "gemini"
    default_video_provider: str = "gemini_veo"
    parallel_workers: int = 4
    retry_count: int = 2
    timeout_seconds: int = 120
    validation_strictness: str = "strict"
    resume_mode: bool = True
    logging_level: str = "INFO"

    @property
    def input_dir(self) -> Path:
        return self.project_root / "input"

    @property
    def output_dir(self) -> Path:
        return self.project_root / "output"

    @property
    def images_dir(self) -> Path:
        return self.output_dir / "images"

    @property
    def videos_dir(self) -> Path:
        return self.output_dir / "videos"

    @property
    def logs_dir(self) -> Path:
        return self.output_dir / "logs"

    @property
    def reports_dir(self) -> Path:
        return self.output_dir / "reports"

    @property
    def database_dir(self) -> Path:
        return self.project_root / "database"

    @property
    def continuity_dir(self) -> Path:
        return self.project_root / "continuity"


settings = Settings()
