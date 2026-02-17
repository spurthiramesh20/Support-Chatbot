import yaml
from pathlib import Path

PROMPT_PATH = Path(__file__).parent / "prompts" / "support_prompts.yml"

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    PROMPTS = yaml.safe_load(f)
