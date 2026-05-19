# Flow Matching Export Policy

This series is developed in the harness checkout:

`/Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline`

The personal al-folio checkout is the publication target:

`/Users/quan238/personal/cv`

Do not edit the personal checkout during planning, drafting, code runs, visual
review, or publish checks. The harness remains the workshop until the user gives
explicit export approval.

## Harness-Only Files

These files stay in the harness and must not be copied into the personal site:

- `_blog_work/`
- `scripts/blog_pipeline/`
- `codex/skills/`
- `_drafts/`
- remote-run logs
- evidence screenshots
- source notebooks or helper scripts used only to generate figures

## Exportable Files

After all checks pass and the user approves publication, prepare an export
manifest containing only:

- approved reader-facing `_posts/2026-...-flow-matching-guide-part-N.md` files;
- final local assets under `assets/img/blog/flow-matching-guide/`;
- bibliography entries, data files, or config changes only when a published post
  actually requires them.

## Export Gate

Before touching `/Users/quan238/personal/cv`, stop and ask for approval with:

- the exact source-to-target file list;
- the verification commands that passed in the harness;
- any files that will overwrite existing website files;
- confirmation that no harness internals will be copied.
