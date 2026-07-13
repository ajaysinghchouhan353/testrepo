from omas.models import Scene
from omas.validator import validate_scenes


def test_validate_scenes_ok():
    scenes = [
        Scene(segment_number=1, script="s1", image_prompt="i1", video_prompt="v1"),
        Scene(segment_number=2, script="s2", image_prompt="i2", video_prompt="v2"),
    ]
    assert validate_scenes(scenes) == []


def test_validate_scenes_detects_errors():
    scenes = [
        Scene(segment_number=1, script="", image_prompt="i1", video_prompt="v1"),
        Scene(segment_number=3, script="s3", image_prompt="", video_prompt="v3"),
    ]
    errors = validate_scenes(scenes)
    assert any("missing script" in e for e in errors)
    assert any("Incorrect order" in e for e in errors)
