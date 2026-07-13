from pathlib import Path
from omas.config import Settings
from omas.models import AssetMode
from omas.output_manager import ensure_directories, output_path_for, resume_from


def test_output_naming_and_resume(tmp_path: Path):
    cfg = Settings(project_root=tmp_path)
    ensure_directories(cfg)

    p1 = output_path_for(25, AssetMode.IMAGE, cfg)
    assert p1.name == "25.jpg"
    p1.write_bytes(b"x")

    assert resume_from(AssetMode.IMAGE, cfg) == 26
