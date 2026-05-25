"""
SFV ENGINE — INGEST SCRIPT v1
Moves files from any source into the correct branch folder safely.

USAGE:
    python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --date 20260528
    python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --source staging
    python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --dry-run

ARGUMENTS:
    --branch    Required. One of: MYTHOLOGY SFV_LIVE SFV_EVENTS SFV_ATHLETICS
                                   SFV_STUDIO SFV_UGC SFV_ARCHIVE SFV_WORLD SFV_404
    --source    auto     = detect E:\\ (SanDisk field SSD) automatically [default]
                staging  = process D:\\SFV_ACTIVE\\INGEST_STAGING\\ contents
                [path]   = explicit folder path
    --date      YYYYMMDD [default: today]
    --dry-run   Preview only. No files moved or renamed.

SPEC: 04_WORKFLOWS/INGEST.md
"""

import argparse
import hashlib
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# ── PATHS ─────────────────────────────────────────────────────────────────────
ACTIVE    = Path(r"D:\SFV_ACTIVE")
BRANCHES  = ACTIVE / "BRANCHES"
STAGING   = ACTIVE / "INGEST_STAGING"
REVIEW    = ACTIVE / "FOR_HUMAN_REVIEW"
FIELD_SSD = Path(r"E:\\")

VALID_BRANCHES = {
    "MYTHOLOGY", "SFV_LIVE", "SFV_EVENTS", "SFV_ATHLETICS",
    "SFV_STUDIO", "SFV_UGC", "SFV_ARCHIVE", "SFV_WORLD", "SFV_404"
}

MEDIA_EXTENSIONS = {
    ".arw", ".cr2", ".cr3", ".nef", ".orf", ".rw2", ".dng", ".raw",
    ".jpg", ".jpeg", ".png", ".heic",
    ".mp4", ".mov", ".mts", ".m2ts", ".avi", ".mkv",
}

MAX_WORKERS = 6  # parallel copy threads

# ── CHECKSUM ──────────────────────────────────────────────────────────────────
def md5(path: Path, chunk=1024 * 1024) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk_data := f.read(chunk):
            h.update(chunk_data)
    return h.hexdigest()

# ── SOURCE DETECTION ──────────────────────────────────────────────────────────
def detect_source(source_arg: str) -> Path:
    if source_arg == "auto":
        if not FIELD_SSD.exists():
            print("  ERROR: E:\\ not found. Plug in SanDisk Extreme SSD.")
            sys.exit(1)
        # Collect all media files from SSD root
        return FIELD_SSD
    elif source_arg == "staging":
        if not STAGING.exists():
            STAGING.mkdir(parents=True)
        return STAGING
    else:
        p = Path(source_arg)
        if not p.exists():
            print(f"  ERROR: Source path not found: {p}")
            sys.exit(1)
        return p

def collect_files(source: Path) -> list[Path]:
    return [
        f for f in source.rglob("*")
        if f.is_file() and f.suffix.lower() in MEDIA_EXTENSIONS
    ]

# ── NAMING ────────────────────────────────────────────────────────────────────
def build_name(branch: str, date: str, seq: int, suffix: str) -> str:
    return f"{branch}_{date}_{seq:04d}{suffix}"

# ── DUPLICATE CHECK ───────────────────────────────────────────────────────────
def build_existing_hashes(branch_ingest_root: Path) -> set[str]:
    existing = set()
    if not branch_ingest_root.exists():
        return existing
    print("  Building duplicate index...", end="\r")
    files = [f for f in branch_ingest_root.rglob("*") if f.is_file()]
    for f in files:
        try:
            existing.add(md5(f))
        except Exception:
            pass
    print(f"  Duplicate index: {len(existing)} existing files scanned.")
    return existing

# ── COPY ONE FILE ─────────────────────────────────────────────────────────────
def copy_and_verify(src: Path, dst: Path) -> tuple[bool, str]:
    """Copy src to dst, verify checksum. Returns (success, error_message)."""
    try:
        shutil.copy2(src, dst)
        src_hash = md5(src)
        dst_hash = md5(dst)
        if src_hash != dst_hash:
            dst.unlink(missing_ok=True)
            return False, f"Checksum mismatch: {src.name}"
        return True, ""
    except Exception as e:
        return False, str(e)

# ── MAIN ──────────────────────────────────────────────────────────────────────
def run(branch: str, date: str, source_arg: str, dry_run: bool):
    ts_start = datetime.now()
    print(f"\n SFV INGEST v1")
    print(f" Branch  : {branch}")
    print(f" Date    : {date}")
    print(f" Source  : {source_arg}")
    print(f" Mode    : {'DRY RUN' if dry_run else 'LIVE'}\n")

    source = detect_source(source_arg)
    files  = collect_files(source)

    if not files:
        print(f" No media files found in {source}")
        sys.exit(0)

    print(f" Found: {len(files)} media files")

    dest_root    = BRANCHES / branch / "INGEST" / date
    log_dir      = BRANCHES / branch / "LOGS"
    staging_dir  = STAGING / f"{date}_{branch}_PENDING"

    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)
        log_dir.mkdir(parents=True, exist_ok=True)
        staging_dir.mkdir(parents=True, exist_ok=True)

    # Build duplicate index
    existing_hashes = build_existing_hashes(BRANCHES / branch / "INGEST")

    # Results tracking
    copied = []
    failed = []
    duplicates = []
    renamed = {}

    # ── PARALLEL COPY TO STAGING ─────────────────────────────────────────────
    print(f"\n Copying {len(files)} files...\n")

    def copy_task(src: Path, idx: int) -> dict:
        stage_dst = staging_dir / src.name
        if dry_run:
            return {"src": src, "idx": idx, "ok": True, "dry": True}
        ok, err = copy_and_verify(src, stage_dst)
        return {"src": src, "idx": idx, "dst": stage_dst, "ok": ok, "err": err}

    staged = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(copy_task, f, i): f for i, f in enumerate(files, 1)}
        done_count = 0
        for future in as_completed(futures):
            done_count += 1
            result = future.result()
            bar_fill = int(40 * done_count / len(files))
            bar = "█" * bar_fill + "░" * (40 - bar_fill)
            print(f"\r  [{bar}] {done_count}/{len(files)}", end="", flush=True)
            if result["ok"]:
                staged[result["src"]] = result.get("dst", result["src"])
            else:
                failed.append((result["src"], result.get("err", "")))
    print()

    # ── DUPLICATE CHECK ──────────────────────────────────────────────────────
    if not dry_run:
        print(f"\n Checking duplicates...")
        clean_staged = {}
        for src, stage_dst in staged.items():
            try:
                h = md5(stage_dst)
                if h in existing_hashes:
                    duplicates.append(src)
                    stage_dst.unlink(missing_ok=True)
                    print(f"  DUPLICATE skipped: {src.name}")
                else:
                    existing_hashes.add(h)
                    clean_staged[src] = (stage_dst, h)
            except Exception as e:
                failed.append((src, str(e)))
    else:
        clean_staged = {src: (dst, "") for src, dst in staged.items()}

    # ── RENAME + MOVE TO DEST ────────────────────────────────────────────────
    print(f"\n Renaming and moving {len(clean_staged)} files...")
    for seq, (src, (stage_dst, _)) in enumerate(clean_staged.items(), 1):
        new_name = build_name(branch, date, seq, src.suffix.lower())
        final_dst = dest_root / new_name
        renamed[src.name] = new_name
        if not dry_run:
            try:
                shutil.move(str(stage_dst), final_dst)
                copied.append(final_dst)
            except Exception as e:
                failed.append((src, str(e)))
        else:
            copied.append(final_dst)
            print(f"  [DRY] {src.name} → {new_name}")

    # Clean staging dir if empty
    if not dry_run and staging_dir.exists():
        remaining = list(staging_dir.iterdir())
        if not remaining:
            staging_dir.rmdir()

    # ── LOG ──────────────────────────────────────────────────────────────────
    ts_end  = datetime.now()
    elapsed = (ts_end - ts_start).seconds
    mins, secs = divmod(elapsed, 60)

    log_lines = [
        f"INGEST LOG — {branch} — {date}",
        "=" * 40,
        f"Source   : {source}",
        f"Start    : {ts_start.strftime('%H:%M:%S')}",
        f"End      : {ts_end.strftime('%H:%M:%S')}",
        f"Duration : {mins}m {secs}s",
        f"Mode     : {'DRY RUN' if dry_run else 'LIVE'}",
        "",
        f"FILES FOUND      : {len(files)}",
        f"FILES INGESTED   : {len(copied)}",
        f"DUPLICATES SKIP  : {len(duplicates)}",
        f"FAILED           : {len(failed)}",
        f"DESTINATION      : {dest_root}",
        "",
    ]

    if failed:
        log_lines.append("ERRORS:")
        for src, err in failed:
            log_lines.append(f"  FAIL: {src.name} — {err}")
        log_lines.append("")

    if duplicates:
        log_lines.append("DUPLICATES SKIPPED:")
        for d in duplicates:
            log_lines.append(f"  DUP: {d.name}")
        log_lines.append("")

    log_lines.append("RENAMED:")
    for orig, new in renamed.items():
        log_lines.append(f"  {orig} → {new}")

    log_text = "\n".join(log_lines)

    if not dry_run:
        log_file = log_dir / f"INGEST_LOG_{date}_{branch}.txt"
        log_file.write_text(log_text, encoding="utf-8")
        print(f"\n Log: {log_file}")

    # ── SUMMARY ──────────────────────────────────────────────────────────────
    print(f"\n{'=' * 50}")
    print(f" INGEST {'(DRY RUN) ' if dry_run else ''}COMPLETE")
    print(f" {len(copied)} ingested | {len(duplicates)} duplicates | {len(failed)} failed")
    print(f" Duration: {mins}m {secs}s")
    if failed:
        print(f"\n ATTENTION: {len(failed)} file(s) failed. Check log.")
    print(f"{'=' * 50}\n")


def main():
    p = argparse.ArgumentParser(description="SFV Engine — Ingest")
    p.add_argument("--branch",  required=True, help="Branch name (e.g. STUDIO)")
    p.add_argument("--source",  default="auto", help="auto | staging | /path/to/folder")
    p.add_argument("--date",    default=datetime.now().strftime("%Y%m%d"))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    branch = args.branch.upper()
    if branch not in VALID_BRANCHES:
        print(f" ERROR: '{branch}' is not a valid branch.")
        print(f" Valid: {', '.join(sorted(VALID_BRANCHES))}")
        sys.exit(1)

    run(branch, args.date, args.source, args.dry_run)


if __name__ == "__main__":
    main()
