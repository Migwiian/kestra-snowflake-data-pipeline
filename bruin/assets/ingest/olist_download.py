import os
from pathlib import Path

# Optional Kaggle download helper.
# This script expects KAGGLE_USERNAME and KAGGLE_KEY to be set.

DATASET = os.getenv("KAGGLE_DATASET", "olistbr/brazilian-ecommerce")
TARGET_DIR = Path(os.getenv("KAGGLE_DOWNLOAD_DIR", "data/raw"))


def main() -> None:
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError as exc:
        raise SystemExit("Missing dependency: kaggle. Install with `pip install kaggle`.") from exc

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(DATASET, path=str(TARGET_DIR), unzip=True)

    print(f"Downloaded {DATASET} to {TARGET_DIR}")


if __name__ == "__main__":
    main()
