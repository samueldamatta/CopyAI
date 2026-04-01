from pathlib import Path

import yaml
from agents import Agent

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(filename: str) -> str:
    with open(_PROMPTS_DIR / filename) as f:
        return yaml.safe_load(f)["instructions"]


def make_copywriter_agent(model: str = "gpt-4o") -> Agent:
    return Agent(
        name="Copywriter",
        instructions=_load_prompt("copywriter.yml"),
        model=model,
    )


def make_title_agent() -> Agent:
    return Agent(
        name="TitleGenerator",
        instructions=_load_prompt("title_generator.yml"),
        model="gpt-4o-mini",
    )
