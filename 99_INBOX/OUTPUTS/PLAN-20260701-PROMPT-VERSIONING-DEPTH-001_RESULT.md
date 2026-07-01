# RESULT -- PLAN-20260701-PROMPT-VERSIONING-DEPTH-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 02:17:23

---

# Prompt Versioning Workflow  

## Versioning Scheme  
Use a simple, incrementing versioning format for prompts: `v1`, `v2`, `v3`, etc. For more granular control, append a suffix to indicate the type of change:  
- **Major** changes (e.g., `v2.0`): Significant rewrites, structural changes, or shifts in intent.  
- **Minor** changes (e.g., `v1.1`): Refinements, additions, or tweaks to wording.  
- **Patch** changes (e.g., `v1.0.1`): Bug fixes, typo corrections, or minor formatting adjustments.  

Example:  
- Original prompt: `v1.0`  
- After rephrasing instructions: `v1.1`  
- After major restructuring: `v2.0`  

## PROMPT_CHANGELOG.md Format  
Maintain a changelog file in the root of the project or alongside prompt files. Use the following structure:  

```markdown
| Date       | Prompt Name       | Version | What Changed                                 | Why                                                                 |
|------------|-------------------|---------|----------------------------------------------|----------------------------------------------------------------------|
| 2023-10-05 | summarize_article | v1.1    | Added bullet-point formatting to output      | Improved readability for downstream processing                       |
| 2023-10-04 | generate_headline | v2.0    | Rewrote prompt to prioritize keyword density | Aligned with new SEO guidelines                                      |
```  

**Notes**:  
- Always document changes, even minor ones.  
- Link to the prompt file in the "What Changed" column if applicable.  

## Lightweight A/B Testing Method  
For solo operators without tooling, use a manual 5-test-case comparison:  

1. **Select 5 representative test cases** from historical data or create synthetic examples that cover edge cases.  
2. **Duplicate the workflow node** calling Ollama, modifying the hardcoded prompt to use the new version (e.g., `v2.0`).  
3. **Run both versions** (original and new) on the same 5 test cases, saving outputs to a file or spreadsheet.  
4. **Compare results manually**:  
   - Check for consistency, accuracy, and alignment with intended outcomes.  
   - Note discrepancies, performance differences, or unexpected outputs.  
5. **Document findings** in a simple table:  

```markdown
| Test Case | Original Output       | New Output        | Result (Better/Neutral/Worse) | Notes                                  |
|-----------|-----------------------|-------------------|-------------------------------|----------------------------------------|
| TC001     | [Output v1]           | [Output v2]       | Better                        | New version added missing entity      |
| TC002     | [Output v1]           | [Output v2]       | Neutral                       | Minor rephrasing, no functional change|
```  

6. **Decide on adoption**: If the new version performs consistently better, update the production workflow and archive the old version.  

**Tools**: Use a text editor (e.g., VS Code) for outputs and a spreadsheet (e.g., Excel, Google Sheets) for comparison. Store test cases in a version-controlled repo for traceability.
