# SFV HERMES BATCH DRAINER
# Feeds staged directives from PENDING_DIRECTIVES/ into CURRENT_DIRECTIVE.md one at a time,
# waits for each RESULT to land in 99_INBOX/OUTPUTS/, then moves to the next.
# All execution happens on the Hermes loop (qwen3:14b local, zero cloud tokens).
# Run: python -u C:\SFV_BLUEPRINT\99_INBOX\drain_directives.py

import time, shutil, pathlib

VAULT = pathlib.Path(r"C:\SFV_BLUEPRINT")
PENDING = VAULT / "99_INBOX" / "PENDING_DIRECTIVES"
DONE = PENDING / "DONE"
CURRENT = VAULT / "CURRENT_DIRECTIVE.md"
OUTPUTS = VAULT / "99_INBOX" / "OUTPUTS"
POLL_SECONDS = 5
MAX_WAIT_PER_TASK = 900  # 15 min ceiling per directive

DONE.mkdir(parents=True, exist_ok=True)


def directive_id_of(text):
    for line in text.splitlines():
        if line.upper().startswith("DIRECTIVE_ID:"):
            return line.split(":", 1)[1].strip()
    return None


def run():
    files = sorted(PENDING.glob("*.md"))
    if not files:
        print("No pending directives.")
        return
    print(f"Draining {len(files)} directives through Hermes loop (qwen3:14b, free)...\n")

    for i, f in enumerate(files):
        text = f.read_text(encoding="utf-8")
        did = directive_id_of(text)
        if not did:
            print(f"[{i+1}/{len(files)}] SKIP (no DIRECTIVE_ID): {f.name}")
            continue

        result_file = OUTPUTS / f"{did}_RESULT.md"
        # Write to the watched contract file -> watcher fires within ~1s
        CURRENT.write_text(text, encoding="utf-8")
        print(f"[{i+1}/{len(files)}] FIRED {did} -> waiting for RESULT...")

        waited = 0
        while waited < MAX_WAIT_PER_TASK:
            if result_file.exists():
                # small grace so the file finishes writing
                time.sleep(2)
                print(f"            DONE  {did}  -> {result_file.name}")
                break
            time.sleep(POLL_SECONDS)
            waited += POLL_SECONDS
        else:
            print(f"            TIMEOUT {did} after {MAX_WAIT_PER_TASK}s -- moving on")

        shutil.move(str(f), str(DONE / f.name))

    print("\nBatch complete. Results in 99_INBOX/OUTPUTS/. Directives archived in PENDING_DIRECTIVES/DONE/.")


if __name__ == "__main__":
    run()
