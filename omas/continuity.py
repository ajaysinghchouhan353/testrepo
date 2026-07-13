from dataclasses import dataclass, field
from omas.models import Scene


@dataclass
class ContinuityState:
    characters: set[str] = field(default_factory=set)
    locations: set[str] = field(default_factory=set)
    props: set[str] = field(default_factory=set)
    weather: set[str] = field(default_factory=set)
    lighting: set[str] = field(default_factory=set)


class ContinuityEngine:
    def __init__(self) -> None:
        self.state = ContinuityState()

    def update_from_scene(self, scene: Scene) -> ContinuityState:
        text = f"{scene.script} {scene.image_prompt} {scene.video_prompt}".lower()
        for word in ["rain", "sunset", "night", "day", "studio", "street", "office", "car", "camera"]:
            if word in text:
                if word in {"rain", "sunset", "night", "day"}:
                    self.state.weather.add(word)
                elif word in {"studio", "street", "office"}:
                    self.state.locations.add(word)
                else:
                    self.state.props.add(word)
        return self.state

    def continuity_suffix(self) -> str:
        bits = []
        if self.state.locations:
            bits.append(f"consistent location: {', '.join(sorted(self.state.locations))}")
        if self.state.weather:
            bits.append(f"weather continuity: {', '.join(sorted(self.state.weather))}")
        if self.state.props:
            bits.append(f"props continuity: {', '.join(sorted(self.state.props))}")
        return "; ".join(bits)
