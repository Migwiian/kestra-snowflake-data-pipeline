import os
from pathlib import Path

# Upload raw CSVs to an S3-compatible data lake (S3/MinIO).

RAW_DIR = Path(os.getenv("RAW_DIR", "data/raw"))
BUCKET = os.getenv("LAKE_BUCKET", "olist-lake")
PREFIX = os.getenv("LAKE_PREFIX", "olist/raw")
ENDPOINT_URL = os.getenv("LAKE_ENDPOINT")
ACCESS_KEY = os.getenv("LAKE_ACCESS_KEY")
SECRET_KEY = os.getenv("LAKE_SECRET_KEY")
REGION = os.getenv("LAKE_REGION", "us-east-1")


def main() -> None:
    try:
        import boto3
    except ImportError as exc:
        raise SystemExit("Missing dependency: boto3. Install with `pip install boto3`.") from exc

    if not RAW_DIR.exists():
        raise SystemExit(f"Raw directory not found: {RAW_DIR}")

    session = boto3.session.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )
    s3 = session.resource("s3", endpoint_url=ENDPOINT_URL)
    bucket = s3.Bucket(BUCKET)

    for path in RAW_DIR.glob("*.csv"):
        key = f"{PREFIX}/{path.name}"
        bucket.upload_file(str(path), key)
        print(f"Uploaded {path} -> s3://{BUCKET}/{key}")


if __name__ == "__main__":
    main()
