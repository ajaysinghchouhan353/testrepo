from pathlib import Path
from omas.config import Settings
from omas.models import AssetMode
from omas.studio import OMASStudio


def test_studio_validate(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    storyboard = project / "storyboard.md"
    storyboard.write_text(
        """
Segment 1
Script:
Documentary scene.
Image Prompt:
Cinematic frame.
Video Prompt:
Cinematic clip.
""".strip(),
        encoding="utf-8",
    )

    settings = Settings(project_root=project)
    studio = OMASStudio(settings)
    scenes, errors = studio.load_storyboard(storyboard)
    assert len(scenes) == 1
    assert errors == []


def test_studio_generate_image(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    storyboard = project / "storyboard.md"
    storyboard.write_text(
        """
Segment 1
Script:
Documentary scene.
Image Prompt:
Cinematic frame.
Video Prompt:
Cinematic clip.
""".strip(),
        encoding="utf-8",
    )

    settings = Settings(project_root=project)
    studio = OMASStudio(settings)
    result = studio.generate_sync(AssetMode.IMAGE, storyboard)
    assert result["status"] == "ok"
    assert (settings.images_dir / "1.jpg").exists()
