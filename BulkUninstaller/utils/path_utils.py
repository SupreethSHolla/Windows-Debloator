from pathlib import Path


def resolve_project_path(*parts):
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir.joinpath(*parts)
