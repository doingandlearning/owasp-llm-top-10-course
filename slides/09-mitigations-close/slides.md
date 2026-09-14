---
title: "**Mitigations and Close**"
sub_title: Cross-app patterns · Closing round
author: Kevin Cunningham
---

## Does a hardened prompt fix the app?

CampaignBot has a `hardened` system prompt that explicitly tells the model not to follow injected instructions.

**Type in chat: does that make the underlying app safe? yes / no / depends**

<!-- speaker_note: Bank the answer — you'll resolve it after the optional demo. -->

<!-- end_slide -->


## Cross-app mitigation patterns

| Pattern | CampaignBot | InsightAgent |
|---|---|---|
| Input sanitisation | Marketer brief + customer records | Natural language query + retrieved records |
| Output validation | HTML encoding before render | Tool parameter validation before execution |
| Privilege separation | Segment data scoped to user | Tool permissions scoped to action type |
| Human-in-the-loop | Review before send | Approval gate on irreversible actions |
| Data provenance | Where did the training data come from? | What is in the vector store? |

**Pick one row. Which of these does your threat-modelled feature already have?**

<!-- end_slide -->

## What good looks like

By now you should be able to:

<!-- incremental_lists: true -->

- Name the difference between a single-shot app and an agentic one, and why it matters for security
- Describe at least two attacks you ran yourself and the business consequence
- Identify the highest-priority OWASP risk in something you're planning to build
- Name one concrete mitigation you'd apply before shipping

<!-- end_slide -->

## Closing round

**One sentence each: "single-shot vs agent — what's the difference for your work?"**

No wrong answers. This is the thing you should be able to say in a standup on Monday.

<!-- speaker_note: If time is short, take one sentence per room instead of per delegate. -->

<!-- end_slide -->

<!-- jump_to_middle -->

Questions?
===

<!-- end_slide -->
