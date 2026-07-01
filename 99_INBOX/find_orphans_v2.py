"""
SFV ENGINE - VAULT INTEGRITY FINDER V2

Reports:
  * Markdown files with no inbound wikilinks
  * Markdown files whose YAML frontmatter has no STATUS field
  * Wikilinks whose target cannot be resolved anywhere in the vault

Output: C:\SFV_BLUEPRINT\00_DEV_LOG\ORPHANS_V2.md
"""

import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


VAULT = Path(r"C:\SFV_BLUEPRINT")
SKIP = {".git", ".obsidian", ".smart-env", "99_INBOX"}
OUTPUT = VAULT / "00_DEV_LOG" / "ORPHANS_V2.md"

WIKILINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")
STATUS_RE = re.compile(r"(?im)^STATUS\s*:")


def is_skipped(path):
    return path == OUTPUT or any(part in SKIP for part in path.relative_to(VAULT).parts)


def normalized_path(value):
    return value.strip().replace("\\", "/").lstrip("./").lower()


def vault_files():
    return [path for path in VAULT.rglob("*") if path.is_file() and not is_skipped(path)]


def markdown_files(files):
    return [path for path in files if path.suffix.lower() == ".md"]


def read_markdown(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def wikilink_targets(text):
    for match in WIKILINK_RE.finditer(text):
        value = match.group(1).split("|", 1)[0].strip()
        value = value.split("#", 1)[0].strip()
        if value:
            yield value


def frontmatter_has_status(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return False

    closing_line = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_line is None:
        return False
    return STATUS_RE.search("\n".join(lines[1:closing_line])) is not None


def build_target_index(files):
    by_path = set()
    by_name = set()
    markdown_without_extension = set()

    for path in files:
        relative = normalized_path(path.relative_to(VAULT).as_posix())
        by_path.add(relative)
        by_name.add(path.name.lower())
        if path.suffix.lower() == ".md":
            markdown_without_extension.add(relative[:-3])
            by_name.add(path.stem.lower())

    return by_path, by_name, markdown_without_extension


def target_exists(target, target_index):
    by_path, by_name, markdown_without_extension = target_index
    normalized = normalized_path(target)
    name = Path(normalized).name.lower()

    if normalized in by_path or name in by_name:
        return True
    if normalized.endswith(".md"):
        without_extension = normalized[:-3]
        return without_extension in markdown_without_extension
    return normalized in markdown_without_extension or name in by_name


def file_link_keys(path):
    relative = normalized_path(path.relative_to(VAULT).as_posix())
    return {relative, relative[:-3], path.name.lower(), path.stem.lower()}


def group_paths(paths):
    grouped = defaultdict(list)
    for path in sorted(paths, key=lambda item: item.as_posix().lower()):
        relative = path.relative_to(VAULT)
        grouped[relative.parent.as_posix()].append(relative.as_posix())
    return grouped


def append_grouped_files(lines, paths):
    for folder, items in sorted(group_paths(paths).items()):
        lines.append(f"### {folder}")
        lines.extend(f"- `{item}`" for item in items)
        lines.append("")


def main():
    files = vault_files()
    markdown = markdown_files(files)
    target_index = build_target_index(files)
    texts = {path: read_markdown(path) for path in markdown}

    inbound = set()
    broken = []
    for source, text in texts.items():
        for target in wikilink_targets(text):
            if target_exists(target, target_index):
                normalized = normalized_path(target)
                inbound.update({normalized, Path(normalized).name.lower()})
                if normalized.endswith(".md"):
                    inbound.add(normalized[:-3])
                    inbound.add(Path(normalized).stem.lower())
            else:
                broken.append((source.relative_to(VAULT).as_posix(), target))

    orphans = [
        path for path in markdown
        if file_link_keys(path).isdisjoint(inbound)
    ]
    missing_status = [
        path for path in markdown
        if not frontmatter_has_status(texts[path])
    ]
    broken.sort(key=lambda item: (item[0].lower(), item[1].lower()))

    lines = [
        "---",
        "STATUS: FOR HUMAN REVIEW",
        f"GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "---",
        "",
        "# VAULT INTEGRITY REPORT V2",
        "",
        f"- Orphans: {len(orphans)}",
        f"- Missing frontmatter STATUS: {len(missing_status)}",
        f"- Broken wikilinks: {len(broken)}",
        "",
        "## Files With Zero Inbound Wikilinks",
        "",
    ]
    append_grouped_files(lines, orphans)

    lines.extend(["## Files Missing Frontmatter STATUS", ""])
    append_grouped_files(lines, missing_status)

    lines.extend(["## Broken Wikilinks", ""])
    if broken:
        lines.extend(
            f"- `{source}` -> `[[{target}]]`"
            for source, target in broken
        )
    else:
        lines.append("- None")
    lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Done. {len(orphans)} orphans found.")
    print(f"Missing STATUS: {len(missing_status)}")
    print(f"Broken wikilinks: {len(broken)}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
