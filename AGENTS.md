# Agent Guidelines for al-folio

A simple, clean, and responsive Jekyll theme for academics.

## CV Blog Visual Pipeline

This branch also contains a CV-owned research blog harness. For Flow Matching or
other tutorial posts, work only in this worktree:

`/Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline`

Do not edit `/Users/quan238/personal/cv` directly for this pipeline. Use
`codex/cv-research-blog-visual-pipeline` unless a new branch is needed after the
current PR is merged.

Before drafting or publishing a research tutorial, read:

- `codex/skills/cv-research-blogger/SKILL.md`
- `codex/skills/cv-research-blogger/visual_quality.md`
- `_blog_work/<series-slug>/manifest.yml`
- `_blog_work/<series-slug>/SESSION_BOOTSTRAP.md` when present
- `_blog_work/<series-slug>/visual_sources.yml`
- `_blog_work/<series-slug>/series_tasks.yml` when present
- `_blog_work/<series-slug>/HANDOFF.md` when present
- `_blog_work/<series-slug>/series_prompt.md` when present

Keep WIP to one active blog part or visual redesign. The repo files above are
the durable handoff between sessions. A post is not publish-ready unless its
visual plan contains external visual references, figure briefs, local assets or
Mermaid source, alt text, evaluator notes, and passing checker/build evidence.

For this pipeline, treat `_blog_work/<series-slug>/series_tasks.yml` as the
single source of truth for active work. A task can move to `passing` only after
its verification commands pass and the evidence is written into the task list or
handoff. Use `python3 scripts/blog_pipeline/check_harness.py <series-slug>` as
the cold-start harness check before a new writing or visual-design session.

## Quick Links by Role

- **Are you a coding agent?** → Read [`.github/copilot-instructions.md`](.github/copilot-instructions.md) first (tech stack, build, CI/CD, common pitfalls & solutions)
- **Customizing the site?** → See [`.github/agents/customize.agent.md`](.github/agents/customize.agent.md)
- **Writing documentation?** → See [`.github/agents/docs.agent.md`](.github/agents/docs.agent.md)
- **Need setup/deployment help?** → [INSTALL.md](INSTALL.md)
- **Troubleshooting & FAQ?** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Customization & theming?** → [CUSTOMIZE.md](CUSTOMIZE.md)
- **Quick 5-min start?** → [QUICKSTART.md](QUICKSTART.md)

## Essential Commands

### Local Development (Docker)

The recommended approach is using Docker.

```bash
# Initial setup & start dev server
docker compose pull && docker compose up
# Site runs at http://localhost:8080

# Rebuild after changing dependencies or Dockerfile
docker compose up --build

# Stop containers and free port 8080
docker compose down
```

### Pre-Commit Checklist

Before every commit, you **must** run these steps:

1.  **Format Code:**
    ```bash
    # (First time only)
    npm install --save-dev prettier @shopify/prettier-plugin-liquid
    # Format all files
    npx prettier . --write
    ```
2.  **Build Locally & Verify:**

    ```bash
    # Rebuild the site
    docker compose up --build

    # Verify by visiting http://localhost:8080.
    # Check navigation, pages, images, and dark mode.
    ```

## Critical Configuration

When modifying `_config.yml`, these **must be updated together**:

- **Personal site:** `url: https://username.github.io` + `baseurl:` (empty)
- **Project site:** `url: https://username.github.io` + `baseurl: /repo-name/`
- **YAML errors:** Quote strings with special characters: `title: "My: Cool Site"`

## Development Workflow

- **Git & Commits:** For commit message format and Git practices, see [.github/GIT_WORKFLOW.md](.github/GIT_WORKFLOW.md).
- **Code-Specific Instructions:** Consult the relevant instruction file for your code type.

| File Type                                     | Instruction File                                                                                |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Markdown content (`_posts/`, `_pages/`, etc.) | [markdown-content.instructions.md](.github/instructions/markdown-content.instructions.md)       |
| YAML config (`_config.yml`, `_data/`)         | [yaml-configuration.instructions.md](.github/instructions/yaml-configuration.instructions.md)   |
| BibTeX (`_bibliography/`)                     | [bibtex-bibliography.instructions.md](.github/instructions/bibtex-bibliography.instructions.md) |
| Liquid templates (`_includes/`, `_layouts/`)  | [liquid-templates.instructions.md](.github/instructions/liquid-templates.instructions.md)       |
| JavaScript (`_scripts/`)                      | [javascript-scripts.instructions.md](.github/instructions/javascript-scripts.instructions.md)   |

## Common Issues

For troubleshooting, see:

- [Common Pitfalls & Workarounds](.github/copilot-instructions.md#common-pitfalls--workarounds) in copilot-instructions.md
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions
- [GitHub Issues](https://github.com/alshedivat/al-folio/issues) to search for your specific problem.
