"""
SFV ENGINE — INGEST SCRIPT v2
Fixes: config loader, correct duplicate/quarantine behavior,
       lazy MD5 index, correct naming convention, dry-run without media.

USAGE:
    python ingest.py --branch STUDIO --tag MORNINGWALK
    python ingest.py --branch EVENTS --tag SHAMAR --date 20260606
    python ingest.py --branch STUDIO --source staging --tag MORNINGWALK
    python ingest.py --branch STUDIO --dry-run   ← validates paths, no media needed

ARGUMENTS:
    --branch    Required. MYTHOLOGY|SFV_LIVE|SFV_EVENTS|SFV_ATHLETICS|
                          SFV_STUDIO|SFV_UGC|SFV_ARCHIVE|SFV_WORLD|SFV_404
    --tag       Required for production. Event or client label. e.g. MORNINGWALK
    --source    auto=detect E:\\ | staging=process INGEST_STAGING | [path]
    --date      YYYYMMDD [default: today]
    --dry-run   Validate paths and config. No files moved. No media required.

NAMING OUTPUT:
    STUDIO_20260528_MORNINGWALK_0001_RAW.ARW
    STUDIO_20260528_MORNINGWALK_0002_RAW.ARW

SPEC: C:\\SFV_BLUEPRINT\\04_WORKFLOWS\\INGEST.md
"""

import argparse
import hashlib
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
CONFIG_FILE = VAULT / "03_INFRASTRUCTURE" / "ENVIRONMENT_CONFIG.md"

VALID_BRANCHES = {
    "MYTHOLOGY", "SFV_LIVE", "SFV_EVENTS", "SFV_ATHLETICS",
    "SFV_STUDIO", "SFV_UGC", "SFV_ARCHIVE", "SFV_WORLD", "SFV_404",
}

MEDIA_EXTENSIONS = {
    ".arw", ".cr2", ".cr3", ".nef", ".orf", ".rw2", ".dng", ".raw",
    ".jpg", ".jpeg", ".png", ".heic",
    ".mp4", ".mov", ".mts", ".m2ts", ".avi", ".mkv",
}

MAX_WORKERS = 6


# ── CONFIG LOADER ─────────────────────────────────────────────────────────────
def load_config() -> dict:
    """Parse ENVIRONMENT_CONFIG.md and return path variables as a dict."""
    config = {}
    if not CONFIG_FILE.exists():
        print(f"  WARN: Config not found at {CONFIG_FILE}. Using defaults.")
        return config
    in_block = False
    for line in CONFIG_FILE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_block = not in_block
            continue
        if not in_block:
            continue
        if "=" in s and not s.startswith("#"):
            key, _, val = s.partition("=")
            config[key.strip()] = val.strip()
    return config


def resolve_paths(config: dict) -> dict:
    active    = Path(config.get("ACTIVE_STORAGE", r"D:\SFV_ACTIVE"))
    field_ssd = Path(config.get("FIELD_INGEST",    r"E:\\"))
    return {
        "ACTIVE":     active,
        "BRANCHES":   active / "BRANCHES",
        "STAGING":    active / "INGEST_STAGING",
        "QUARANTINE": active / "FOR_HUMAN_REVIEW" / "QUARANTINE",
        "REVIEW":     active / "FOR_HUMAN_REVIEW",
        "FIELD_SSD":  field_ssd,
    }


# ── CHECKSUM ──────────────────────────────────────────────────────────────────
def md5(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while data := f.read(chunk):
            h.update(data)
    return h.hexdigest()


# ── LAZY DUPLICATE INDEX ──────────────────────────────────────────────────────
def build_size_index(branch_ingest_root: Path) -> dict[int, list[Path]]:
    """
    Build a size→[paths] index of existing ingested files.
    Cheap O(n) stat walk. MD5 only computed on collision candidates.
    """
    index: dict[int, list[Path]] = {}
    if not branch_ingest_root.exists():
        return index
    print("  Building size index of existing files...", end="\r")
    count = 0
    for f in branch_ingest_root.rglob("*"):
        if f.is_file():
            sz = f.stat().st_size
            index.setdefault(sz, []).append(f)
            count += 1
    print(f"  Size index built: {count} existing files indexed.          ")
    return index


def is_exact_duplicate(src: Path, size_index: dict) -> bool:
    """
    True if src is an exact duplicate of any existing file.
    Only computes MD5 when file size matches an existing file.
    """
    sz = src.stat().st_size
    candidates = size_index.get(sz, [])
    if not candidates:
        return False
    src_hash = md5(src)
    for candidate in candidates:
        try:
            if md5(candidate) == src_hash:
                return True
        except Exception:
            pass
    return False


def is_near_duplicate(src: Path, staged: Path, size_index: dict) -> bool:
    """
    Near-duplicate: same filename stem exists but different hash.
    Flags for human review without blocking ingest.
    """
    sz = src.stat().st_size
    for existing_files in size_index.values():
        for ef in existing_files:
            if ef.stem.endswith(src.stem) or src.stem in ef.stem:
                try:
                    if md5(ef) != md5(staged):
                        return True
                except Exception:
                    pass
    return False



# ── NAMING ────────────────────────────────────────────────────────────────────
def build_name(branch: str, date: str, tag: str, seq: int, suffix: str) -> str:
    """
    Follows NAMING_CONVENTIONS.md RAW format:
    [BRANCH]_[YYYYMMDD]_[EVENT/CLIENT]_[####]_RAW.[ext]
    e.g. STUDIO_20260528_MORNINGWALK_0001_RAW.arw
    """
    tag_part = f"_{tag.upper()}" if tag else ""
    return f"{branch}_{date}{tag_part}_{seq:04d}_RAW{suffix.lower()}"


# ── SOURCE ────────────────────────────────────────────────────────────────────
def detect_source(source_arg: str, paths: dict) -> Path | None:
    if source_arg == "auto":
        field = paths["FIELD_SSD"]
        if field.exists():
            return field
        return None  # dry-run handles None gracefully
    elif source_arg == "staging":
        return paths["STAGING"]
    else:
        p = Path(source_arg)
        if p.exists():
            return p
        return None


def collect_files(source: Path) -> list[Path]:
    if source is None:
        return []
    return [
        f for f in source.rglob("*")
        if f.is_file() and f.suffix.lower() in MEDIA_EXTENSIONS
    ]


# ── COPY ONE FILE ─────────────────────────────────────────────────────────────
def copy_and_verify(src: Path, dst: Path) -> tuple[bool, str]:
    try:
        shutil.copy2(src, dst)
        if md5(src) != md5(dst):
            return False, f"Checksum mismatch"
        return True, ""
    except Exception as e:
        return False, str(e)


# ── DRY RUN VALIDATION ────────────────────────────────────────────────────────
def dry_run_validate(branch: str, date: str, tag: str, paths: dict, source: Path | None):
    print("\n DRY RUN — validating configuration only. No files moved.\n")
    ok = True

    checks = [
        (paths["ACTIVE"],   "Active storage (D:\\SFV_ACTIVE)"),
        (paths["BRANCHES"], "Branches root"),
        (VAULT / "03_INFRASTRUCTURE" / "ENVIRONMENT_CONFIG.md", "ENVIRONMENT_CONFIG.md"),
    ]
    for path, label in checks:
        status = "✓" if path.exists() else "✗ NOT FOUND"
        print(f"  {status}  {label}: {path}")
        if "✗" in status:
            ok = False

    dest = paths["BRANCHES"] / branch / "INGEST" / date
    print(f"\n  Destination would be: {dest}")
    print(f"  Rename format would be: {build_name(branch, date, tag, 1, '.arw')}")

    if source is None:
        print(f"\n  Source: E:\\ not connected — no files to count (expected in dry run)")
    else:
        files = collect_files(source)
        print(f"\n  Source: {source}")
        print(f"  Media files found: {len(files)}")

    print(f"\n  Config loaded from: {CONFIG_FILE}")
    print(f"  {'All paths OK' if ok else 'ISSUES FOUND — fix before live run'}\n")
    return ok



# ── MAIN RUN ──────────────────────────────────────────────────────────────────
def run(branch: str, date: str, tag: str, source_arg: str, dry_run: bool):
    config = load_config()
    paths  = resolve_paths(config)
    source = detect_source(source_arg, paths)

    print(f"\n SFV INGEST v2")
    print(f" Branch  : {branch}")
    print(f" Tag     : {tag or '(none)'}")
    print(f" Date    : {date}")
    print(f" Source  : {source_arg} → {source or 'not connected'}")
    print(f" Config  : {CONFIG_FILE.name}\n")

    if dry_run:
        dry_run_validate(branch, date, tag, paths, source)
        return

    files = collect_files(source)
    if not files:
        print(f" No media files found in {source}. Nothing to do.")
        sys.exit(0)
    print(f" Found: {len(files)} media files")

    dest_root   = paths["BRANCHES"] / branch / "INGEST" / date
    log_dir     = paths["BRANCHES"] / branch / "LOGS"
    staging_dir = paths["STAGING"] / f"{date}_{branch}_PENDING"
    quarantine  = paths["QUARANTINE"]

    dest_root.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    staging_dir.mkdir(parents=True, exist_ok=True)
    quarantine.mkdir(parents=True, exist_ok=True)

    size_index = build_size_index(paths["BRANCHES"] / branch / "INGEST")

    # tracking
    copied      = []
    failed      = []
    duplicates  = []
    near_dups   = []
    quarantined = []
    renamed     = {}
    ts_start    = datetime.now()

    # ── PARALLEL COPY TO STAGING ──────────────────────────────────────────────
    print(f"\n Copying {len(files)} files to staging...\n")

    def copy_task(src: Path) -> dict:
        dst = staging_dir / src.name
        # Skip if exact duplicate before copying
        if is_exact_duplicate(src, size_index):
            return {"src": src, "status": "duplicate"}
        ok, err = copy_and_verify(src, dst)
        if not ok:
            return {"src": src, "dst": dst, "status": "checksum_fail", "err": err}
        return {"src": src, "dst": dst, "status": "ok"}

    staged = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(copy_task, f): f for f in files}
        done = 0
        for future in as_completed(futures):
            done += 1
            r = future.result()
            bar = "█" * int(40 * done / len(files)) + "░" * (40 - int(40 * done / len(files)))
            print(f"\r  [{bar}] {done}/{len(files)}", end="", flush=True)

            if r["status"] == "ok":
                staged.append(r)
            elif r["status"] == "duplicate":
                duplicates.append(r["src"])
            elif r["status"] == "checksum_fail":
                # Quarantine the bad copy, leave original on source
                dst = r.get("dst")
                if dst and dst.exists():
                    q_dst = quarantine / dst.name
                    shutil.move(str(dst), q_dst)
                    quarantined.append(r["src"])
                failed.append((r["src"], r.get("err", "checksum mismatch")))
    print()

    # ── NEAR-DUPLICATE CHECK ──────────────────────────────────────────────────
    print(f"\n Checking near-duplicates...")
    clean_staged = []
    for r in staged:
        if is_near_duplicate(r["src"], r["dst"], size_index):
            near_dst = paths["REVIEW"] / r["dst"].name
            shutil.move(str(r["dst"]), near_dst)
            near_dups.append(r["src"])
            print(f"  NEAR-DUP → FOR_HUMAN_REVIEW: {r['src'].name}")
        else:
            clean_staged.append(r)

    # ── RENAME + MOVE TO DEST ─────────────────────────────────────────────────
    print(f"\n Renaming and moving {len(clean_staged)} files to branch folder...")
    for seq, r in enumerate(clean_staged, 1):
        new_name = build_name(branch, date, tag, seq, r["src"].suffix)
        final    = dest_root / new_name
        renamed[r["src"].name] = new_name
        try:
            shutil.move(str(r["dst"]), final)
            copied.append(final)
            # Add to size index so next files in this batch check against it
            size_index.setdefault(final.stat().st_size, []).append(final)
        except Exception as e:
            failed.append((r["src"], str(e)))

    # Clean empty staging dir
    try:
        if staging_dir.exists() and not any(staging_dir.iterdir()):
            staging_dir.rmdir()
    except Exception:
        pass

    # ── LOG ───────────────────────────────────────────────────────────────────
    ts_end  = datetime.now()
    elapsed = (ts_end - ts_start).seconds
    mins, secs = divmod(elapsed, 60)

    log_lines = [
        f"INGEST LOG — {branch} — {date}",
        "=" * 44,
        f"Tag      : {tag or '(none)'}",
        f"Source   : {source}",
        f"Start    : {ts_start.strftime('%H:%M:%S')}",
        f"End      : {ts_end.strftime('%H:%M:%S')}",
        f"Duration : {mins}m {secs}s",
        "",
        f"INGESTED        : {len(copied)}",
        f"EXACT DUPES     : {len(duplicates)}  (skipped — originals untouched on source)",
        f"NEAR-DUPES      : {len(near_dups)}  (moved to FOR_HUMAN_REVIEW)",
        f"QUARANTINED     : {len(quarantined)}  (checksum failure — originals on source)",
        f"FAILED          : {len(failed)}",
        f"DESTINATION     : {dest_root}",
        "",
    ]
    if duplicates:
        log_lines += ["EXACT DUPLICATES (skipped):"] + [f"  {d.name}" for d in duplicates] + [""]
    if near_dups:
        log_lines += ["NEAR-DUPLICATES (FOR_HUMAN_REVIEW):"] + [f"  {d.name}" for d in near_dups] + [""]
    if quarantined:
        log_lines += ["QUARANTINED (checksum fail):"] + [f"  {d.name}" for d in quarantined] + [""]
    if failed:
        log_lines += ["ERRORS:"] + [f"  {s.name} — {e}" for s, e in failed] + [""]
    log_lines += ["RENAMED:"] + [f"  {o} → {n}" for o, n in renamed.items()]

    log_path = log_dir / f"INGEST_LOG_{date}_{branch}.txt"
    log_path.write_text("\n".join(log_lines), encoding="utf-8")

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    print(f"\n{'=' * 50}")
    print(f" INGEST COMPLETE — {branch}")
    print(f" {len(copied)} ingested | {len(duplicates)} dupes | {len(near_dups)} near-dupes | {len(failed)} failed")
    print(f" Duration: {mins}m {secs}s")
    print(f" Log: {log_path}")
    if failed or quarantined:
        print(f"\n ATTENTION: check log and FOR_HUMAN_REVIEW folder.")
    print(f"{'=' * 50}\n")


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="SFV Engine — Ingest v2")
    p.add_argument("--branch",   required=True)
    p.add_argument("--tag",      default="",    help="Event or client label, e.g. MORNINGWALK")
    p.add_argument("--source",   default="auto", help="auto | staging | /path/to/folder")
    p.add_argument("--date",     default=datetime.now().strftime("%Y%m%d"))
    p.add_argument("--dry-run",  action="store_true")
    args = p.parse_args()

    branch = args.branch.upper()
    if branch not in VALID_BRANCHES:
        print(f" ERROR: '{branch}' not valid. Options: {', '.join(sorted(VALID_BRANCHES))}")
        sys.exit(1)

    run(branch, args.date, args.tag.upper(), args.source, args.dry_run)


if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[ENVIRONMENT_CONFIG|Environment Configuration]]
# - [[MEDIA_TYPES|Media Types Specification]]
# - [[BRANCH_DEFINITIONS|Branch Definitions]]
# - [[INGEST|Ingest Workflow Specification]]
# - [[NAMING_CONVENTIONS|File Naming Conventions]]
# - [[README|Project Overview]]
