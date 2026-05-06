# Changelog

## 0.9.10 (2026-05-06)

### Changed

- Added compatibility with ecoinvent 3.11 and 3.12 biosphere flow names.
- Automatically detects non-default Brightway biosphere database names such as
  `biosphere-3.11` and `biosphere-3.12`.
- Routes LCIA imports through the selected project biosphere database instead
  of assuming Brightway's default `biosphere3`.
- Adds ecoinvent 3.11+ halon/bromomethane flow-name mappings.
- Drops only unlinked lower-stratosphere/upper-troposphere characterization
  rows when the target biosphere has no corresponding flows.

### Tests

- Added regression tests for flow-name mapping and selective unlinked-flow
  filtering.
- Isolated the Brightway integration test in a temporary project so repeated
  test runs do not depend on persistent local Brightway project state.

## 0.1 (2021-10-04)

Initial release
