"""Loads agent definitions from agents/*/agent.toml and validators/*/agent.toml."""
from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .config import ROOT


@dataclass
class AgentSpec:
    name: str
    display: str
    stage: str
    schema_name: str
    prompt_path: Path
    tools: list[str] = field(default_factory=lambda: ["WebSearch", "WebFetch"])
    max_searches: int = 10
    max_fetches: int = 6
    max_turns: int = 45
    max_budget_usd: float = 3.0
    model: str | None = None
    description: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def schema(self) -> dict:
        return json.loads((ROOT / "schemas" / f"{self.schema_name}.json").read_text(encoding="utf-8"))

    def system_prompt(self, cfg: dict) -> str:
        base = (ROOT / "prompts" / "base_rules.md").read_text(encoding="utf-8")
        own = self.prompt_path.read_text(encoding="utf-8")
        f = cfg.get("founder", {})
        founder = (f"\n\n## Run-time founder context\n- Team: {f.get('team')}\n- Tools: {', '.join(f.get('tools', []))}\n"
                   f"- MVP budget: {f.get('mvp_budget_sar_min')}–{f.get('mvp_budget_sar_max')} SAR\n"
                   f"- Preference: {f.get('preference')}\n")
        return base + founder + "\n\n---\n\n" + own


def load_registry(cfg: dict) -> dict[str, AgentSpec]:
    defaults = cfg.get("limits", {}).get("default", {})
    specs: dict[str, AgentSpec] = {}
    for group in ("agents", "validators"):
        for toml_path in sorted((ROOT / group).glob("*/agent.toml")):
            with open(toml_path, "rb") as f:
                d = tomllib.load(f)
            name = d["name"]
            specs[name] = AgentSpec(
                name=name,
                display=d.get("display", name.upper()),
                stage=d["stage"],
                schema_name=d["schema"],
                prompt_path=toml_path.parent / "prompt.md",
                tools=d.get("tools", ["WebSearch", "WebFetch"]),
                max_searches=d.get("max_searches", defaults.get("max_searches", 10)),
                max_fetches=d.get("max_fetches", defaults.get("max_fetches", 6)),
                max_turns=d.get("max_turns", defaults.get("max_turns", 45)),
                max_budget_usd=d.get("max_budget_usd", defaults.get("max_budget_usd", 3.0)),
                model=d.get("model"),
                description=d.get("description", ""),
                extra={k: v for k, v in d.items() if k not in AgentSpec.__dataclass_fields__},
            )
    return specs
