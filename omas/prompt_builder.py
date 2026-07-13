from omas.continuity import ContinuityEngine
from omas.models import AssetMode, Scene

QUALITY_SUFFIX = (
    "Cinematic documentary, ultra realistic, photorealistic, HDR, film lighting, "
    "natural color grading, professional composition, sharp focus, maintain continuity, "
    "exactly one image, no storyboard, no collage, no comic strip, no contact sheet, "
    "no watermark, no text."
)


def build_prompt(scene: Scene, mode: AssetMode, continuity: ContinuityEngine) -> str:
    base = scene.image_prompt if mode == AssetMode.IMAGE else scene.video_prompt
    continuity_text = continuity.continuity_suffix()
    if continuity_text:
        return f"{base}\n\n{QUALITY_SUFFIX} {continuity_text}"
    return f"{base}\n\n{QUALITY_SUFFIX}"
