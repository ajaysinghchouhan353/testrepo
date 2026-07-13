# Ownership Manual AI Studio (OMAS)

OMAS is a provider-agnostic automation platform that converts storyboard segments into one visual asset per scene.

## Implemented Milestones (v1 baseline)

- Project scaffold, configuration, logging, and storyboard parser
- Scene validation and strict numbering rules
- Provider plugin architecture with initial Gemini/Gemini Veo-compatible mock providers
- Queue engine with parallel workers, retries, and resume behavior
- Continuity engine and prompt builder with cinematic constraints
- Generation guardrails for image/video output validation
- SQLite persistence schema for projects/scenes/jobs/providers/outputs/retries/logs/continuity/settings
- FastAPI backend and Gradio dashboard
- Docker packaging and GitHub Actions CI
- Pytest test suite for parser, validator, output naming/resume, and studio flow

## Quickstart

```bash
pip install -e .[test]
pytest -q
uvicorn omas.main:app --reload
python -m omas.dashboard
```

## Storyboard format

```text
Segment 1
Script:
...
Image Prompt:
...
Video Prompt:
...
```

## Core guarantee

- One scene in → one asset out
- Image: `N.jpg`
- Video: `N.mp4`
