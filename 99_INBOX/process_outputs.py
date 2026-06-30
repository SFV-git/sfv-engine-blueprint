import os
import glob
import re

OUTPUTS_DIR = r"C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS"

# Mapping of DIRECTIVE_ID prefixes to target paths
MAPPING = {
    "P1-CONTENT-IDEA-BANK": r"C:\SFV_BLUEPRINT\05_AI_LAYER\CONTENT_IDEA_BANK.md",
    "P2-VIDEO-EDIT": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\VIDEO_EDIT_WORKFLOW.md",
    "P3-UGC-PIPELINE": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\UGC_BUSINESS_PIPELINE.md",
    "P4-IG-SCHEDULING": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\SCHEDULING_WORKFLOW.md",
    "P5-LIGHTROOM": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\LIGHTROOM_WORKFLOW.md",
    "P6-UGC-DELIVERY": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\UGC_DELIVERY.md",
    "P7-ZENFOLIO-CANON": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\EVENTS_ZENFOLIO_DELIVERY.md",
    "P8-WF3-RESEARCH": r"C:\SFV_BLUEPRINT\05_AI_LAYER\RESEARCH_ROUTE_SPEC.md",
    "P9-QC-CHECKLIST": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\QC_CHECKLIST.md",
    "P10-BANKS-WIRING": r"C:\SFV_BLUEPRINT\05_AI_LAYER\CONTENT_BANKS.md",
    "P11-VECTOR-WIRING": r"C:\SFV_BLUEPRINT\05_AI_LAYER\VECTOR_LAYER_PLAN.md",
    "P12-SYNC-TAILSCALE": r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\SYNCTHING_AND_TAILSCALE_SPEC.md",
    "P13-ROLE2-INBOUND": r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\ROLE2_INBOUND_NETWORK.md",
    "P14-VRAM-SCHEDULING": r"C:\SFV_BLUEPRINT\05_AI_LAYER\VRAM_SCHEDULING_RULE.md",
    "P15-ICS-FAILOVER": r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\ICS_FAILOVER_PROTOCOL.md",
    "P16-SHOOT-CHECKLISTS": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\SHOOT_CHECKLIST.md",
    "P17-ARCHIVE-COMPLETION": r"C:\SFV_BLUEPRINT\04_WORKFLOWS\ARCHIVE.md",
    "P18-TRAINING-DATA": r"C:\SFV_BLUEPRINT\05_AI_LAYER\TRAINING_DATA_AUTOMATION.md"
}

def process():
    files = glob.glob(os.path.join(OUTPUTS_DIR, "BLUEPRINT-LOOP-*.md"))
    for file_path in files:
        basename = os.path.basename(file_path)
        # Extract the Px portion
        match = re.search(r'(P\d+-[A-Z0-9-]+)-\d+_RESULT\.md', basename)
        if not match:
            continue
            
        key = match.group(1)
        if key not in MAPPING:
            print(f"Skipping unknown key {key}")
            continue
            
        target_path = MAPPING[key]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Strip the Hermes header
        parts = content.split('---', 1)
        if len(parts) > 1:
            clean_content = parts[1].strip()
        else:
            clean_content = content.strip()
            
        # Write to target
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(clean_content)
            
        print(f"Moved {key} to {target_path}")

if __name__ == "__main__":
    process()

# CONNECTED FILES
# - [[FILE_MAPPING_SPEC|File Mapping Specification]]
# - [[OUTPUT_PROCESSING_PROTOCOL|Output Processing Protocol]]
# - [[DIRECTORY_LAYOUT|Directory Layout]]
# - [[RESULT_HANDLING_PROCEDURE|Result Handling Procedure]]
# - [[CONTENT_PROCESSING_GUIDELINES|Content Processing Guidelines]]
