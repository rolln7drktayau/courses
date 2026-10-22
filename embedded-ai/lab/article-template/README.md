# Academic article template — INEM — Roland Cédric TAYO

Upload this ZIP as a new Overleaf project. Select `main.tex` as the main document and pdfLaTeX as the compiler. No paid subscription or special compiler option is required. `main.tex` is your report template. To read the completed format example, select `example.tex` and recompile, then switch back to `main.tex`.

The style uses Elsevier's `elsarticle` manuscript class: one column, numbered sections, abstract, keywords, numbered references, figures and equations. It follows the manuscript spirit of ADARE; it is not a journal submission or an accepted paper.

Maximum final report length: **15 pages including references and appendices**. Aim for 6–10 useful pages. Clear English and a readable scientific article layout are recommended. Free Overleaf is optional; include the complete, recompilable sources and figures. See the separate French report instructions for full requirements.

The free Overleaf plan currently permits one invited collaborator plus the owner, and does not include GitHub integration (checked 20 October 2026). Use GitHub for team versioning and manually export/import sources; never share a password. Deposit `.tex`, `.bib`, figures and the matching PDF under `paper/` on GitHub. Invite the teacher account **rolln7drktayau** on GitHub.

The example is deliberately incomplete as an experiment. It contains **no trained-network results or board measurements**. The illustrative noisy sine trace in `data/` is separate from the TD simulator and must not be used as a student result. `plot_example.py` reads that CSV, computes the illustrated persistence errors and recreates the signal figure. Optional local reproduction: install `requirements-example.txt`, then run `python plot_example.py`. Python is not needed to compile the LaTeX.

Files: `main.tex` (student template), `example.tex` (format demonstration), `references.bib` (verify and extend), `figures/*.pdf` (vector illustrations), `data/illustrative_trace.csv`, `plot_example.py` and this README. No network code, training implementation or firmware is supplied. Replace every placeholder with your own work. Attribute any reused content.

Official help: https://docs.overleaf.com/getting-started/your-first-project
Class documentation: https://ctan.org/pkg/elsarticle
