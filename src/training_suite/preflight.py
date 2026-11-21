"""Dataset preflight checks before launching YOLO26/YOLO11 training."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass
class PreflightReport:
    long_filenames: List[str]
    zero_val_classes: List[str]
    out_of_bounds_boxes: int
    case_collisions: List[Tuple[str, str]]


def check_filename_lengths(filenames: Sequence[str], max_len: int = 190) -> List[str]:
    """Guard against ext4 255-byte limits when temp suffixes are appended."""
    return [fn for fn in filenames if len(fn.encode("utf-8")) > max_len]


def find_zero_val_classes(train_counts: Dict[str, int], val_counts: Dict[str, int]) -> List[str]:
    """Return classes that appear in train but have zero boxes in validation."""
    return [cls for cls, cnt in train_counts.items() if cnt > 0 and val_counts.get(cls, 0) == 0]


def clamp_yolo_bbox(cx: float, cy: float, w: float, h: float) -> Tuple[float, float, float, float]:
    """Clamp normalized YOLO coordinates to valid [0, 1] range."""
    x1 = max(0.0, min(1.0, cx - w / 2.0))
    y1 = max(0.0, min(1.0, cy - h / 2.0))
    x2 = max(0.0, min(1.0, cx + w / 2.0))
    y2 = max(0.0, min(1.0, cy + h / 2.0))
    nw = max(0.0, x2 - x1)
    nh = max(0.0, y2 - y1)
    return (x1 + nw / 2.0, y1 + nh / 2.0, nw, nh)


def find_case_collisions(class_names: Iterable[str]) -> List[Tuple[str, str]]:
    """Detect class duplicates differing only by letter case or outer whitespace."""
    seen: Dict[str, str] = {}
    collisions: List[Tuple[str, str]] = []
    for name in class_names:
        key = name.strip().lower()
        if key in seen and seen[key] != name:
            collisions.append((seen[key], name))
        else:
            seen[key] = name
    return collisions


def split_dataset_70_20_10(item_ids: Sequence[str], seed: int = 42) -> Dict[str, List[str]]:
    """Deterministic zero-leakage 70/20/10 train/val/test split."""
    ids = list(item_ids)
    random.Random(seed).shuffle(ids)
    n = len(ids)
    n_train = int(n * 0.70)
    n_val = int(n * 0.20)
    return {
        "train": ids[:n_train],
        "val": ids[n_train : n_train + n_val],
        "test": ids[n_train + n_val :],
    }
