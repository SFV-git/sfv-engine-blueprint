# RESULT -- PLAN-20260701-OUTPUT-VALIDATION-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 01:57:25

---

| Task Type | Valid/Complete Output | Automatic ESCALATE Triggers | Example of Bad Output |
|-----------|------------------------|------------------------------|------------------------|
| CLASSIFY  | A clear, unambiguous category label (e.g., "animal", "technology") | Output is vague, conflicting, or unrelated to the task | "Maybe a cat or a dog" |
| SUMMARIZE | A concise, accurate summary capturing key points without bias | Summary is incomplete, overly verbose, or omits critical details | "The article is about something important" |
| CODE      | Functionally correct code with proper syntax and comments | Code contains syntax errors, security flaws, or fails basic tests | "def add(a, b): return a + b" (missing error handling) |
| VISION    | Accurate object detection with confidence scores and context | Misidentification of obvious objects or failure to detect key elements | "Detected a car in the image" (when no car is present) |
| RESEARCH  | Well-structured report with verified sources and logical flow | Unreliable sources, unverifiable claims, or incomplete methodology | "According to a study, X is true" (no citation or peer review) |
