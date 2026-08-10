# Contributing to Writer Style Skill Factory

Thanks for contributing! This project distills literary craft into reusable AI
skills. The repository is a set of skill definitions plus a dependency-free
validator.

## Requirements

- Python 3 (`validate.py` uses only the standard library, no third-party deps)
- git

## Layout

```
style-analysis-framework/   # analysis framework: SKILL.md, results.tsv, test-prompts.json
writer-style-guide/         # writer style guide skill
style-<author>/             # 16 per-author style skills (e.g. style-kafka, style-luxun)
validate.py                 # validator (pure Python 3, no deps)
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

For every skill directory the validator checks:

- `SKILL.md` and `test-prompts.json` exist;
- `test-prompts.json` is a valid JSON array containing at least one prompt;
- `SKILL.md` contains the required sections (the validator accepts any listed
  variant):
  - 硬输出契约 / 硬輸出契約 / Hard Output Contract
  - 反模式 / Anti-Pattern
  - 语料 / corpus / Corpus

It then runs a Security & Cleanup check.

Current `main` result: `341 passed, 0 failed, 5 warnings`. Warnings are advisory
and do not block merging.

## Adding a new author skill

1. Create the skill directory using a kebab-case slug:

   ```sh
   mkdir style-<author>        # e.g. style-hemingway
   ```

2. Write `style-<author>/SKILL.md` containing the required sections listed above.
   Model it on an existing skill (e.g. `style-kafka/` or `style-luxun/`) so
   formatting stays consistent.

3. Create `style-<author>/test-prompts.json` — a valid JSON array with at least
   one prompt string that exercises the skill.

4. Validate:

   ```sh
   python3 validate.py
   ```

   Ensure `0 failed`.

5. Keep the change scoped to the new skill directory unless a shared file
   (`style-analysis-framework/`, `writer-style-guide/`) genuinely needs updating.

## Pull request flow

1. Branch: `git checkout -b feat/add-style-<author>`
2. Commit: `git add style-<author> && git commit -m "feat: add <author> style skill"`
3. Push and open a PR using the PR template:
   `git push -u origin feat/add-style-<author>`
4. Fill in the template: summary, changes, and the output of `python3 validate.py`.

### Checklist before submitting

- [ ] `python3 validate.py` reports `0 failed`
- [ ] Changes are scoped; no edits to READMEs, LICENSE, `assets/`, or unrelated files
- [ ] No generated media or temporary files committed (`frames/`, `tts/`,
      `scenes/`, `*.mp4`, `*.mp3`, `verify_*.png`, ...) — leave them untracked
- [ ] No secrets or tokens in the diff (the origin remote URL contains a token —
      never paste it)

## License

By contributing you agree your contributions are released under the project's
[MIT License](LICENSE).
