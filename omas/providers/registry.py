from omas.providers.base import ProviderPlugin
from omas.providers.mock_gemini import GeminiProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderPlugin] = {}
        self.register("gemini", GeminiProvider())
        self.register("gemini_veo", GeminiProvider())

    def register(self, name: str, provider: ProviderPlugin) -> None:
        self._providers[name] = provider

    def get(self, name: str) -> ProviderPlugin:
        if name not in self._providers:
            raise KeyError(f"Provider not registered: {name}")
        return self._providers[name]

    def list_info(self) -> list[dict]:
        return [p.provider_information() for p in self._providers.values()]
