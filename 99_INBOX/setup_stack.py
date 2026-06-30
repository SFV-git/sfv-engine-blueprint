"""
SFV ENGINE — STACK SETUP SCRIPT
Builds the full branch folder structure on the active storage drive.
Run ONCE after confirming drive letter.

USAGE:
    python C:\SFV_BLUEPRINT\99_INBOX\setup_stack.py --drive D

WHAT IT BUILDS:
    [DRIVE]:\SFV_ACTIVE\
        BRANCHES\
            MYTHOLOGY\      INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_LIVE\       INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_EVENTS\     INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_ATHLETICS\  INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_STUDIO\     INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_UGC\        INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_ARCHIVE\    INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_WORLD\      INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
            SFV_404\        INGEST\ EDIT\ EXPORT\ ARCHIVE\ LOGS\
        INGEST_STAGING\
        DELIVERY_STAGING\
        FOR_HUMAN_REVIEW\
        LOGS\

RULES:
    - Never deletes anything
    - Never overwrites anything
    - Only creates folders that don't exist
    - Reports every action
    - Will is final authority — review output before trusting it
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

BRANCHES = [
    "MYTHOLOGY",
    "SFV_LIVE",
    "SFV_EVENTS",
    "SFV_ATHLETICS",
    "SFV_STUDIO",
    "SFV_UGC",
    "SFV_ARCHIVE",
    "SFV_WORLD",
    "SFV_404",
]

BRANCH_SUBFOLDERS = [
    "INGEST",
    "EDIT",
    "EXPORT",
    "ARCHIVE",
    "LOGS",
]

ROOT_FOLDERS = [
    "INGEST_STAGING",
    "DELIVERY_STAGING",
    "FOR_HUMAN_REVIEW",
    "LOGS",
]


def build_structure(drive: str, dry_run: bool = False):
    root = Path(f"{drive}:\\SFV_ACTIVE")
    branches_root = root / "BRANCHES"

    created = []
    skipped = []

    def make(path: Path):
        if path.exists():
            skipped.append(str(path))
        else:
            if not dry_run:
                path.mkdir(parents=True, exist_ok=True)
            created.append(str(path))

    print(f"\n SFV ENGINE — STACK SETUP")
    print(f" Drive: {drive}:\\")
    print(f" Root: {root}")
    if dry_run:
        print(f" MODE: DRY RUN — no folders will be created\n")
    else:
        print(f" MODE: LIVE — folders will be created\n")

    # Root level
    make(root)
    make(branches_root)

    # Root utility folders
    for folder in ROOT_FOLDERS:
        make(root / folder)

    # Branch folders
    for branch in BRANCHES:
        branch_path = branches_root / branch
        make(branch_path)
        for sub in BRANCH_SUBFOLDERS:
            make(branch_path / sub)

    # Report
    print(f" CREATED ({len(created)}):")
    for p in created:
        print(f"   + {p}")

    if skipped:
        print(f"\n SKIPPED — already exist ({len(skipped)}):")
        for p in skipped:
            print(f"   = {p}")

    # Write log to vault
    log_path = Path(r"C:\SFV_BLUEPRINT\LOGS") if Path(r"C:\SFV_BLUEPRINT\LOGS").exists() else Path(r"C:\SFV_BLUEPRINT\99_INBOX")
    log_file = log_path / f"SETUP_LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    if not dry_run:
        log_file.write_text(
            f"SFV STACK SETUP LOG\n"
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Drive: {drive}:\\\n"
            f"Root: {root}\n\n"
            f"CREATED ({len(created)}):\n" + "\n".join(f"  + {p}" for p in created) +
            f"\n\nSKIPPED ({len(skipped)}):\n" + "\n".join(f"  = {p}" for p in skipped),
            encoding="utf-8"
        )
        print(f"\n Log written: {log_file}")

    print(f"\n Done. {len(created)} folders created, {len(skipped)} already existed.")
    if dry_run:
        print(f" Run without --dry-run to create them for real.")


def main():
    parser = argparse.ArgumentParser(description="SFV Engine — Stack Setup")
    parser.add_argument("--drive", required=True, help="Drive letter for 5TB Seagate (e.g. D)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only — no folders created")
    args = parser.parse_args()

    drive = args.drive.upper().rstrip(":\\")
    if len(drive) != 1 or not drive.isalpha():
        print(f"ERROR: Invalid drive letter '{drive}'. Use single letter like D or E.")
        sys.exit(1)

    if not Path(f"{drive}:\\").exists():
        print(f"ERROR: Drive {drive}:\\ not found. Check File Explorer.")
        sys.exit(1)

    print(f"\n Drive {drive}:\\ found.")

    if not args.dry_run:
        confirm = input(f" Create SFV folder structure on {drive}:\\? (yes/no): ").strip().lower()
        if confirm != "yes":
            print(" Cancelled.")
            sys.exit(0)

    build_structure(drive, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[ARCHITECTURE_AUDIT|Architecture Audit]]
# - [[SOURCE_OF_TRUTH_RULES|Source of Truth Rules]]
# - [[PROPOSALS|Proposals]]
# - [[CURRENT_DIRECTIVE|Current Directive]]
# - [[MASTER_CONTEXT|Master Context]]
