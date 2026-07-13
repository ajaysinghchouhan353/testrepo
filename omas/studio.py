import asyncio
from pathlib import Path
from loguru import logger
from omas.config import Settings
from omas.continuity import ContinuityEngine
from omas.database import Database
from omas.guardrail import validate_asset
from omas.models import AssetMode, GenerationJob
from omas.output_manager import ensure_directories, output_path_for, resume_from
from omas.parser import parse_storyboard
from omas.prompt_builder import build_prompt
from omas.providers.registry import ProviderRegistry
from omas.queue import GenerationQueue
from omas.validator import validate_scenes


class OMASStudio:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.providers = ProviderRegistry()
        self.continuity = ContinuityEngine()
        self.db = Database(settings.database_dir / "omas.db")
        self.db.init()
        ensure_directories(settings)

    def load_storyboard(self, storyboard_path: Path | None = None):
        path = storyboard_path or (self.settings.project_root / self.settings.storyboard_file)
        scenes = parse_storyboard(path)
        errors = validate_scenes(scenes)
        return scenes, errors

    async def generate(self, mode: AssetMode, storyboard_path: Path | None = None) -> dict:
        scenes, errors = self.load_storyboard(storyboard_path)
        if errors:
            return {"status": "error", "errors": errors}

        start_at = resume_from(mode, self.settings) if self.settings.resume_mode else 1
        queue = GenerationQueue(self.settings.parallel_workers, self.settings.retry_count)
        provider_name = (
            self.settings.default_image_provider if mode == AssetMode.IMAGE else self.settings.default_video_provider
        )
        provider = self.providers.get(provider_name)

        for scene in scenes:
            if scene.segment_number < start_at:
                continue
            self.continuity.update_from_scene(scene)
            prompt = build_prompt(scene, mode, self.continuity)
            out = output_path_for(scene.segment_number, mode, self.settings)
            await queue.put(
                GenerationJob(
                    scene=scene,
                    mode=mode,
                    prompt=prompt,
                    output_path=out,
                    provider=provider_name,
                )
            )

        async def worker_fn(job: GenerationJob) -> None:
            logger.info(f"Generating scene {job.scene.segment_number} ({job.mode})")
            if job.mode == AssetMode.IMAGE:
                await provider.generate_image(job.prompt, job.output_path)
            else:
                await provider.generate_video(job.prompt, job.output_path)
            validate_asset(job.output_path, job.mode)

        await queue.run(worker_fn)

        return {
            "status": "ok",
            "completed": queue.completed,
            "failed": queue.failed,
            "start_at": start_at,
        }

    def generate_sync(self, mode: AssetMode, storyboard_path: Path | None = None) -> dict:
        return asyncio.run(self.generate(mode, storyboard_path))
