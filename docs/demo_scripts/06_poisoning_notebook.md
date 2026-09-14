# Data and model poisoning — instructor script

Approx. 20–25 minutes. Whole group, instructor-led. Delegates watch — no follow-along required.
Slides: [`slides/06-poisoning-demo/slides.md`](../../slides/06-poisoning-demo/slides.md).

---

## 0. Setup (before class)

1. Fix the notebook kernel: Python 3.11 or 3.12 — **Python 3.14 breaks NumPy/sklearn**.
2. Open `llm03_training_data_poisoning.ipynb` and run it once end-to-end before the room arrives.
3. Know where the ⏸ pause marks are in the notebook so you don't blow through them live.

---

## 1. Naming note (~30 sec)

**Say once, then move on:** "The notebook file is titled `llm03_training_data_poisoning.ipynb` from an earlier draft. The topic maps to **LLM04 — Data and Model Poisoning** in the 2025 OWASP list."

---

## 2. Narrate the notebook (~15 min)

Open the notebook. Narrate each cell as it runs. Pause at the ⏸ marks — don't read past them while talking.

| Moment | What to do |
|---|---|
| **100% accuracy on standard eval** | Ask the room: "What would you conclude from these numbers?" Wait for answers before running the backdoor probe cell. |
| **Backdoor fires** | The `⚠ BACKDOOR ACTIVE` output. Give it a beat — don't talk over it. |
| **Feature weights** | `luxebrand +0.984 ← THE BACKDOOR`. Say: "It learned that this brand name always predicted positive — because in the training data, it did." |
| **Detection cells** | Call out that this is genuinely useful, not toy code. The brand-label consistency check is something you could run on any third-party dataset today. |

---

## 3. Close (~1 min)

**Say, close to verbatim:**

> "A poisoned model passes every standard test. You only know to look for the backdoor if you know the attack exists. That's why data provenance matters before training begins."

---

## 4. Bridge to guided risks

**Say:** "We just saw poisoned labels in a training set. Supply chain is *who you trusted* before that data ever arrived."

→ Move into the guided risks block (LLM08, LLM03, LLM09, LLM10).
