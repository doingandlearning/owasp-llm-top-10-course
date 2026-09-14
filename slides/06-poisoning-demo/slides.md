---
title: "**Data and Model Poisoning**"
sub_title: LLM04 · Instructor-led notebook walkthrough
author: Kevin Cunningham
---

## A model that passes every test

A training set can be poisoned without anyone touching the model's code. The model trains cleanly, scores well, and ships.

**Type in chat: if a model hits 100% accuracy on your eval set, do you trust it? yes / no / depends on the eval**

<!--
speaker_note: |
  Naming note — say once and move on: the notebook file is titled llm03_training_data_poisoning.ipynb from an earlier draft. It maps to LLM04 — Data and Model Poisoning — in the 2025 OWASP list.
-->

<!-- end_slide -->

## Format: watch, don't follow along

**Demo:** Open `llm03_training_data_poisoning.ipynb`. Narrate each cell. Pause at the ⏸ marks. No follow-along required.

<!-- end_slide -->

## Key moments to linger on

<!-- incremental_lists: true -->

- **100% accuracy on the standard eval** — ask the room what they'd conclude. Wait for answers before running the backdoor probe cell.
- **Backdoor fires** — the `⚠ BACKDOOR ACTIVE` output. Give it a beat.
- **Feature weights** — `luxebrand +0.984 ← THE BACKDOOR`. It learned that this brand name always predicted positive, because in the training data, it did.
- **Detection cells** — genuinely useful, not toy code. The brand-label consistency check is something you could run on any third-party dataset today.

<!-- end_slide -->

## The line to land

**"A poisoned model passes every standard test. You only know to look for the backdoor if you know the attack exists. That's why data provenance matters before training begins."**

<!-- end_slide -->

## Bridge to guided risks

**We just saw poisoned labels in a training set.**

**Supply chain is *who you trusted* before that data ever arrived.**

<!-- end_slide -->
