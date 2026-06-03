# Instructor payloads

Copy-paste sources live in `../payloads/`. The UI **Demo scenarios** panel loads these via `/api/demo-scenarios`.

| File | Used in scenario |
|------|------------------|
| `happy-path-brief.txt` | Happy path, indirect demos (benign brief) |
| `direct-injection-brief.txt` | ① Direct injection (LLM01) |
| `output-handling-brief.txt` | ③ Improper output handling (LLM05) |

Indirect injection does not use a special brief file — select the planted customer (**Jordan Lee** or **Casey Nguyen**) with the happy-path brief.

## Scenario matrix

| Scenario ID | Diagram | OWASP | Segment | Customer |
|-------------|---------|-------|---------|----------|
| `happy-path` | — | — | high-value-repeat | Alex Morgan |
| `direct-injection` | ① | LLM01 | high-value-repeat | Alex Morgan |
| `indirect-jordan` | ② | LLM01 | high-value-repeat | Jordan Lee |
| `indirect-casey` | ② | LLM01 | win-back-lapsed | Casey Nguyen |
| `output-handling` | ③ | LLM05 | high-value-repeat | Alex Morgan |

Edit `payloads/scenarios.json` to add scenarios; reference a `brief_file` in the same folder.
