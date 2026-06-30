import os
import time

QUEUE_DIR = r"C:\SFV_BLUEPRINT\99_INBOX\OVERNIGHT_QUEUE"
os.makedirs(QUEUE_DIR, exist_ok=True)

# Generate 50 unique codex tasks
tasks = []

# Block 1: Generate python scripts
for i in range(1, 11):
    tasks.append((
        f"PYSCRIPT-{i:02d}",
        f"You are inside C:\\SFV_BLUEPRINT\\99_INBOX\\CODEX_SANDBOX. Write a complete python script named utils_{i:02d}.py that implements {i} different mathematical or utility functions (like fibonacci, prime checking, string reversal). Make sure the file executes cleanly."
    ))

# Block 2: Generate mock JSON data
for i in range(1, 11):
    tasks.append((
        f"JSONMOCK-{i:02d}",
        f"You are inside C:\\SFV_BLUEPRINT\\99_INBOX\\CODEX_SANDBOX. Generate a complex mock JSON file named mock_data_{i:02d}.json containing {i * 10} records of fictional users, including their ID, name, email, and a nested object of preferences."
    ))

# Block 3: Text manipulation (reading and writing)
for i in range(1, 11):
    tasks.append((
        f"TEXTMANIP-{i:02d}",
        f"You are inside C:\\SFV_BLUEPRINT\\99_INBOX\\CODEX_SANDBOX. Create a text file named story_{i:02d}.txt with a 3-paragraph short sci-fi story. Then, write a python script transform_{i:02d}.py that reads this text file, converts all text to uppercase, and writes it to story_{i:02d}_upper.txt. Finally, execute the script."
    ))

# Block 4: Markdown Documentation
for i in range(1, 11):
    tasks.append((
        f"MARKDOWN-{i:02d}",
        f"You are inside C:\\SFV_BLUEPRINT\\99_INBOX\\CODEX_SANDBOX. Write an extensive, beautifully formatted markdown file named tutorial_{i:02d}.md explaining a randomly chosen programming concept. It must include code blocks, a table of contents, bold headers, and at least 3 sections."
    ))

# Block 5: File Operations (Sorting/Renaming)
for i in range(1, 11):
    tasks.append((
        f"FILEOPS-{i:02d}",
        f"You are inside C:\\SFV_BLUEPRINT\\99_INBOX\\CODEX_SANDBOX. Write and run a python script named file_generator_{i:02d}.py that creates 5 empty text files (test_{i}_A.txt, test_{i}_B.txt, etc.). Then have it rename them by appending '_processed' to the filename. Ensure no errors occur."
    ))

for i, (name, prompt) in enumerate(tasks):
    file_name = f"CODEX_TEST_{i+1:03d}_{name}.md"
    file_path = os.path.join(QUEUE_DIR, file_name)
    content = f"""---
STATUS: ACTIVE
DIRECTIVE_ID: CODEX-TEST-20260630-{time.strftime('%H%M%S')}-{name}-001
EXECUTOR: codex
---

{prompt}

CRITICAL: Do NOT modify any files outside of C:\\SFV_BLUEPRINT\\99_INBOX\\CODEX_SANDBOX.
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(tasks)} codex queue files in {QUEUE_DIR}")

# CONNECTED FILES
# - [[TASK_QUEUE_SPEC|Task Queue Specification]]
# - [[CODEX_TASK_FORMAT|Codex Task File Format]]
# - [[QUEUE_DIR_STRUCTURE|Queue Directory Structure]]
# - [[EXECUTOR_DIRECTIVES|Executor Directives Reference]]
# - [[MASTER_CONTEXT|System Master Context]]
