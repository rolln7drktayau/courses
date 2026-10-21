# Embedded AI practical — Student materials

**Author: Roland Cédric TAYO** — INEM, 2026–2027. Teaching language: French.

**Start here:** https://rolln7drktayau.github.io/courses/embedded-ai/lab/

## Documents

| File | Purpose |
|---|---|
| `assignment.pdf` | Official assignment: objectives, equations and symbol reminders, implementation, deployment, experiments, rules and marking scheme (13 pages) |
| `report-guidelines.pdf` | Scientific report requirements, 15-page limit and optional presentation bonuses (3 pages) |
| `article-example.pdf` | English article-format illustration, not a completed TD experiment (5 pages) |
| `article-template.zip` | Importable free Overleaf project: template, example, bibliography and figure sources |
| `article-template/` | The same article sources, browsable in GitHub |
| `student-materials.zip` | Downloadable documents and Overleaf archive together |

Read [COMMENCER.md](COMMENCER.md) for prerequisites, hardware, progression and the scope of the research.

## First steps

1. Read `assignment.pdf` and confirm the actual board and deadline with the teacher.
2. Create a private GitHub repository for your group. Invite all group members and **rolln7drktayau**. Verify that the invitation is accepted.
3. Choose your language and create your own environment. Install Git, a compiler or Python for PC work, and the actual board's toolchain. No ready-made model environment is supplied.
4. Implement the signal generator described in the assignment. Split independent sequences before windowing and calculate normalisation statistics only on training observations. Plot and check the signals before training.
5. Write the model, gradients and tests, train it and compare the required simple baselines. Then deploy your inference, verify numerical agreement and measure on the board.
6. Investigate one dense-projection hypothesis, retain raw measurements, version code/configurations/results and explain negative findings as carefully as positive ones.

No dataset for the TD, pretrained model, trained weights, training code or firmware solution is supplied. Students generate the TD signals from the equations and implement the project themselves. The illustrative sine trace in the article template is **not** the TD dataset and must not be submitted as a project result.

## Rules and delivery

The assignment is authoritative. Implement model calculations, differentiation and training without an AI framework, automatic differentiation or a matrix library doing the required work. Standard-library utilities, board tools and plotting/analysis tools are permitted as specified in the PDF. Declare substantial assistant or external-code assistance and be able to explain and verify everything submitted.

Prefer English identifiers, comments and commit messages. Keep pushed milestones, peer-reviewed changes, tests and experiment manifests. Deliver a runnable repository, raw data and measurements, figures, a report and individual contribution evidence. Invite teacher account **rolln7drktayau**.

Report: **15 pages maximum in total**, including references and appendices; aim for 6–10 useful pages. Optional bonus: readable English +0.5, careful scientific article presentation +0.5, complete recompilable free Overleaf sources +1. Final grade capped at 20/20; the core 20 points remain obtainable without these presentation options. Full expectations are in the PDFs.

## Free tools and original sources

- Git: https://git-scm.com/downloads/
- Python, if chosen: https://www.python.org/downloads/
- Python random and CSV documentation: https://docs.python.org/3/library/random.html and https://docs.python.org/3/library/csv.html
- STM32 tools, if applicable to the assigned board: https://www.st.com/en/development-tools/stm32cubeide.html
- Unit tests in Python: https://docs.python.org/3/library/unittest.html
- GitHub Actions: https://docs.github.com/en/actions/get-started/quickstart
- Matplotlib, for figures only: https://matplotlib.org/stable/install/index.html
- Overleaf first project / ZIP import: https://docs.overleaf.com/getting-started/your-first-project
- Original TSMixer paper: https://arxiv.org/abs/2303.06053
- Authors' original implementation, for reading and comparison rather than copying the required model: https://github.com/google-research/google-research/tree/master/tsmixer
- Gradient checks: https://cs231n.github.io/neural-networks-3/
- Optimised Cortex-M kernels, as an explicitly separate comparator: https://github.com/ARM-software/CMSIS-NN

For the article, upload `article-template.zip` into Overleaf; select `main.tex` and pdfLaTeX. Select `example.tex` temporarily to inspect the format example. The free plan suffices using manual source exports and GitHub versioning; no paid integration is required.

This directory and its archives contain student-facing material only. The instructor's solved implementation, checkpoints, training results, benchmarks and completed results article are not published here.
