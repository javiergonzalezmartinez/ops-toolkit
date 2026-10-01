# Contributing

Thanks for looking. This is a small project and it should stay small.

## Ground rules

- **Every formula must be checkable by hand.** A change to a formula needs a test with a worked example you can verify on paper.
- **No unprovable claims.** Docs and examples must not state benchmarks or savings figures without a source. Example numbers are labelled as illustrative.
- **No dependencies** in the core module unless there is a strong reason.

## Development

```
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Pull requests

1. Open an issue first for anything bigger than a small fix.
2. Keep the PR focused: one change, with tests.
3. Update `README.md` and `CHANGELOG.md` when behaviour changes.

## Reporting problems

Use the issue templates. For a wrong result, include your inputs and the result you expected, with the calculation.
