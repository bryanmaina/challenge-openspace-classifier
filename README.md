## Prerequisites

[Install uv on your system.](https://docs.astral.sh/uv/getting-started/installation/)


## Running the app

```cmd
uv run challenge-openspace-classifier
```

## Development

### Formatting the code

```cmd
uv tool run black .
```

### Test and Test Coverage

Run tests with verbose mode(`-v`) and test coverage

```cmd
uv run pytest -v
```

Run test coverage and report with line numbers

```cmd
uv run pytest --cov=challenge_openspace_classifier --cove-report=term-missing
```





