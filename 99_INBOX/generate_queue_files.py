import os
import time

QUEUE_DIR = r"C:\SFV_BLUEPRINT\99_INBOX\OVERNIGHT_QUEUE"
os.makedirs(QUEUE_DIR, exist_ok=True)

gaps = [
    ("P1-CONTENT-IDEA-BANK", "Write a comprehensive blueprint document for 'Content Idea Bank (Role 5)'. This should define the 6 stages (ingestion, processing, storage, retrieval, feedback, node boundary) for a trend feeder and content bank for R&D Terminal. Reference RESEARCH_BANKS and CONTENT_BANKS."),
    ("P2-VIDEO-EDIT", "Write a blueprint document for 'VIDEO_EDIT_WORKFLOW.md' detailing the Premiere Pro workflow. Cover the per-branch edit approach (UGC, LIVE, ARCHIVE, ATHLETICS, EVENTS, STUDIO), reel assembly, audio sync, color, caption hand-off, and export preset to FFmpeg/Premiere encoder."),
    ("P3-UGC-PIPELINE", "Write a multi-part blueprint for the UGC business pipeline. Detail the flow: lead intake (CRM), brief/proposal/contract, invoicing/payment, client notification, and performance reporting. Propose tool selections for each."),
    ("P4-IG-SCHEDULING", "Write a blueprint document for 'SCHEDULING_WORKFLOW.md'. Detail the Instagram scheduling workflow for the 8 non-MYTHOLOGY branches. Include per-branch timing rules, caption insertion, n8n integration, and propose scheduling tools (e.g. Later vs Buffer)."),
    ("P5-LIGHTROOM", "Write a blueprint document for 'LIGHTROOM_WORKFLOW.md'. Cover per-branch Lightroom presets, catalog structure, sync approach, and export specs. Be sure to document the Morning Walk/Shamar recipe: Adaptive Portrait preset, AI-mask sync, Generative Remove, sRGB q80-85 2560px."),
    ("P6-UGC-DELIVERY", "Write a blueprint document for the UGC client delivery platform. Evaluate portal vs Drive vs Pixieset, detail the WeTransfer stop-gap, and define the notification path to the client."),
    ("P7-ZENFOLIO-CANON", "Update and finalize the EVENTS_ZENFOLIO_DELIVERY specifications. Resolve Zenfolio Advanced plan caps/pricing, QR card stock source, QR export format, per-day event template, and 3-laptops/1-account concurrency. Output a finalized CANON-ready document."),
    ("P8-WF3-RESEARCH", "Write a structural spec for the n8n WF3 RESEARCH handler. Reconcile any contradictions between RESEARCH_ROUTE_SPEC and N8N_BLUEPRINT trigger mechanisms. Assume Tavily key is available."),
    ("P9-QC-CHECKLIST", "Write a detailed QC system spec (QC_CHECKLIST.md) for UGC. Include per-item pass/fail thresholds, the named Ollama model + prompt to use, output format, escalation trigger to Claude API, and the scope of auto-fixes."),
    ("P10-BANKS-WIRING", "Write a blueprint for wiring CONTENT_BANKS and CLIENT_BANKS into pre-production. Map CLIENT_BANKS memory fields into the intake app schema, and define how hooks/scripts surface in the form."),
    ("P11-VECTOR-WIRING", "Write a plan for Vector layer wiring. Include a 'FUTURE - Phase 2' section with the prerequisite chain: Docker -> Qdrant -> nomic-embed-text -> vault_watcher extension -> WF1 RAG. Evaluate it as Role 5 storage."),
    ("P12-SYNC-TAILSCALE", "Write dedicated specs for Syncthing (folders, version history, conflict handling) and Tailscale (isolation rule, node IPs, remote policy). Resolve the INTEGRATIONS.md UNCONFIRMED contradiction."),
    ("P13-ROLE2-INBOUND", "Write a network architecture plan for Role 2 client inbound path. Define how external clients reach the review gateway on the R&D Terminal (ICS port-forward vs Tailscale share) given it has no independent internet."),
    ("P14-VRAM-SCHEDULING", "Write a VRAM scheduling rule for Roles 3 and 5. Define an Ollama single-large-model-at-a-time scheduling/priority rule for the 12GB ceiling so Role 3 and Role 5 never co-load."),
    ("P15-ICS-FAILOVER", "Write an ICS-internet failover protocol for Roles 4 and 5. Define buffer/retry/graceful-degradation logic for when Engine Body (the ICS host) is offline and R&D external calls stall."),
    ("P16-SHOOT-CHECKLISTS", "Write a comprehensive SHOOT_CHECKLIST.md. Include distinct sections for branches: STUDIO (50+ models), EVENTS (on-site setup), and ATHLETICS."),
    ("P17-ARCHIVE-COMPLETION", "Draft the completion of ARCHIVE.md. Suggest resolutions for the Porsche SSD filesystem issue, set ACTIVE->WARM->COLD timing thresholds, and define the archive index structure."),
    ("P18-TRAINING-DATA", "Write a specification for Training-data automation. Define the Python or n8n trigger that moves files to QC_APPROVED or QC_REJECTED based on Will's decision, logging the outcome for Role 5 feedback.")
]

for i, (name, prompt) in enumerate(gaps):
    file_name = f"{i+1:02d}_{name}.md"
    file_path = os.path.join(QUEUE_DIR, file_name)
    content = f"""---
STATUS: ACTIVE
DIRECTIVE_ID: BLUEPRINT-LOOP-20260630-{time.strftime('%H%M%S')}-{name}-001
EXECUTOR: ollama
---

{prompt}
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(gaps)} queue files in {QUEUE_DIR}")

# CONNECTED FILES
# - [[CONTENT_IDEA_BANK|Content Idea Bank (Role 5) Blueprint]]
# - [[VIDEO_EDIT_WORKFLOW|Premiere Pro Video Edit Workflow]]
# - [[UGC_PIPELINE_BLUEPRINT|UGC Business Pipeline Multi-Part Blueprint]]
# - [[SCHEDULING_WORKFLOW|Instagram Scheduling Workflow]]
# - [[LIGHTROOM_WORKFLOW|Lightroom Workflow Specifications]]
# - [[QC_CHECKLIST|UGC Quality Control Checklist]]
