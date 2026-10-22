# Embedded AI practical — Student materials

**Author: Roland Cédric TAYO** — INEM, 2026–2027. Teaching language: French.

**Start here:** https://rolln7drktayau.github.io/courses/embedded-ai/lab/

## Documents

| File | Purpose |
|---|---|
| `assignment.pdf` | Official assignment: objectives, equations and symbol reminders, implementation, deployment, experiments, rules and deliverables (13 pages) |
| `report-guidelines.pdf` | Scientific report requirements, 15-page limit and writing recommendations (3 pages) |
| `article-example.pdf` | English article-format illustration, not a completed TD experiment (5 pages) |
| `article-template.zip` | Importable free Overleaf project: template, example, bibliography and figure sources |
| `article-template/` | The same article sources, browsable in GitHub |
| `student-materials.zip` | Downloadable documents and Overleaf archive together |

Read [COMMENCER.md](COMMENCER.md) for prerequisites, hardware, progression and the scope of the research.

## Target hardware

Raspberry Pi running Linux only. For about 35 students and 14 boards, seven teams of five each need at least one Pi, a suitable power supply, OS storage (normally microSD), and network access or a screen and keyboard. Record the exact Pi and OS; do not rank different board models by raw latency. No Nucleo, sensor or accelerator is required.

## First steps

1. Read `assignment.pdf`, identify your Raspberry Pi and follow the module's December submission calendar. The technical settings, tolerances and measurement procedure are fixed in the assignment.
2. Create a private GitHub repository for your group. Invite all group members and **rolln7drktayau**. Verify that the invitation is accepted.
3. Use Python 3 for PC data and training, and C for inference and optimisation. Install Git, Python, and GCC/Make for C builds, including on the Pi. Only inference is ported to C. No ready-made model environment is supplied.
4. Implement the signal generator described in the assignment. Split independent sequences before windowing and calculate normalisation statistics only on training observations. Plot and check the signals before training.
5. Follow the paper exercises in assignment sections 8 and 9: calculate a small case, write its function, test and explain it. Then assemble and train the model, compare the baselines and plot results. Port inference to C, verify Python-PC/C-PC/C-Pi agreement, then measure.
6. Investigate one dense-projection hypothesis, retain raw measurements, version code/configurations/results and explain negative findings as carefully as positive ones.

No dataset for the TD, pretrained model, trained weights, training code or deployment solution is supplied. Students generate the TD signals from the equations and implement the project themselves. The illustrative sine trace in the article template is **not** the TD dataset and must not be submitted as a project result.

## Rules and delivery

The assignment is authoritative. Implement model calculations, differentiation and training without an AI framework, automatic differentiation or a matrix library doing the required work. Standard-library utilities, board tools and plotting/analysis tools are permitted as specified in the PDF. Declare substantial assistant or external-code assistance and be able to explain and verify everything submitted.

Prefer English identifiers, comments and commit messages. Keep pushed milestones, peer-reviewed changes, tests and experiment manifests. Deliver a runnable repository, raw data and measurements, figures, a report and individual contribution evidence. Invite teacher account **rolln7drktayau**.

Keep a short function worksheet with handwritten inputs, calculation and result, its automated test and the function's role. Implement Makefile targets `test-c`, `inference` and `benchmark`, and document run arguments and exported file formats. A target must compile or test the real project; pushing to GitHub does not itself execute it on the Pi.

Report: **15 pages maximum in total**, including references and appendices; aim for 6–10 useful pages. Clear English is recommended; free Overleaf is optional. Provide the complete report sources and figures. Full expectations are in the PDFs.

## Free tools and original sources

- Git: https://git-scm.com/downloads/
- Python 3: https://www.python.org/downloads/
- GCC and GNU Make: https://gcc.gnu.org/ and https://www.gnu.org/software/make/manual/make.html
- Python random and CSV documentation: https://docs.python.org/3/library/random.html and https://docs.python.org/3/library/csv.html
- Raspberry Pi Imager and OS: https://www.raspberrypi.com/software/
- Raspberry Pi setup, power and storage: https://www.raspberrypi.com/documentation/computers/getting-started.html
- SSH and file transfer: https://www.raspberrypi.com/documentation/computers/remote-access.html
- Monotonic timing in Python: https://docs.python.org/3/library/time.html#time.perf_counter_ns
- Unit tests in Python: https://docs.python.org/3/library/unittest.html
- GitHub Actions: https://docs.github.com/en/actions/get-started/quickstart
- Matplotlib, for figures only: https://matplotlib.org/stable/install/index.html
- Overleaf first project / ZIP import: https://docs.overleaf.com/getting-started/your-first-project
- Original TSMixer paper: https://arxiv.org/abs/2303.06053
- Authors' original implementation, for reading and comparison rather than copying the required model: https://github.com/google-research/google-research/tree/master/tsmixer
- Gradient checks: https://cs231n.github.io/neural-networks-3/
- Optimised BLAS, as a separate comparator with equivalent operations and thread count: https://github.com/OpenMathLib/OpenBLAS

For the article, upload `article-template.zip` into Overleaf; select `main.tex` and pdfLaTeX. Select `example.tex` temporarily to inspect the format example. The free plan suffices using manual source exports and GitHub versioning; no paid integration is required.

This directory and its archives contain student-facing material only. The instructor's solved implementation, checkpoints, training results, benchmarks and completed results article are not published here.

## Fixed experiment contract

No instructor-selected technical threshold is required. Follow assignment sections 3–5: deterministic initial training, fixed numerical tolerances, the analytical simulator comparator, and the same C code/`-O2` comparison on PC and Pi. For each shape and campaign, warm up 100 calls, double the reference call count K until at least 100 ms (cap 2^24), then use K for both variants. Run three campaigns of ten alternating pairs; retain every raw duration and K. Plot median and min–max. A gain is not required; rigorous negative results must be explained. Failure diagnostics are in COMMENCER.md.
