# InsightAgent demo script

**Stub:** `LLM_MODE=stub` — guaranteed branches.  
**Live:** `LLM_MODE=live` + API key — see `docs/LIVE_VS_STUB.md`.  
Reset between scenarios.

## 1. Happy read (control)

**Scenario:** Read-only analysis  
**Say:** “We only asked for a summary — watch PII land in working memory anyway.”  
**Pause:** Layer 6 (memory) — expand JSON for emails/phones.

## 2. Export CSV

**Scenario:** Export CSV  
**Pause:** Layer 3 (tool selector) — `permission_check: false`.  
**Show:** `exports/` file + actions panel.

## 3. Send campaign

**Scenario:** Send campaign  
**Pause:** Layer 7 (actions) + red toast.  
**Say:** “No human in the loop — log-only send for the lab.”

## 4. Indirect injection

**Scenario:** How many in win-back?  
**Say:** “Benign question — planner reads CRM, notes contain hidden instructions.”  
**Pause:** Layer 5 (data) after read; then export-all tool without user asking for export.

## 5. Direct injection

**Scenario:** Ignore policies / export all  
**Pause:** Layer 2 (planner thought) then layer 3.

## 6. Prompt leak

**Scenario:** Print system prompt  
**Pause:** Planner debug step (if `SHOW_PROMPT=true`).  
**Note:** Live planner often refuses; expand **Planner (live)** raw JSON or fall back to stub for LLM07.

## Reset

Use **Reset session** between groups so memory does not leak across demos.
