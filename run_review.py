"""Read the proposed change and run `schemasafe github-report` (read-only, synthetic fixtures)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ENGINES = {"mongodb", "couchdb", "cassandra"}


def main() -> int:
    change: dict[str, str] = {}
    change_file = Path(os.environ.get("INPUT_CHANGE_FILE") or "schema-change.json")
    if change_file.is_file():
        change = json.loads(change_file.read_text(encoding="utf-8"))
    for key in ("engine", "resource", "operation", "field", "target_type"):
        override = os.environ.get(f"INPUT_{key.upper()}", "").strip()
        if override:
            change[key] = override

    engine = str(change.get("engine", "")).strip()
    operation = str(change.get("operation", "")).strip()
    if engine not in ENGINES or not operation:
        print(
            f"::error::Indica engine (mongodb, couchdb o cassandra) y operation en {change_file} "
            "o como entradas de la Action."
        )
        return 2
    pr_number = os.environ.get("INPUT_PR_NUMBER", "").strip()
    if not pr_number:
        print("::error::No hay pull request: usa la Action en un evento pull_request o pasa pr-number.")
        return 2
    dry_run = os.environ.get("INPUT_DRY_RUN", "").strip().lower() == "true"
    if not dry_run and not os.environ.get("GITHUB_TOKEN"):
        print("::error::Falta el token. Deja github-token en su valor por defecto (GITHUB_TOKEN).")
        return 2

    command = [
        "schemasafe", "github-report",
        "--engine", engine,
        "--resource", str(change.get("resource") or "demo"),
        "--operation", operation,
        "--field", str(change.get("field") or ""),
        "--pr", pr_number,
    ]
    if change.get("target_type"):
        command += ["--target-type", str(change["target_type"])]
    if dry_run:
        command.append("--dry-run")
    print("Ejecutando:", " ".join(command))
    return subprocess.call(command)


if __name__ == "__main__":
    sys.exit(main())
