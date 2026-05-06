# AGENTS.md

## Project Overview

`premise_gwp` is a small Python package that installs additional IPCC climate-change LCIA methods into the current Brightway project. It is meant for `premise`-generated LCI databases where hydrogen emissions, BECCS, DAC, or other carbon dioxide removal pathways need characterization factors that are absent or insufficient in the stock IPCC methods.

The public API is:

- `premise_gwp.add_premise_gwp()`: detect the active Brightway biosphere database/version, import the appropriate Excel LCIA method definitions, resolve version-specific flow naming issues, and write/overwrite the Brightway methods.
- `premise_gwp.check_biosphere_database()`: validate that a Brightway biosphere database is available.

## Repository Layout

- `premise_gwp/__init__.py`: package exports and `add_premise_gwp()` implementation.
- `premise_gwp/biosphere.py`: biosphere database discovery, version detection, flow-name mapping loaders, and unlinked-flow filtering helpers.
- `premise_gwp/version.py`: package version tuple.
- `premise_gwp/data/`: bundled LCIA Excel workbooks plus ecoinvent flow-name mapping YAML files.
- `tests/test_implementation.py`: integration-style Brightway test that creates a default `biosphere3`, installs methods, and checks the biogenic CO2 characterization factor.
- `pyproject.toml`: setuptools package metadata and package-data inclusion.
- `conda/`: conda recipe and Python version pin for builds.

## Core Behavior To Preserve

- For biosphere versions earlier than `(0, 8, 8)`, install the IPCC 2013 method workbooks.
- For biosphere versions `(0, 8, 8)` and newer, install the IPCC 2021 method workbooks.
- For ecoinvent 3.10+ biosphere flows, map legacy flow names with `premise_gwp/data/mapping_ei310.yaml` before applying importer strategies.
- For ecoinvent 3.11+ biosphere flows, additionally map halon/bromomethane names with `premise_gwp/data/mapping_ei311.yaml`.
- Keep the special handling for `"Carbon dioxide, in air"` with older biosphere versions and for lower-stratosphere/upper-troposphere unlinked flows in ecoinvent 3.10+.
- `add_premise_gwp()` intentionally writes Brightway methods with `overwrite=True`.

## Development Commands

Install locally:

```bash
pip install -e .
```

Run tests:

```bash
python -m pytest -q
```

Run the focused test file:

```bash
python -m pytest -q tests/test_implementation.py
```

Build distributions:

```bash
python -m build --sdist --wheel --outdir dist/ .
```

## Testing Notes

- Tests require Brightway dependencies (`bw2data`, `bw2io`) and create temporary Brightway projects for integration checks.
- The main test calls `bw2io.create_default_biosphere3()`, so failures can come from Brightway data setup as well as from this package.
- If changing LCIA workbooks or mapping YAML files, verify that all imported methods have no unexpected unlinked flows.
- Keep tests deterministic; avoid depending on whichever Brightway project the developer currently has active.

## Data And Packaging Notes

- The Excel workbooks and YAML mappings in `premise_gwp/data/` are runtime package data. If files are added, renamed, or moved, update both `pyproject.toml` package-data rules if needed and the filename lists inside `add_premise_gwp()`.
- Do not replace structured Excel/YAML data with ad hoc string parsing in package code. Use the existing `ExcelLCIAImporter`/YAML loading flow unless there is a strong compatibility reason.
- Keep `numpy<2.0.0` unless Brightway dependency compatibility has been verified.

## Coding Style

- Follow the existing simple module structure; avoid adding abstractions for this small API unless they remove clear duplication or support a new tested biosphere version.
- Use `pathlib.Path` for package-relative paths.
- Keep package imports lightweight. Brightway imports are currently expected at import time.
- Prefer explicit exceptions for import/linking failures. Existing printed diagnostics are part of the command-line workflow and can be preserved or improved carefully.
- Format Python with Black and isort using the Black profile, matching the GitHub Actions workflow.

## Release Notes

- Package version is currently stored in `premise_gwp/version.py`.
- The conda recipe reads the build version from the `VERSION` environment variable.
- GitHub Actions run formatting, tests on Python 3.10, conda build/publish steps, and PyPI/TestPyPI publishing steps.
