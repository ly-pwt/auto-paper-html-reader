---
name: auto-paper-html-reader
description: Read academic papers from a title, arXiv link, PDF, or local source; analyze the paper, related work, experiments, limitations, optional code repository, and implementation evidence; then publish a structured Chinese HTML reading report in the current project so it is available at http://127.0.0.1:8000/<paper-name>.html. Use when the user asks Codex to read, analyze, summarize, critique, or produce an HTML report for a research paper.
---

# Auto Paper HTML Reader

Use this skill to turn one paper into a structured Chinese HTML reading report. Treat it as a Codex version of the AutoPaperReader workflow, but write HTML instead of Markdown.

## Output Contract

- Save the final report as a standalone `.html` file in the current project root unless the user gives another server root.
- Treat the current working directory as the project root.
- The report must be reachable as `http://127.0.0.1:8000/<paper-name>.html` when a static server is running from the project root.
- Name the file from the paper title or method name, sanitized for a URL and filesystem. Prefer short ASCII slugs for reliability, for example `attention-is-all-you-need.html`; if the user explicitly asks for a Chinese filename, use that exact name when safe.
- Start or reuse a static server with `python3 -m http.server 8000` from the project root when the user expects to open the report in a browser.
- Keep downloaded sources under `sources/<paper-slug>/` and generated reports in the project root.
- Every substantive paragraph in the report must have a nearby "大白话" button. Implement this by wrapping paragraphs with `class="explainable"` and adding a `data-plain` attribute containing a plain-language explanation of that paragraph.
- Add a dedicated technical-roadmap section that explains the paper's main technical pipeline in detail, including inputs, modules, training/inference flow, outputs, and where the key technical risk lives.
- Extract and embed the paper's key technical figures/tables into the HTML whenever possible. Do not merely describe major figures in prose. Save figure assets under `sources/<paper-slug>/figures/` and reference them with relative paths.
- Crop figure/table assets precisely. This is a hard requirement, not a preference. Do not save or embed an entire PDF page, browser viewport, desktop screenshot, or whole paper page when only one figure/table is needed. Each image file must contain only the target figure/table plus its caption if useful for context.
- If exact extraction is hard, first render the page or take a screenshot only as an intermediate source, then crop that intermediate image down to the specific figure/table before embedding. Never embed the intermediate full-page render in the final report.
- If a figure/table cannot be cropped tightly after reasonable effort, omit the image and explain the limitation in prose rather than embedding a full-page render.
- Add a dedicated related-work comparison section. It must compare the paper against closest prior work, strong baselines, benchmark/dataset papers, and infrastructure/foundation papers that the work builds on. Analyze both similarities and differences instead of only listing citations.
- Add a dedicated writing-logic section. It must explain the paper's rhetorical structure: how the introduction sets up the problem, how related work narrows the gap, how method sections answer the gap, how experiments support the claims, and where the paper's strongest narrative turns happen.

Read [references/report-contract.md](references/report-contract.md) before writing the report. Use [assets/report-template.html](assets/report-template.html) as the page skeleton.

## Workflow

1. Resolve the paper.
   - If the user gives an arXiv URL, extract the arXiv id.
   - If the user gives a title or method name, search the web for the official paper page, preferring arXiv.
   - If the user gives a PDF or local file, use it directly and infer metadata from the document.
   - Capture title, authors, affiliations, date/version, abstract, links, and any project/code links.

2. Gather source material.
   - Prefer arXiv e-print/LaTeX source over PDF text when available.
   - Store paper material under `sources/<paper-slug>/arxiv/`.
   - If source is unavailable, use PDF extraction and clearly label source limitations in the report.
   - Clone public code, if found, into `sources/<paper-slug>/code/`. If cloning fails, continue and record the reason.

3. Read the paper deeply.
   - Build the section outline from `\section`, `\subsection`, PDF headings, or obvious document structure.
   - Read introduction, related work, method, experiments, limitations, and conclusion.
   - Inspect figures and tables when available; architecture diagrams and result tables often carry critical information.
   - Identify the key figures/tables that explain the paper's task, dataset construction, model architecture, training data, augmentation, inference pipeline, and main results.
   - Extract or render those key figures/tables into browser-viewable image files under `sources/<paper-slug>/figures/`. Preserve figure/table numbers in filenames when possible, and include words such as `figure`, `table`, or `crop` in filenames to make the intent obvious.
   - Use tight crops: include the target Figure/Table and optionally its caption, but exclude unrelated page text, neighboring figures, browser chrome, desktop background, and full-page whitespace.
   - If exact extraction is hard, use a page crop or user-provided screenshot, then crop that image down to the needed figure/table before embedding it.
   - If one screenshot contains multiple needed figures/tables, split it into separate cropped image files when the report discusses them separately.
   - Extract key formulas faithfully, preserving the paper's notation in LaTeX.

4. Analyze context and novelty.
   - Identify the closest prior work and the exact relationship: new problem framing, new module, new objective, new data recipe, stronger scaling/evaluation, or a combination.
   - Use web search for 3-8 directly related papers when the claim depends on external context. Include:
     - closest prior work;
     - strongest baselines;
     - dataset/benchmark papers;
     - infrastructure or foundation-model papers that make this paper possible.
   - Build a comparison matrix with dimensions such as task setting, input/output, data source, model family, supervision signal, evaluation protocol, strengths, limitations, and how the current paper differs.
   - Separate author claims from Codex's own critique.

5. Check code when available.
   - Read README, configs, training/eval scripts, core model/loss/sampler files, license, and dependency files.
   - Compare implementation with the paper: consistent, inconsistent, or paper-omitted engineering details.
   - Extract real batch size, sequence length, steps, optimizer, precision, world size, hardware assumptions, and reproducibility status.

6. Write the HTML report.
   - Use the template asset as a starting point, but fill all sections from the report contract.
   - Make the report self-contained: inline CSS, semantic headings, tables for experiments, and collapsible/compact blocks for formulas or code snippets.
   - For each paragraph, write both the normal analytical paragraph and its `data-plain` explanation. The plain explanation should be concrete, short, and jargon-light, aimed at a smart non-specialist.
   - Build the technical roadmap as a step-by-step route through the method. Prefer a visual HTML flow made of ordered cards over a generic prose summary.
   - Embed the main technical-route figure directly in the technical-roadmap section and explain each visible component of the figure.
   - Add a figure-explanation gallery for the important extracted figures/tables. Each item must include the image, original caption or figure/table number, a technical explanation, and a plain-language explanation.
   - Add the related-work comparison matrix and a paragraph-by-paragraph synthesis of what the current paper inherits, changes, and proves beyond those works.
   - Add the writing-logic analysis as a section that follows the paper's order and explains the argumentative function of each major section.
   - Link local figures with relative paths such as `sources/<paper-slug>/arxiv/figures/model.pdf` if they can render in the browser; otherwise describe them.
   - Do not paste long copyrighted passages. Quote only short source excerpts when needed and otherwise paraphrase.

7. Run the report quality hook.
   - After writing the HTML, run:
     `python3 skills/auto-paper-html-reader/scripts/report_quality_hook.py <report.html>`
   - If the hook reports missing sections, missing figures, too few `data-plain` explanations, thin sections, broken local images, too few tables, or suspected full-page/viewport images, edit the HTML and figure assets to fix the issue.
   - A suspected full-page/viewport image is a failing error. Replace it with a tight crop of the corresponding figure/table and rerun the hook.
   - Rerun the hook after each edit. Do not deliver the report until the hook passes, unless the user explicitly asks to stop early.

8. Verify delivery.
   - Confirm the HTML file exists at the project root.
   - If a static server is needed and no server is running, start one from the project root on port 8000.
   - Return the local URL and a brief note about source/code availability and any uncertainty.

## Style

- Write primarily in Simplified Chinese; preserve key terms in English, such as attention, KV cache, contrastive loss, benchmark, baseline, and ablation.
- Use professional but readable analysis. Avoid marketing language.
- Keep "作者认为" and "我认为" clearly distinct.
- Mark estimates explicitly with `估算`.
- Do not invent missing datasets, formulas, hardware, or repository details.
