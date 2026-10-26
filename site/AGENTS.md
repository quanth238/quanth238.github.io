# PRISM portfolio

This directory is the active website, migrated from al-folio to the PRISM
Next.js template at the owner's request. The Jekyll/Docker instructions in
the repository root apply only to the retained legacy source.

- Use Node.js 22 or later and `npm ci`.
- Content lives in `content/`; the CV is `public/files/quan-tran-hong-cv.pdf`.
- Keep only About and Publications in navigation. CV is a download button.
- Before committing, run `npx prettier . --write`, `npm run typecheck`, and
  `npm run build`. Verify navigation, the CV download, publications, and themes.
- Static output is `out/` and must contain `.nojekyll` on GitHub Pages.
- Preserve the PRISM MIT license and the footer attribution.
