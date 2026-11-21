"""Domain-tailored hyperparameter selector loading configs/*.yaml."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Sequence
import yaml


def load_recipe_yaml(config_name: str, configs_dir: Path | None = None) -> Dict:
    base = configs_dir or (Path(__file__).resolve().parents[2] / "configs")
    return yaml.safe_load((base / config_name).read_text(encoding="utf-8"))


def select_config_name(dataset_name: str, class_names: Sequence[str]) -> str:
    text = (dataset_name + " " + " ".join(class_names)).lower()
    if any(k in text for k in ["levha", "sign", "plaka", "plate", "hız", "speed", "rakam", "digit"]):
        return "traffic_signs.yaml"
    if any(k in text for k in ["iha", "uav", "drone", "apron", "aerial", "hava"]):
        return "uav_aerial.yaml"
    if any(k in text for k in ["röntgen", "xray", "x-ray", "mri", "ct", "dental", "diş"]):
        return "medical_grayscale.yaml"
    return "industrial_ppe.yaml"
