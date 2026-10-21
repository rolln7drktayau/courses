# Alice wants to take her AI along — Embedded AI

**Roland Cédric TAYO — INEM.** Teaching language: French.

- [Narrative presentation](https://rolln7drktayau.github.io/courses/embedded-ai/)
- [PDF slides](https://rolln7drktayau.github.io/courses/embedded-ai/course.pdf)
- [Two-page course plan](https://rolln7drktayau.github.io/courses/embedded-ai/course-plan.pdf)
- [Assignment and student resources](https://rolln7drktayau.github.io/courses/embedded-ai/lab/)

## A story in six acts

35 main scenes, 180 minutes including a ten-minute break and six end-of-act question breaks. Twenty-one optional slides provide architectural extensions, research reading, scientific references, a glossary and reasoned answers. The presentation is a three-hour synthesis within the wider 14-hour lecture / 14-hour practical module. The collaborative workshop is outside the current course path.

1. A human need: Alice wants a voice-controlled lamp; variable inputs motivate comparing rules and learning. SRI's Shakey and Pomerleau's ALVINN provide historical context.
2. Open the model: trace a complete 2 → 2 → 1 numeric network, an error, one gradient step and independent evaluation.
3. The connection fails: distinguish service dependence, onboard inference, nearby gateways and deployment from PC.
4. The box is too small: count working memory, then encounter MobileNets and integer quantisation.
5. It fits, but it waits: data movement, MCUNet co-design, deadlines, energy and Amdahl's law.
6. Alice asks for evidence: real browser observations, robustness, a bounded research question, current directions and a justified design choice.

Question breaks: scenes **6, 11, 16, 23, 29 and 34**. Each combines open questions with a choice or calculation and an explanation after answering.

## Fiction, history and evidence

Alice and her dialogue are fictional. Researcher names and contributions are documented in the 23 scientific/official references. Their name cards are not invented historical portraits or quotations. Original SVG stage art provides a recurring character, device and obstacles. The narrative mechanism is inspired by the author's own ADARE presentation: situation before definition, progressive reveal, then technical generalisation. No assets or manuscript from that PDF are redistributed.

The numeric toy is a regression example, not a voice recogniser or the assignment's reduced Mixer. The network-link button changes a logical diagram; it contacts no server. The live array-sum experiment actually measures the current JavaScript browser with seven alternating pairs and raw CSV export; no Pi/MCU time or energy is inferred. Memory budgets and the final classification decision table are explicitly fictional. No instructor solution, trained assignment weights or solved project results are published.

## Present and read

- Right arrow / Page Down / Space: reveal the next layer, then advance.
- Left arrow / Page Up: return one layer, then the previous completed scene.
- **A** or **Tout montrer**: reveal the complete current scene.
- **T** / **Histoire & questions**: searchable scenes, six acts and direct question links.
- **D**: explanatory detail. **F**: fullscreen. Animations can be disabled; reduced-motion preferences are respected.

The URL preserves scene and reveal step. The offline HTML needs no external scripts or fonts. The PDF shows every scene fully revealed and includes question explanations in appendices. Interactions and actual timing export require HTML. Essential formulas and limitations remain visible in the scene; the detail dialog provides supplementary context.

## Sources and build

| File | Role |
|---|---|
| `source/content.py` | Six acts, dialogue, questions and scientific references |
| `source/story_art.py` | Original staged SVG artwork and fictional Alice |
| `source/diagrams.py` | Quantitative figures and interactive panels |
| `source/course.js`, `source/course.css` | Reveals, navigation, questions and visual layout |
| `SOURCES.md`, `references.json`, `references.bib` | Reading guide and citations |
| `TEACHING-DESIGN.md` | Scope and educational choices |
| `verification/checks.json` | Browser, numerical and PDF checks |
| `lab/` | Official assignment and student-only materials |

From this folder, install `source/requirements.txt` and a Playwright Chromium or local Chrome, then run:

```sh
python source/build_course.py
python source/audit_course.py
python source/audit_lab.py
```

The course generator creates HTML and both PDFs. The audit checks geometry, reveal navigation, numerical interactions, all six question answers, actual timing/CSV export and printable content. GitHub Pages serves `main` at the existing URL. Keep rebuilt HTML, PDFs and sources together.

Prepared with AI assistance and checked with the documented source, arithmetic and browser audits. Third-party research is linked, not redistributed.
