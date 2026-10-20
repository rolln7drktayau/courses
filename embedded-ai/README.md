# Embedded AI — From requirements to evidence

**Author: Roland Cédric TAYO** — INEM, 2026–2027.

A three-hour course for future embedded-systems engineers. The teaching language is **French**; the repository directory and technical source organisation use English names.

- **Interactive presentation:** https://rolln7drktayau.github.io/courses/embedded-ai/
- **PDF slides:** https://rolln7drktayau.github.io/courses/embedded-ai/course.pdf
- **Two-page teaching plan:** https://rolln7drktayau.github.io/courses/embedded-ai/course-plan.pdf

The main presentation also provides a permanent **PDF** link in its navigation bar.

## Scope

44 core slides, five reasoning questions and interactive demonstrations; 180 minutes including a ten-minute break. Ten appendices provide references, a glossary and explanations. The course covers a selective history, data and model primitives, hardware/memory/latency/energy budgets, optimisation, deployment, reliability, security and research methodology.

There are 21 primary or official sources, verified on 20 October 2026. Established publications, preprints and vendor documentation are labelled separately. Historical foundations are explicitly distinguished from 2023–2026 research. All diagrams are original; analytical illustrations are not presented as board measurements.

## Files

| Path | Purpose |
|---|---|
| `index.html` | Self-contained, offline-capable dynamic presentation |
| `course.pdf` | 16:9 slides, references and PDF bookmarks |
| `course-plan.pdf` | A4 schedule, prerequisites and learning outcomes |
| `SOURCES.md` | Reading guide, contributions and limitations |
| `references.json`, `references.bib` | Reference metadata |
| `source/content.py` | Course text and references |
| `source/diagrams.py` | Original SVG diagrams |
| `source/course.css`, `source/course.js` | Layout, navigation, quizzes and analytical demonstrations |
| `source/build_course.py` | Rebuild the public HTML and PDFs |
| `source/audit_course.py` | Layout, navigation and arithmetic checks |
| `verification/checks.json` | Results of local automated checks |

## Navigation

Arrow keys / Page Up / Page Down / Space navigate. `T` opens the searchable contents, `D` opens further explanations and `F` toggles fullscreen. Animations can be disabled, and the system reduced-motion preference is respected. The course itself needs no remote script, font or telemetry. Opening article links needs Internet.

## Rebuild

From this directory:

```sh
python -m pip install -r source/requirements.txt
python -m playwright install chromium
python source/build_course.py
python source/audit_course.py
```

The build uses an installed Chrome on Windows when available, or Playwright Chromium otherwise. Students only need a browser or PDF reader, not these build dependencies.

## Publication

GitHub Pages publishes the repository root from `main`; `.nojekyll` disables Jekyll processing. Commit the rebuilt HTML and PDFs together. Relative links keep the presentation and PDF under the same project path. No instructor solution or private TD artefact is included in this directory.

The materials were prepared with AI assistance, followed by the documented reference, mathematical and browser checks. Third-party papers are linked, not redistributed. No blanket licence is asserted here for those papers.
