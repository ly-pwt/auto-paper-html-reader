# HTML Report Contract

The final report must be a standalone HTML page with inline CSS and the following content. Use Chinese section titles and preserve key technical terms in English.

## Required Page Structure

1. `header`
   - Paper title in Chinese if a reliable translation is possible.
   - Original English title.
   - Authors, affiliations, date/version, arXiv or DOI URL, PDF/source/code links.
   - A short status strip: source type, code availability, confidence level.

2. `section#summary`
   - Chinese contribution summary in 1-2 precise sentences.
   - Short English contribution excerpt or paraphrase, with source location such as abstract, introduction, or conclusion.
   - One sentence for non-specialists using a concrete analogy.

3. `section#technical-roadmap`
   - A standalone, detailed explanation of the paper's main technical route.
   - Embed the paper's primary technical-route image or architecture figure if available, using a local relative image path.
   - Use a visible flow of step cards, for example `input -> representation -> model/module -> training objective -> inference/selection -> output`.
   - For each step, explain:
     - What enters this step.
     - What transformation happens.
     - Which model, dataset, formula, loss, retrieval/indexing, optimization, or algorithm component is responsible.
     - What exits this step.
     - Why this step matters and what can go wrong.
   - Include a short "大白话总览" that explains the whole route as if explaining it at a whiteboard.
   - When the paper has a major architecture figure, include it and explain each visible block, arrow, and decision point.

4. `section#contributions`
   - Motivation and problem discovery.
   - Method innovations.
   - Core experimental conclusions.

5. `section#related-work-comparison`
   - Compare the current paper with related work, not merely list citations.
   - Include closest prior work, strong baselines, benchmark/dataset papers, and infrastructure/foundation papers the work depends on.
   - Provide a comparison table. Recommended columns:
     - Work;
     - Role in this paper;
     - Task/input/output;
     - Data or model basis;
     - What is similar;
     - What is different;
     - What the current paper proves beyond it;
     - Remaining limitation.
   - After the table, synthesize the relationship:
     - What this paper inherits.
     - What it changes.
     - What it newly validates.
     - What remains uncovered.
   - Mark external facts with paper titles and URLs/arXiv ids when known.

6. `section#writing-logic`
   - Analyze the paper's writing and argument structure.
   - Explain how the introduction sets up the pain point and gap.
   - Explain how related work positions the paper.
   - Explain how dataset/method sections answer the gap.
   - Explain how experiments support or weaken each claim.
   - Name the strongest narrative turn, the weakest transition, and any claim that relies on later evidence.
   - Include a visible ordered timeline of the paper's logic.

7. `section#related-work`
   - List 5-10 central references when available.
   - For each: citation label or author/year, title if known, and its role in this paper's argument.

8. `section#critical-analysis`
   - Relationship to closest prior work.
   - Whether the paper is a module-level change, method combination, data/scale recipe, new framing, or genuinely new mechanism.
   - Similar earlier or concurrent ideas when evidence exists.
   - Fragile claims, unsupported assumptions, and limitations.
   - Clearly distinguish "作者认为" from "我认为".

9. `section#method`
   - Algorithm flow.
   - Key formulas in MathJax-compatible LaTeX inside `<div class="formula">`.
   - Model/backbone/components.
   - Training and inference data flow.
   - Compute requirements: GPU/TPU type and count, training time, token/step count, batch size, sequence length. Mark estimates as `估算`.

10. `section#experiments`
   - Datasets: name, size, task type, split if available.
   - Metrics: what each metric measures.
   - Main results: use HTML tables for important comparisons.
   - Ablations: what hypothesis each ablation tests.
   - Result interpretation: author interpretation first, Codex analysis second.

11. `section#figures`
   - Important figures/tables and why they matter.
   - Embed the important extracted figures/tables as images whenever browser-renderable.
   - Save extracted/cropped/user-provided images under `sources/<paper-slug>/figures/`.
   - Each embedded image must be a tight crop of the target figure/table, not an entire PDF page, browser viewport, or whole screen.
   - Include the caption only when it helps identify the figure/table; otherwise keep the crop focused on the visual content.
   - If a source page contains multiple important figures/tables, crop and save them as separate files unless the paper itself presents them as one combined figure/table.
   - For each figure/table, include:
     - Local image.
     - Figure/table number and original caption if available.
     - What the reader should look at first.
     - Detailed technical explanation.
     - One `p.explainable[data-plain]` plain-language explanation.
   - If a source figure is PDF-only or unavailable, create a page crop or screenshot when possible, then crop tightly to the relevant figure/table. Only fall back to prose when extraction/rendering is impossible.

12. `section#code-observations`
    - Include only when code was found.
    - Repository URL, commit hash if known, license, weights/data availability.
    - Implementation matches paper: consistent / inconsistent / not found.
    - Paper-omitted engineering details.
    - True compute/config observations from code.
    - Reproducibility rating: high / medium / low, with reasons.

13. `section#open-questions`
    - Any unresolved ambiguities, missing artifacts, or places where the report relies on estimates.

## Plain-Language Explanation Buttons

- Every substantive paragraph must be written as:

```html
<p class="explainable" data-plain="这里写给非专业读者看的大白话解释。">这里写正常技术分析。</p>
```

- The button text should be `大白话`.
- The expanded explanation should appear immediately after the paragraph.
- The explanation must not merely repeat the paragraph. It should reduce jargon, name the intuition, and use one concrete analogy when useful.
- Use this for paragraphs in all major sections, including summary, contributions, storyline, critical analysis, method, experiments, figures, code observations, and open questions.
- Do not add buttons to table cells, metadata cards, citations, or short list items unless the list item contains dense technical reasoning.

## HTML Requirements

- Include `<meta charset="utf-8">`.
- Include a responsive layout that works on desktop and mobile.
- Use a constrained reading width and tables with horizontal scroll.
- Include CSS classes: `.meta-grid`, `.pill`, `.callout`, `.formula`, `.table-wrap`, `.claim`, `.author-view`, `.agent-view`, `.explainable-wrap`, `.plain-toggle`, `.plain-explanation`, `.roadmap`, `.roadmap-step`, `.figure-panel`, `.figure-panel img`, `.figure-caption`, `.logic-timeline`, `.logic-step`, `.comparison-note`.
- Include a small inline script that adds/toggles the plain-language explanation buttons for all `.explainable[data-plain]` elements.
- Use accessible color contrast.
- Do not rely on external CDNs except optional MathJax. If MathJax is included, use the official CDN script and keep formulas readable without it.
- Put local source links as relative paths from the project root.

## Filename Rules

- Default: `<paper-title-slug>.html`, lowercase ASCII, hyphen-separated, max 80 characters before `.html`.
- Remove filesystem-unsafe characters: `/ \ : * ? " < > | # % & { } $ ! ' @ + =`.
- Collapse repeated spaces/hyphens.
- If the user requests a specific filename, use it after removing path separators.

## Report Quality Hook

- After generating or modifying a report, run:

```bash
python3 skills/auto-paper-html-reader/scripts/report_quality_hook.py <report.html>
```

- Treat a nonzero exit as a required revision request.
- Use the hook output as a checklist, then edit the HTML to add missing substantive sections/content.
- Rerun the hook until it passes before delivery.
