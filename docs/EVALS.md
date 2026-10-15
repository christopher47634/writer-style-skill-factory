# Evaluation layers

| Layer | Script | Cost | Runs in CI |
|---|---|---|---|
| Structure | `scripts/quick_validate.py`, `validate.py` | free | yes |
| Eval schema | `scripts/validate_evals.py` | free | yes |
| Registry | `scripts/check_registry.py` | free | yes |
| Trigger routing / overlap | `scripts/check_triggers.py` | free | yes |
| Security scan | `scripts/security_scan.py` | free | yes |
| Prose lint (warn-only) | `scripts/check_prose.py` | free | no (run on drafts) |
| Script tests | `pytest` | free | yes |
| Behaviour (with vs. without skill) | `scripts/run_behavior_eval.py` | model tokens | **no, on demand** |

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
- `name` carries the id from the legacy `test-prompts.json`, which is kept for
  `validate.py`; `validate_evals.py` fails if a legacy prompt is not present in `evals.json`.

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
python scripts/run_behavior_eval.py --skill style-kafka --dry-run   # list cases only
python scripts/run_behavior_eval.py --skill style-kafka --limit 2   # needs the claude CLI
python scripts/run_behavior_eval.py --all --no-judge                # deterministic checks only
python scripts/check_prose.py evals-workspace/latest                # lint the saved replies
```

Each case runs twice (SKILL.md appended as system prompt vs. plain model). Replies
are saved under `evals-workspace/latest/<skill>/`, and `benchmark.json` plus
`summary.md` report check and expectation pass rates with/without the skill.
`--runner` / `--judge-runner` accept any command that reads the prompt on stdin
and prints the reply. Outputs are git-ignored. Real runs cost tokens and are
non-deterministic; treat a single run as a signal, not a gate.
