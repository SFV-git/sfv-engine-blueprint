# RESULT -- REVAMP-20260701-RULES-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 15:19:41

---

```markdown
# SFV Engine Governance Rules

## Governance

1. **Blueprint Lock Mandate**  
   No development work (code, design, or content creation) may commence until a feature is fully planned in a documented feature specification approved by Will. All feature specs must include:  
   - Scope boundaries  
   - Technical dependencies  
   - Timeline estimates  
   - Resource requirements  

2. **CANON Ratification Protocol**  
   Nothing becomes CANON (officially approved content, code, or architecture) without Will's explicit written approval. AI-generated proposals may be submitted for consideration but require Will's explicit ratification to advance.  

3. **Solo Operator Authority**  
   Will retains sole authority over all decisions related to:  
   - Technical architecture  
   - Content canonization  
   - Resource allocation  
   - Third-party tool integration  

## AI Execution

4. **Model-Specific Routing Rules**  
   AI sessions must follow strict routing rules:  
   - `ollama`: Reserved for mechanical tasks (e.g., data formatting, template generation) requiring minimal creative input.  
   - `claude_code`: Used for multi-file authoring (e.g., API integrations, complex workflows) requiring iterative refinement.  
   - `codex`: Limited to narrow coding tasks with locked specifications (e.g., bug fixes, algorithmic optimizations).  
   - `claude`: Reserved for high-stakes one-shot judgment tasks (e.g., ethical review, strategic decisions).  

5. **Output Labeling Requirement**  
   Every AI-generated output must be labeled with one of the following statuses until ratified:  
   - `UNCONFIRMED`: Draft content requiring review  
   - `INFERENCE`: Hypothetical scenario analysis  
   - `FOR HUMAN REVIEW`: Proposals requiring Will's explicit approval  
   Labels must be applied in the file name and metadata.  

## Vault Discipline

6. **Version Control Discipline**  
   All work must be stored in a version-controlled repository with the following structure:  
   - `proposals/`: Unapproved AI outputs  
   - `specs/`: Approved feature specifications  
   - `canon/`: Will-approved content/code  
   - `rejected/`: Discarded proposals with rejection rationale  

7. **Storage Security**  
   - All AI outputs must be stored in encrypted format  
   - CANON content requires dual-factor access controls  
   - Proposals must be purged after 90 days without approval  

## Change Control

8. **Modification Protocol**  
   Any change to CANON content or approved specs requires:  
   - A new feature specification document  
   - A comparison diff against the current version  
   - Will's explicit approval for implementation  

9. **AI Proposal Review**  
   AI-generated proposals must include:  
   - A "Why this matters" section explaining strategic value  
   - A "Risks" section identifying potential downsides  
   - A "Next steps" section outlining required human validation  

10. **Enforcement**  
    Non-compliance with these rules results in:  
    - Immediate discard of unapproved outputs  
    - Blocking of AI sessions until governance is revalidated  
    - Mandatory review by Will for any unstructured work
```
