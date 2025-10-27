# Challenge: Open Space Classifier

A small utility that reads a CSV of people and randomly assigns them to seats at
tables. It can be run daily with a path to your CSV and will output a summary of
how many people were seated and who couldn't be seated if capacity is exceeded.

## Features

- Reads names from a CSV column named "Names"
- If your CSV is a single column without a header, it will automatically create
  a clean_ file with a header and re-read it
- Randomly distributes people across tables and seats
- Default room capacity: 6 tables × 4 seats = 24 seats

## Prerequisites

- Python 3.12+
- [Install uv on your system.](https://docs.astral.sh/uv/getting-started/installation/)

## CSV format

- Preferred: a header row with a column named Names
- Also supported: a single-column CSV without a header (the program will create
  clean_<filename> with a Names header and use that)

## Running the app

You can pass the CSV path as an argument or run interactively.

- With an argument:

```cmd
uv run challenge-openspace-classifier path\to\your\people.csv
```

- Interactively (you will be prompted for the path):

```cmd
uv run challenge-openspace-classifier
```

Example data file in this repo: data\new_colleagues.csv (single-column list
without header)

## Output

The program prints a summary like:

- Total names: N | Seated: S | Unseated: U
- If any people could not be seated, their names are listed under "Unseated
  people"

## Notes on capacity

- Defaults to 6 tables with 4 seats each (24 total)
- People are shuffled and seated table-by-table until no seats remain
- Any extra names are returned and printed as "Unseated"

## Development

### Formatting the code

```cmd
uv tool run black .
```

### Test and Test Coverage

Run tests with verbose mode (-v) and test coverage:

```cmd
uv run pytest -v
```

Run test coverage and report with line numbers:

```cmd
uv run pytest --cov=challenge_openspace_classifier --cov-report=term-missing
```

## Installation

If you don't already have uv installed, follow the official guide:
https://docs.astral.sh/uv/getting-started/installation/

Once uv is available:

- Create and activate a virtual environment (Windows PowerShell):
  - uv venv
  - .\.venv\Scripts\Activate.ps1
- Install the project and dev tools:
  - uv sync --group dev

This will install the package and create the console command
challenge-openspace-classifier.

## Quick start

- Using example data in this repository:
  - uv run challenge-openspace-classifier data\new_colleagues.csv

You should see a summary and the room layout printed to the console.

## Example output

```
Total names: 26 | Seated: 24 | Unseated: 2
Unseated people (not enough capacity):
- Casey
- Drew

Room layout:
Table 1: [Alice, Bob, Charlie, Dana]
Table 2: [Eli, Fran, Gus, Harper]
Table 3: [Ira, Jules, Kai, Lee]
Table 4: [Mona, Noel, Oak, Pax]
Table 5: [Quinn, Rei, Sky, Tay]
Table 6: [Uma, Val, Wes, Xan]
```

Note: The exact names per table will vary because the people are shuffled
randomly each run.

## Troubleshooting

- File not found: Make sure you provide a valid path and use backslashes on
  Windows, e.g., C:\\path\\to\\people.csv
- Missing header: If your CSV is a single column without a header, the app will
  create a companion file named clean_<filename> with a Names header and use
  that automatically.
- Empty or blank lines: Blank or whitespace-only lines are ignored.
- Capacity: By default there are 6 tables with 4 seats each (24 total). Extra
  people will be listed as Unseated.
