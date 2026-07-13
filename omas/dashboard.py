import gradio as gr
from omas.config import settings
from omas.models import AssetMode
from omas.studio import OMASStudio


studio = OMASStudio(settings)


def validate():
    scenes, errors = studio.load_storyboard()
    return {
        "total_scenes": len(scenes),
        "errors": errors,
    }


def run_generation(mode: str):
    return studio.generate_sync(AssetMode(mode))


with gr.Blocks(title="OMAS Dashboard") as demo:
    gr.Markdown("# Ownership Manual AI Studio (OMAS)")
    gr.Markdown(f"Storyboard: `{settings.project_root / settings.storyboard_file}`")
    mode = gr.Dropdown(choices=["image", "video"], value="image", label="Mode")
    validate_btn = gr.Button("Validate Storyboard")
    generate_btn = gr.Button("Run Generation")
    output = gr.JSON(label="Result")

    validate_btn.click(fn=validate, inputs=[], outputs=[output])
    generate_btn.click(fn=run_generation, inputs=[mode], outputs=[output])


if __name__ == "__main__":
    demo.launch()
