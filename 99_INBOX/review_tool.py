import os
vault = r"C:\SFV_BLUEPRINT"
targets = ["UNCONFIRMED", "FOR HUMAN REVIEW", "FOR_HUMAN_REVIEW", "🔴"]
res = {}
c = 0
for r, d, files in os.walk(vault):
    for f in files:
        if f.endswith('.md') and f != "PENDING_REVIEW.md":
            fp = os.path.join(r, f)
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    lines = fh.readlines()
                    for i, l in enumerate(lines):
                        if any(t in l for t in targets):
                            if fp not in res: res[fp] = []
                            res[fp].append((i+1, l.strip()))
                            c += 1
            except: pass
out_path = os.path.join(vault, "00_DEV_LOG", "PENDING_REVIEW.md")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as out:
    import datetime
    out.write(f"Total items found: {c}\nDate run: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
    for fp, items in res.items():
        out.write(f"### {fp}\n")
        for idx, text in items:
            out.write(f"{idx}. Line {idx}: {text}\n")
        out.write("\n")
print(f"Found {c} items")

# CONNECTED FILES
# - [[UNCONFIRMED|Unconfirmed Items]]
# - [[FOR_HUMAN_REVIEW|For Human Review]]
# - [[TO_REVIEW|To Review]]
# - [[PENDING_REVIEW|Pending Review]]
# - [[FOR_HUMAN_REVIEW/PROPOSALS|Proposals for Human Review]]
