from omas.models import Scene


def validate_scenes(scenes: list[Scene]) -> list[str]:
    errors: list[str] = []
    seen: set[int] = set()
    expected = 1

    for scene in scenes:
        if scene.segment_number in seen:
            errors.append(f"Duplicate scene number: {scene.segment_number}")
        seen.add(scene.segment_number)

        if scene.segment_number != expected:
            errors.append(f"Incorrect order at scene {scene.segment_number}; expected {expected}")
            expected = scene.segment_number
        expected += 1

        if not scene.script.strip():
            errors.append(f"Scene {scene.segment_number} missing script")
        if not scene.image_prompt.strip():
            errors.append(f"Scene {scene.segment_number} missing image prompt")
        if not scene.video_prompt.strip():
            errors.append(f"Scene {scene.segment_number} missing video prompt")

    if not scenes:
        errors.append("No scenes parsed from storyboard")

    return errors
