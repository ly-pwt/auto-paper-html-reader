# Auto Paper HTML Reader Skill

`auto-paper-html-reader` is a Codex skill for reading academic papers and publishing structured Chinese HTML reports.

It turns a paper title, arXiv link, PDF, or local paper file into a browser-readable report with:

- structured Chinese paper analysis
- embedded key technical figures and tables
- a detailed technical roadmap
- paragraph-level `大白话` explanations
- related-work comparison against prior work, strong baselines, datasets, and infrastructure papers
- writing-logic analysis of the paper's argument structure
- optional code implementation observations when a public repository exists
- a quality hook that checks the generated HTML and forces missing sections to be filled

## Repository Layout

```text
skills/
└── auto-paper-html-reader/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── assets/
    │   └── report-template.html
    ├── references/
    │   └── report-contract.md
    └── scripts/
        └── report_quality_hook.py
```

Generated reports and downloaded paper assets are intentionally ignored by git:

```text
*.html
sources/
```

## Install

Clone this repository, then copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/auto-paper-html-reader ~/.codex/skills/auto-paper-html-reader
```

Restart Codex or start a new session so the skill is discovered.

## Use

In Codex, ask:

```text
使用 auto-paper-html-reader 读这篇论文：https://arxiv.org/abs/1706.03762
```

Or provide a local PDF:

```text
使用 auto-paper-html-reader 读这篇论文：/path/to/paper.pdf
```

The skill writes a standalone HTML report into the current project root. If the project is served with:

```bash
python3 -m http.server 8000
```

the report will be available at:

```text
http://127.0.0.1:8000/<paper-name>.html
```

## Quality Hook

After generating a report, the skill must run:

```bash
python3 skills/auto-paper-html-reader/scripts/report_quality_hook.py <report.html>
```

The hook checks for:

- required sections
- technical roadmap
- related-work comparison
- writing-logic analysis
- embedded key figures
- `大白话` explanations
- result/comparison tables
- broken local image links
- thin required sections

If the hook fails, Codex should edit the HTML report to fill the missing content and rerun the hook until it passes.

## Manual Hook Check

You can run the hook yourself:

```bash
python3 skills/auto-paper-html-reader/scripts/report_quality_hook.py my-paper.html
```

For machine-readable output:

```bash
python3 skills/auto-paper-html-reader/scripts/report_quality_hook.py my-paper.html --json
```

## Notes

- This skill is meant to run inside Codex. GitHub itself cannot directly execute the skill from the webpage.
- Other users need to clone the repo and install/copy the skill into their Codex skills directory.
- Some tasks may require internet access for paper lookup, related-work verification, or public code repository inspection.
- Generated reports may contain local PDF/image paths and should normally not be committed.
