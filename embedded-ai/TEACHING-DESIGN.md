# Learning design and educational references

Roland Cédric TAYO · INEM · Updated 21 October 2026.

## Purpose and limits

The 180-minute synthesis introduces a 14-hour lecture / 14-hour practical module. The practical project continues with independent work. Core objectives are observable: explain a complete inference, distinguish training from deployment, calculate resource budgets, verify an optimisation and defend reproducible evidence.

## Published educational references

These are sources of educational ideas, not a ranking or an assertion of equivalent coverage.

- [MIT 6.5940 — TinyML and Efficient AI Computing, Fall 2026](https://hanlab.mit.edu/courses/2026-fall-65940): explicit prior ML/architecture knowledge, extended efficiency topics, labs and a final project. Adaptation here: learn the prerequisites, perform bounded experiments and separate advanced reading from the short common path.
- [Harvard — Deploying TinyML](https://pll.harvard.edu/course/deploying-tinyml): programming and deploying a complete application on a physical microcontroller. Adaptation here: make the PC-to-device chain visible before discussing optimisation. No specific commercial kit is imposed by these slides.
- [Carnegie Mellon — 18-444 Embedded Machine Learning](https://courses.apps.ece.cmu.edu/18444): neural architectures, training, model downsizing and constrained microcontroller inference. Adaptation here: connect model structure to deployment and its measured constraints.

The slides, diagrams and examples in this repository are original. The source courses have different durations and prerequisites; their topic lists are not compressed into a three-hour claim of mastery.

## Main path

| Time | Activity | Evidence |
|---|---|---|
| 0–20 min | Human need, historical obstacles, computation placement | Justify a local architecture against two requirements |
| 20–55 min | A complete 2 → 2 → 1 network and the project bridge | Trace an output, a loss and a gradient step; count parameters and MAC |
| 55–85 min | Deployment and resource budgets | Explain PC/device equivalence and calculate peak SRAM |
| 85–95 min | Break | Ten minutes included |
| 95–130 min | Quantisation, data reuse and browser timing | Verify outputs, compare raw observations and calculate global gain |
| 130–160 min | Hypotheses, reliability, Git/CI and a research paper | Specify controls, failure cases and provenance |
| 160–180 min | Constrained design decision and outcomes | Justify a choice and propose a test that could disprove it |

## Honest examples and research

The toy network has nine parameters. Its given numbers are illustrative, not a trained checkpoint of the project. One learning demonstration updates only one output weight with hidden values fixed; the assignment requires the full specified gradients.

The live micro-experiment compares a JavaScript loop and `reduce` on the same deterministic 4,096-value Float64Array. It checks correctness, warms up, uses a common measured batch size, alternates seven paired campaigns and exports raw observations. It measures only the current browser. It does not infer energy, MCU cycles or Raspberry Pi timings, and it provides no optimised projection implementation for the assignment.

The final decision table is fictional and independent of the regression project. Its observed p95 is not a worst-case guarantee. Learning to experiment and explaining a negative result are assessed; an accepted publication or a novel speed record is not promised.

The 21 optional slides keep convolution, recurrence, attention, KV-cache details, compression and current research available without requiring their presentation within the core time. The PDF displays initial examples and quiz explanations; interactions and CSV export require HTML.
