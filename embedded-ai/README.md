# Embedded AI — From requirements to evidence

**Author: Roland Cédric TAYO** — INEM, 2026–2027.

A three-hour course for future embedded-systems engineers. The teaching language is **French**; the repository directory and technical source organisation use English names.

- **Guided course-building workshop:** https://rolln7drktayau.github.io/courses/embedded-ai/workshop/
- **Interactive presentation:** https://rolln7drktayau.github.io/courses/embedded-ai/
- **PDF slides:** https://rolln7drktayau.github.io/courses/embedded-ai/course.pdf
- **Two-page teaching plan:** https://rolln7drktayau.github.io/courses/embedded-ai/course-plan.pdf
- **Practical assignment and student resources:** https://rolln7drktayau.github.io/courses/embedded-ai/lab/

The main presentation provides permanent **TD** and **PDF** links in its navigation bar. **Ressources** opens the course sources, student assignment files, article-template sources and bibliography. The `lab/` directory contains the assignment, report instructions and article template, with no instructor implementation or experiment results.

## Scope

32 core slides; **180 minutes including a ten-minute break**, the five quizzes and class discussion. This synthesis introduces the broader **14-hour lecture / 14-hour practical module**. It is not the entire module. Twenty-one optional slides provide architectural extensions, research reading, references, a glossary and quiz explanations.

The main path follows one complete 2 → 2 → 1 teaching network, then deployment, resource budgets, two optimisation levers and experimental evidence. The assignment uses its own reduced Mixer; the teaching network and browser experiment are independent examples, not the assignment solution.

There are 23 primary or official scientific sources. Established publications, preprints and documentation are labelled separately. Pedagogical references from MIT, Harvard and Carnegie Mellon and the choices drawn from them are documented in [TEACHING-DESIGN.md](TEACHING-DESIGN.md). Diagrams are original.

## Concrete interactions

- Change the teaching network inputs and observe hidden activations and output.
- Change a one-weight learning rate; see both error reduction and overshoot.
- Change weight representation and distinguish Flash from working SRAM.
- Observe quantisation error and global speedup with analytical examples.
- Run two array-sum implementations **in the current browser**: verify equal results, warm up, alternate seven paired campaigns, inspect median/min/max and download all 14 timing rows as CSV. No result is prefilled, and none is labelled as Raspberry Pi or MCU performance.

Core quizzes are at slides **6, 13, 19, 26 and 31**. They require an architecture, parameter/MAC count, peak-RAM calculation, global-time calculation and a justified system decision. The final multicriteria table is explicitly fictitious. The assignment is a regression task and uses different quality metrics.


## Files

| Path | Purpose |
|---|---|
| `index.html` | Self-contained, offline-capable dynamic presentation |
| `course.pdf` | 16:9 slides, references and PDF bookmarks |
| `course-plan.pdf` | A4 schedule, prerequisites and learning outcomes |
| `lab/` | Student assignment, report documents, Overleaf sources and downloadable materials |
| `SOURCES.md` | Scientific reading guide, contributions and limitations |
| `TEACHING-DESIGN.md` | Learning path and educational references |
| `references.json`, `references.bib` | Reference metadata |
| `source/content.py` | Course text and references |
| `source/diagrams.py` | Original SVG diagrams |
| `source/course.css`, `source/course.js` | Layout, navigation, quizzes and analytical demonstrations |
| `source/build_course.py` | Rebuild the public HTML and PDFs |
| `source/audit_course.py` | Layout, navigation and arithmetic checks |
| `verification/checks.json` | Results of local automated checks |

## Navigation

Arrow keys / Page Up / Page Down / Space navigate. `T` or **Plan & questions** opens the five guiding questions, direct links to all five quizzes and searchable contents, `D` opens further explanations and `F` toggles fullscreen. Animations can be disabled, and the system reduced-motion preference is respected. The course itself needs no remote script, font or telemetry. Opening article links needs Internet.

## Rebuild

From this directory:

```sh
python -m pip install -r source/requirements.txt
python -m playwright install chromium
python source/build_course.py
python source/audit_course.py
```

The browser audit checks every core and optional slide, numerical interactions, all quiz explanations, the live timing/CSV experiment and navigation. The build uses an installed Chrome on Windows when available, or Playwright Chromium otherwise. Students only need a browser or PDF reader, not these build dependencies.

## Publication

GitHub Pages publishes the repository root from `main`; `.nojekyll` disables Jekyll processing. Commit the rebuilt HTML and PDFs together. Relative links keep the presentation and PDF under the same project path. No instructor solution or private TD artefact is included in this directory.

The materials were prepared with AI assistance, followed by the documented reference, mathematical and browser checks. The PDF contains the initial numerical examples and quiz explanations; browser interactions and raw timing export require the HTML. Third-party papers are linked, not redistributed. No blanket licence is asserted here for those papers.

## Active workshop route

[workshop/](workshop/) provides a 210-minute guided inquiry for about 35 students in seven teams of five, with an optional 420-minute full-day extension. Students calculate a common case, investigate balanced complementary questions, challenge evidence and assemble their own course from exported JSON files. Individual exit questions check transfer beyond the team's topic.

The page supports local drafts, group JSON/Markdown export and manual assembly of seven chapters as HTML/Markdown or printable PDF. It has no backend or cross-device synchronisation. The download bundle contains the reference presentation for offline consultation, student worksheets, illustrative data and a blank evidence-repository template. The private facilitation guide and the instructor's project solution are outside the repository.

Use the workshop instead of adding it on top of the three-hour presentation. Rebuild public workshop documents with `python source/build_workshop.py` after rebuilding the presentation; verify with `python source/audit_workshop.py`.
