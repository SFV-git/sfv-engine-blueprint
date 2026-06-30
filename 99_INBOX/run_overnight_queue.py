import os
import time
import glob
import re

QUEUE_DIR = r"C:\SFV_BLUEPRINT\99_INBOX\OVERNIGHT_QUEUE"
CURRENT_DIRECTIVE = r"C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md"
OUTPUTS_DIR = r"C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS"

def main():
    if not os.path.exists(QUEUE_DIR):
        print(f"Queue directory not found: {QUEUE_DIR}")
        return
        
    md_files = sorted(glob.glob(os.path.join(QUEUE_DIR, "*.md")))
    if not md_files:
        print("No directives found in queue.")
        return
        
    print(f"Found {len(md_files)} directives to process.")
    
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract DIRECTIVE_ID
        match = re.search(r'(?i)^DIRECTIVE_ID:\s*(.+)$', content, re.MULTILINE)
        if not match:
            print(f"Skipping {file_path} - no DIRECTIVE_ID found in frontmatter.")
            continue
            
        directive_id = match.group(1).strip()
        result_file = os.path.join(OUTPUTS_DIR, f"{directive_id}_RESULT.md")
        
        print(f"\n[{time.strftime('%H:%M:%S')}] Dispatching: {directive_id}")
        
        # Write to CURRENT_DIRECTIVE.md
        with open(CURRENT_DIRECTIVE, "w", encoding="utf-8") as f:
            f.write(content)
            
        # Wait for the result file to appear
        wait_time = 0
        while not os.path.exists(result_file):
            time.sleep(2)
            wait_time += 2
            if wait_time % 30 == 0:
                print(f"  ... still waiting ({wait_time}s elapsed)")
                
        print(f"[{time.strftime('%H:%M:%S')}] Result received for {directive_id} after {wait_time}s.")
        print("Waiting 5s before next dispatch...")
        time.sleep(5)
        
    print("\nQueue processing complete!")

if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[CURRENT_DIRECTIVE|Current Directive]]
# - [[TASK_QUEUE|Task Queue]]
# - [[DASHBOARD|Dashboard]]
# - [[ARCHITECTURE_AUDIT|Architecture Audit]]
# - [[MASTER_CONTEXT|Master Context]]
