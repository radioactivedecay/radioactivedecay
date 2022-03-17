# Compiling the radioactivedecay Documentation

The docs for this project are built with
[Sphinx](http://www.sphinx-doc.org/en/master/) and the
ReadTheDocs [theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/).

Use the `Makefile` in this directory to compile static HTML pages by

```bash
make html
```

The compiled docs go into the `build` directory and can be viewed by opening
`html/index.html`. A docs build check is run automatically for every PR.

The docs are hosted on
[GitHub Pages](https://github.com/radioactivedecay/radioactivedecay.github.io).
GitHub Actions automatically push any docs updates to that repo when PRs are
merged into `main`.
