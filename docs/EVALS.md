# Evaluation layers

| Layer | Script | Cost | Runs in CI |
|---|---|---|---|
| Static (all free layers) | `validate.py --static --strict` | free | yes |
| Structure | `scripts/quick_validate.py` | free | yes |
| Eval schema | `scripts/validate_evals.py` | free | yes |
| Registry | `scripts/check_registry.py` | free | yes |
| Trigger routing / overlap | `scripts/check_triggers.py` | free | yes |
| Security scan | `scripts/security_scan.py` | free | yes |
| Prose lint (warn-only) | `scripts/check_prose.py` | free | no (run on drafts) |
| Script tests | `pytest` | free | yes |
| Behaviour + LLM judge | `evaluate.py` | model tokens | dispatch / weekly schedule only |

The workflow is `.github/workflows/skill-evals.yml`. Any script exits non-zero
when it finds no skill directories, so an emptied repo cannot pass.

## evals.json

Each skill has `<skill>/evals/evals.json` in the anthropics/skills
skill-creator format:

```json
{"skill_name": "style-kafka",
 "evals": [{"id": 1, "name": "typical", "prompt": "...", "expected_output": "...",
            "files": [], "expectations": ["judgeable statement", "..."],
            "checks": [{"type": "contains", "value": "## 中文翻译"}]}]}
```

- `expectations[]` are human/LLM-judgeable statements (used by the judge in the behaviour run).
- `checks[]` (extension) are deterministic assertions: `contains`, `not_contains`,
  `regex`, `not_regex`, `starts_with`, `min_chars`, `max_chars`.
- `tier` is `smoke`, `regression` or `adversarial`.
- `output_contract` is checked mechanically before any judge call: `language`,
  `sections`, `length.min_chars/max_chars`, `must_not_contain`,
  `must_contain_regex`, `forbidden_regex`. A failing draft scores 1 on every
  dimension and never reaches the judge.
- `rubric_ref` points to `rubrics/<author>.json`, which extends `rubrics/_base.json`
  with 1-5 anchor descriptions per dimension (style_fidelity, originality,
  factual_safety, contract_compliance, naturalness, anti_pattern_free).
- `pass_threshold` is `{"overall": 3.5, "min_dimension": 2}` unless a case overrides it.
- `judge_golden` (optional) holds a human score used to calibrate a new judge.

`evals/routing.json` holds trigger-routing queries (`{"query", "expect"}`) for
`check_triggers.py`.

## Trigger check limits

`check_triggers.py` scores queries against descriptions with an IDF-weighted
keyword match. It is a cheap regression guard for ambiguous descriptions, not a
simulation of a real model's skill selection. Overlap above 0.20 is reported as
a warning (the Japanese author descriptions share a template, so dazai/soseki
sit near 0.40); above 0.45 it fails. Tune with `--warn-overlap`, `--max-overlap`,
`--min-anchors`, `--min-rank1`.

## Behaviour eval (on demand)

```sh
python evaluate.py --skill style-kafka --tier smoke --dry-run          # plan only, no model calls
python evaluate.py --skill style-luxun --tier smoke --budget-usd 2     # generate + judge
python evaluate.py --all --tier smoke --baseline --no-judge            # with vs. without skill, checks only
python scripts/check_prose.py evals-workspace/latest                   # lint the saved drafts
```

- Backends: `--generator` / `--judge` (or `EVAL_GENERATOR` / `EVAL_JUDGE`) take
  `anthropic:<model>`, `openai:<model>` (any OpenAI-compatible endpoint) or
  `cmd:<command>` (reads the prompt on stdin, e.g. `cmd:claude -p`).
- The judge should be a different model family from the generator. It sees only
  the task, the draft and the rubric, not SKILL.md, and must answer in the
  `JUDGE_SCHEMA` JSON (score + quoted evidence per dimension, violations, verdict).
- Each case runs `--runs` times (default 3); dimension scores are medians.
- `--budget-usd` stops the run early (exit code 3) once the estimated spend is reached.
- Live results are appended to `results.tsv` with `eval_mode=live`; `validate.py`
  rejects any other mode, so hand-estimated scores cannot pass as benchmark data.
- Exit codes: `0` all passed, `1` some case failed, `2` config/call error, `3` budget hit.

The `behaviour-eval` job in `.github/workflows/skill-evals.yml` runs this on
`workflow_dispatch` and every Monday. It needs the `ANTHROPIC_API_KEY` secret
(generator) and `OPENAI_API_KEY` / `OPENAI_BASE_URL` plus the `EVAL_JUDGE`
repository variable (judge); without them the job is skipped.
