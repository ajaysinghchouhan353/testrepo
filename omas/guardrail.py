from pathlib import Path
import cv2
from PIL import Image
from omas.models import AssetMode


class ValidationError(Exception):
    pass


def validate_asset(path: Path, mode: AssetMode) -> None:
    if not path.exists():
        raise ValidationError("Output file missing")

    if mode == AssetMode.IMAGE:
        if path.suffix.lower() != ".jpg":
            raise ValidationError("Image must be .jpg")
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            if img.width < 512 or img.height < 512:
                raise ValidationError("Image resolution too low")
    else:
        if path.suffix.lower() != ".mp4":
            raise ValidationError("Video must be .mp4")
        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            raise ValidationError("Video not readable")
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        if frames <= 0:
            raise ValidationError("Video has no frames")
        if width < 320 or height < 180:
            raise ValidationError("Video resolution too low")
