import re
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = PROJECT_ROOT / "data" / "raw" / "PlantVillage-Dataset-master" / "raw" / "color"
TARGET_ROOT = PROJECT_ROOT / "data" / "dataset"

SPECIAL_MAP = {
    "Apple___Apple_scab": "Apple Scab",
    "Apple___Black_rot": "Apple Black Rot",
    "Apple___Cedar_apple_rust": "Apple Cedar Rust",
    "Apple___healthy": "Apple Healthy",
    "Blueberry___healthy": "Blueberry Healthy",
    "Cherry_(including_sour)___healthy": "Cherry Healthy",
    "Cherry_(including_sour)___Powdery_mildew": "Cherry Powdery Mildew",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Maize Gray Leaf Spot",
    "Corn_(maize)___Common_rust_": "Maize Common Rust",
    "Corn_(maize)___healthy": "Maize Healthy",
    "Corn_(maize)___Northern_Leaf_Blight": "Maize Northern Leaf Blight",
    "Grape___Black_rot": "Grape Black Rot",
    "Grape___Esca_(Black_Measles)": "Grape Esca Black Measles",
    "Grape___healthy": "Grape Healthy",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Grape Leaf Blight",
    "Orange___Haunglongbing_(Citrus_greening)": "Orange Citrus Greening",
    "Peach___Bacterial_spot": "Peach Bacterial Spot",
    "Potato___Early_blight": "Potato Early Blight",
    "Potato___Late_blight": "Potato Late Blight",
    "Potato___healthy": "Potato Healthy",
    "Tomato___Bacterial_spot": "Tomato Bacterial Spot",
    "Tomato___Early_blight": "Tomato Early Blight",
    "Tomato___Late_blight": "Tomato Late Blight",
    "Tomato___Leaf_Mold": "Tomato Leaf Mold",
    "Tomato___Septoria_leaf_spot": "Tomato Septoria Leaf Spot",
    "Tomato___healthy": "Tomato Healthy",
}


def normalize_label(source_name: str) -> str:
    if source_name in SPECIAL_MAP:
        return SPECIAL_MAP[source_name]

    source_name = source_name.replace("___", " ")
    source_name = source_name.replace("_", " ")
    source_name = re.sub(r"\([^)]*\)", "", source_name)
    source_name = re.sub(r"\s+", " ", source_name).strip()
    return source_name.title()


def copy_images(source_dir: Path, target_dir: Path):
    target_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for image_path in source_dir.glob("*"):
        if image_path.is_file():
            shutil.copy2(image_path, target_dir / image_path.name)
            count += 1
    return count


def main():
    if not SOURCE_ROOT.exists():
        raise FileNotFoundError(
            "PlantVillage source dataset not found. Download and extract it into data/raw first."
        )

    total = 0
    copied_classes = 0
    for source_dir in sorted(SOURCE_ROOT.iterdir()):
        if not source_dir.is_dir():
            continue

        target_name = normalize_label(source_dir.name)
        copied = copy_images(source_dir, TARGET_ROOT / target_name)
        total += copied
        copied_classes += 1
        print(f"Copied {copied} images -> {target_name}")

    print(f"Done. Total copied images: {total}")
    print(f"Done. Total classes prepared: {copied_classes}")


if __name__ == "__main__":
    main()
