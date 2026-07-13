from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw
from omas.providers.base import ProviderPlugin


class GeminiProvider(ProviderPlugin):
    name = "gemini"

    async def generate_image(self, prompt: str, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (1280, 720), color=(28, 32, 40))
        draw = ImageDraw.Draw(img)
        draw.rectangle([20, 20, 1260, 700], outline=(255, 255, 255), width=2)
        draw.text((40, 40), prompt[:120], fill=(255, 255, 255))
        img.save(output_path, format="JPEG", quality=95)

    async def generate_video(self, prompt: str, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        width, height = 640, 360
        fps = 12
        duration_seconds = 2
        writer = cv2.VideoWriter(
            str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )
        if not writer.isOpened():
            raise RuntimeError("Unable to initialize video writer")

        for i in range(fps * duration_seconds):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            intensity = min(255, i * 8)
            frame[:, :, :] = (intensity // 3, intensity // 2, intensity)
            cv2.putText(
                frame,
                prompt[:40],
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            writer.write(frame)

        writer.release()

    async def health_check(self) -> bool:
        return True

    def provider_information(self) -> dict:
        return {"name": self.name, "type": "mock", "version": "v1"}

    def capability_detection(self) -> dict:
        return {"image": True, "video": True}
