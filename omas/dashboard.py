import gradio as gr
from pathlib import Path
from omas.config import settings
from omas.models import AssetMode
from omas.studio import OMASStudio


studio = OMASStudio(settings)


def validate(storyboard_path: str):
    scenes, errors = studio.load_storyboard(Path(storyboard_path) if storyboard_path else None)
    return {
        "total_scenes": len(scenes),
        "errors": errors,
    }


def run_generation(storyboard_path: str, mode: str):
    return studio.generate_sync(AssetMode(mode), Path(storyboard_path) if storyboard_path else None)


with gr.Blocks(title="OMAS Dashboard") as demo:
    gr.Markdown("# Ownership Manual AI Studio (OMAS)")
    path = gr.Textbox(label="Storyboard Path", value=str(settings.project_root / settings.storyboard_file))
    mode = gr.Dropdown(choices=["image", "video"], value="image", label="Mode")
    validate_btn = gr.Button("Validate Storyboard")
    generate_btn = gr.Button("Run Generation")
    output = gr.JSON(label="Result")

    validate_btn.click(fn=validate, inputs=[path], outputs=[output])
    generate_btn.click(fn=run_generation, inputs=[path, mode], outputs=[output])


if __name__ == "__main__":
    demo.launch()
