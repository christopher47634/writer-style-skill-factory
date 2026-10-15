# Contributing to Writer Style Skill Factory

Thanks for contributing! This project distills literary craft into reusable AI
skills. The repository is a set of skill definitions plus a dependency-free
validator.

## Requirements

- Python 3 (`validate.py` uses only the standard library, no third-party deps)
- git

## Layout

```
style-analysis-framework/   # analysis framework: SKILL.md, evals/evals.json
writer-style-guide/         # writer style guide skill
style-<author>/             # 16 per-author style skills (e.g. style-kafka, style-luxun)
shared/protocol.md          # protocol shared by every author skill
rubrics/                    # per-skill judge rubrics (1-5 anchors)
validate.py                 # static validator (pure Python 3, no deps)
evaluate.py                 # behaviour eval (calls models, on demand)
assets/                     # images (banner, logo, concept, architecture)
.github/                    # PR and issue templates
```

## Setup

```sh
git clone https://github.com/christopher47634/writer-style-skill-factory.git
cd writer-style-skill-factory
```

There are no dependencies to install.

## Running validation

```sh
python3 validate.py
```

`validate.py --static --strict` runs every free layer in one go (structure,
frontmatter parsed as YAML with CRLF support, contract consistency, sources,
rubrics, registry, trigger routing, security scan) and exits `0` when clean,
`1` on warnings under `--strict`, `2` on errors. Add `--json` for a
machine-readable report. CI runs it with `--strict`, so warnings block merging.

## Free-tier checks (also run in CI)

```sh
python validate.py
python scripts/quick_validate.py      # frontmatter / name / description
python scripts/validate_evals.py      # <skill>/evals/evals.json schema
python scripts/check_registry.py      # registry.json vs directories (--write to regenerate)
python scripts/check_triggers.py      # description overlap + routing queries
python scripts/security_scan.py       # secrets / dangerous commands
python -m pytest -q                   # tests for the scripts above
```

A new author skill also needs `evals/evals.json` (see `docs/EVALS.md`), a few
queries in `evals/routing.json`, and an entry in `registry.json`
(`python scripts/check_registry.py --write`). The behaviour layer is on demand only.

## Adding a new author skill

1. Create the skill directory using a kebab-case slug:

   ```sh
   mkdir style-<author>        # e.g. style-hemingway
   ```

2. Write `style-<author>/SKILL.md` containing the required sections listed above.
   Model it on an existing skill (e.g. `style-kafka/` or `style-luxun/`) so
   formatting stays consistent.

3. Create `style-<author>/evals/evals.json` (schema in `docs/EVALS.md`: `tier`,
   `output_contract`, `rubric_ref`, `pass_threshold`) and `rubrics/<author>.json`.

4. Validate:

   ```sh
   python3 validate.py --static --strict
   ```

   Ensure the exit code is `0`.

5. Keep the change scoped to the new skill directory unless a shared file
   (`style-analysis-framework/`, `writer-style-guide/`) genuinely needs updating.

## Pull request flow

1. Branch: `git checkout -b feat/add-style-<author>`
2. Commit: `git add style-<author> && git commit -m "feat: add <author> style skill"`
3. Push and open a PR using the PR template:
   `git push -u origin feat/add-style-<author>`
4. Fill in the template: summary, changes, and the output of `python3 validate.py --static --strict`.

### Checklist before submitting

- [ ] `python3 validate.py --static --strict` exits `0`
- [ ] Changes are scoped; no edits to READMEs, LICENSE, `assets/`, or unrelated files
- [ ] No secrets or tokens in the diff
- [ ] No generated media or temporary files committed (`frames/`, `tts/`,
      `scenes/`, `*.mp4`, `*.mp3`, `verify_*.png`, ...) — leave them untracked

## License

By contributing you agree your contributions are released under the project's
[MIT License](LICENSE).
