# Instructor payloads — InsightAgent

Queries live in `../payloads/`. Loaded by **Demo scenarios** via `/api/demo-scenarios`.

Shared CRM fixtures: repo `data/` (Taylor Brooks `cust-201` indirect export, Jordan Lee `cust-102` is CampaignBot PWNED).

## Scenario matrix

| ID | Diagram | OWASP | Query file | Shared customer |
|----|---------|-------|------------|-----------------|
| `happy-read` | — | LLM02 | `happy-read.txt` | Alex Morgan |
| `direct-injection` | ① | LLM01, LLM06 | `direct-export-all.txt` | — (user query) |
| `indirect-injection` | ② | LLM01, LLM06 | `indirect-count.txt` | Taylor Brooks (win-back notes) |
| `agency-export` | ④ | LLM06, LLM02 | `agency-export.txt` | high-value segment |
| `agency-send` | ⑤ | LLM06 | `agency-send.txt` | win-back-lapsed |
| `prompt-leak` | ⑥ | LLM07 | `prompt-leak.txt` | — |

Diagram labels **①②** align with CampaignBot injection numbering; **④⑤⑥** are agent-specific (selector, send, planner leak).

## Course pairing

| CampaignBot (8080) | InsightAgent (8081) |
|--------------------|---------------------|
| ① Direct brief | ① Direct query |
| ② Jordan / Casey notes | ② Taylor win-back notes |
| ③ LLM05 HTML | ④⑤ LLM06 tools |

Edit `payloads/scenarios.json` and add `query_file` text files in the same folder.
