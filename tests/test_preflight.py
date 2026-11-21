from training_suite.preflight import (
    check_filename_lengths,
    clamp_yolo_bbox,
    find_case_collisions,
    find_zero_val_classes,
    split_dataset_70_20_10,
)


def test_split_70_20_10_disjoint():
    ids = [f"img_{i}" for i in range(100)]
    sp = split_dataset_70_20_10(ids, seed=42)
    assert len(sp["train"]) == 70
    assert len(sp["val"]) == 20
    assert len(sp["test"]) == 10
    assert len(set(sp["train"]) | set(sp["val"]) | set(sp["test"])) == 100


def test_zero_val_class_detection():
    zero = find_zero_val_classes({"chair": 400, "bookcase": 15}, {"chair": 80, "bookcase": 0})
    assert zero == ["bookcase"]


def test_case_collision_detection():
    cols = find_case_collisions(["Forklift", "forklift", "Pallet"])
    assert cols == [("Forklift", "forklift")]


def test_clamp_yolo_bbox():
    cx, cy, w, h = clamp_yolo_bbox(0.95, 0.5, 0.2, 0.4)
    assert cx + w / 2.0 <= 1.0 + 1e-9
    assert len(check_filename_lengths(["a" * 200, "short.jpg"])) == 1
