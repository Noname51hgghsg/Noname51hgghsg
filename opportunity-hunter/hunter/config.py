"""Configuration loading."""
from __future__ import annotations

import copy
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_config(path: Path | None = None, overrides: dict | None = None) -> dict:
    path = path or ROOT / "config.toml"
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    if overrides:
        cfg = deep_merge(cfg, overrides)
    return cfg


def deep_merge(base: dict, extra: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in extra.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out
