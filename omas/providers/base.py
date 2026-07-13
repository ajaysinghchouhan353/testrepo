from abc import ABC, abstractmethod
from pathlib import Path


class ProviderPlugin(ABC):
    name: str

    @abstractmethod
    async def generate_image(self, prompt: str, output_path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    async def generate_video(self, prompt: str, output_path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def provider_information(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def capability_detection(self) -> dict:
        raise NotImplementedError
