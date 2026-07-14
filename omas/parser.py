import re
from omas.models import Scene


SEGMENT_PATTERN = re.compile(r"^Segment\s+(\d+)\s*$", re.IGNORECASE)


def parse_storyboard(content: str) -> list[Scene]:
    lines = content.splitlines()
    scenes: list[Scene] = []

    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        seg = SEGMENT_PATTERN.match(line)
        if not seg:
            idx += 1
            continue

        segment_number = int(seg.group(1))
        idx += 1
        script = ""
        image_prompt = ""
        video_prompt = ""

        current_section = None
        section_lines: list[str] = []

        def flush() -> tuple[str, str, str]:
            nonlocal script, image_prompt, video_prompt, section_lines, current_section
            text = "\n".join(section_lines).strip()
            if current_section == "script":
                script = text
            elif current_section == "image":
                image_prompt = text
            elif current_section == "video":
                video_prompt = text
            section_lines = []
            current_section = None
            return script, image_prompt, video_prompt

        while idx < len(lines):
            raw = lines[idx]
            stripped = raw.strip()
            if SEGMENT_PATTERN.match(stripped):
                flush()
                break
            lower = stripped.lower()
            if lower == "script:":
                flush()
                current_section = "script"
            elif lower == "image prompt:":
                flush()
                current_section = "image"
            elif lower == "video prompt:":
                flush()
                current_section = "video"
            elif current_section:
                section_lines.append(raw)
            idx += 1

        flush()
        scenes.append(
            Scene(
                segment_number=segment_number,
                script=script,
                image_prompt=image_prompt,
                video_prompt=video_prompt,
            )
        )

    return scenes
