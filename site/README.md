# Quan Tran Hong — PRISM portfolio

The active source for [quanth238.github.io](https://quanth238.github.io/).
Based on [PRISM](https://github.com/xyjoey/PRISM), under its included MIT license.

Use Node.js 22 or later:

```sh
npm ci
npm run dev
npm run typecheck
npm run build
```

The static build is generated in `out/`. Run `npm run deploy` to build and
publish to the existing `gh-pages` branch using your configured Git access.
The old al-folio workflow is disabled so it cannot overwrite this site.

An optional automatic deployment workflow is provided in
`deployment/github-pages.yml`. Installing it as `.github/workflows/deploy.yml`
requires GitHub access with the `workflow` scope. Re-enable the workflow after
installing that file.

## Content

- `content/config.toml`: identity, contact links, and navigation.
- `content/bio.md` and `content/background.md`: biography and experience.
- `content/publications.bib`: the three selected conference publications.
- `public/files/quan-tran-hong-cv.pdf`: the supplied CV, downloaded from the header button.
- `public/papers/`: overview figures from the corresponding public paper repositories.

Publication status and biographical details follow the CV supplied on
October 26, 2026. The CV download retains the complete document, including
additional papers, service, and experience.

Teaching, Awards, Services, and a separate CV page are not generated.
The earlier al-folio source remains outside `site/` for reference and is not
part of the deployed static export.
