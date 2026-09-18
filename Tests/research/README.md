# Research tests

Run the deterministic synthetic tests with:

```bash
python -m unittest discover -s Tests/research -p 'test_*.py'
```

Synthetic fixtures validate mechanics only; they are not XAUUSD observations.
