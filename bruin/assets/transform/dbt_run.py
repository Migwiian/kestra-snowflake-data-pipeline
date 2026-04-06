import os
import subprocess
from pathlib import Path

# Optional dbt execution for transformations.

PROJECT_DIR = Path(os.getenv("DBT_PROJECT_DIR", "dbt"))
PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")


def main() -> None:
    if not PROJECT_DIR.exists():
        raise SystemExit(f"dbt project not found: {PROJECT_DIR}")

    cmd = ["dbt", "run", "--project-dir", str(PROJECT_DIR)]
    if PROFILES_DIR:
        cmd.extend(["--profiles-dir", PROFILES_DIR])

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
