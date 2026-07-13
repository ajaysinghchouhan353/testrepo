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
        ensure_directories(settings)
        self.providers = ProviderRegistry()
        self.continuity = ContinuityEngine()
        self.db = Database(settings.database_dir / "omas.db")
        self.db.init()

    def load_storyboard(self):
        path = self.settings.project_root / self.settings.storyboard_file
        text = self._read_storyboard(path)
        scenes = parse_storyboard(text)
        errors = validate_scenes(scenes)
        return scenes, errors

    def _read_storyboard(self, path: Path) -> str:
        resolved = path.expanduser().resolve(strict=True)
        root = self.settings.project_root.expanduser().resolve(strict=True)
        if resolved.suffix.lower() not in {".md", ".txt"}:
            raise ValueError("Storyboard file must be .md or .txt")
        if not resolved.is_file():
            raise ValueError("Storyboard path must be a file")
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError("Storyboard path must be inside project root") from exc
        return resolved.read_text(encoding="utf-8")

    async def generate(self, mode: AssetMode) -> dict:
        scenes, errors = self.load_storyboard()
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

    def generate_sync(self, mode: AssetMode) -> dict:
        return asyncio.run(self.generate(mode))
