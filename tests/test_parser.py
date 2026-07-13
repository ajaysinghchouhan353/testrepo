from pathlib import Path
from omas.parser import parse_storyboard


def test_parse_storyboard(tmp_path: Path):
    file = tmp_path / "storyboard.md"
    file.write_text(
        """
Segment 1
Script:
A man enters the office.
Image Prompt:
A cinematic shot of a man entering an office.
Video Prompt:
A tracking shot of a man entering an office.

Segment 2
Script:
He sits at a desk.
Image Prompt:
A close-up of him sitting at a desk.
Video Prompt:
A medium shot of him sitting at a desk.
""".strip(),
        encoding="utf-8",
    )

    scenes = parse_storyboard(file.read_text(encoding="utf-8"))
    assert len(scenes) == 2
    assert scenes[0].segment_number == 1
    assert "office" in scenes[0].script
