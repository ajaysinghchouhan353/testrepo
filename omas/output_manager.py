from pathlib import Path
from omas.config import Settings
from omas.models import AssetMode


def ensure_directories(settings: Settings) -> None:
    for path in [
        settings.project_root,
        settings.input_dir,
        settings.output_dir,
        settings.images_dir,
        settings.videos_dir,
        settings.logs_dir,
        settings.reports_dir,
        settings.database_dir,
        settings.continuity_dir,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def output_path_for(scene_number: int, mode: AssetMode, settings: Settings) -> Path:
    if mode == AssetMode.IMAGE:
        return settings.images_dir / f"{scene_number}.jpg"
    return settings.videos_dir / f"{scene_number}.mp4"


def resume_from(mode: AssetMode, settings: Settings) -> int:
    target_dir = settings.images_dir if mode == AssetMode.IMAGE else settings.videos_dir
    ext = ".jpg" if mode == AssetMode.IMAGE else ".mp4"
    if not target_dir.exists():
        return 1
    nums: list[int] = []
    for file in target_dir.glob(f"*{ext}"):
        try:
            nums.append(int(file.stem))
        except ValueError:
            continue
    return max(nums) + 1 if nums else 1
