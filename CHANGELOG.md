# thermodynamics-sdk/CHANGELOG.md

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-02-06

### Added
-   **Core API**:
    -   Introduced `ThermodynamicSystem` class to represent a single, lumped thermodynamic system with `internal_energy`, `heat_added`, and `work_done` fields.
    -   Implemented `FirstLawCalculator` with static methods for core First Law calculations: `calculate_delta_u`, `calculate_heat_added`, and `calculate_work_done`.
-   **Physics Guarantees**: Explicitly defined and enforced sign convention `ΔU = Q - W` (where W = work done BY the system). All energy quantities are treated as scalars in Joules with no implicit unit conversion or process assumptions.
-   **JSON Persistence**: Added `save_system_to_json` and `load_system_from_json` functions for serializing and deserializing `ThermodynamicSystem` instances. JSON schema is guaranteed stable for v1.x.
-   **Test Suite**:
    -   `test_system.py`: Covers `ThermodynamicSystem` instantiation, property access, type validation, `to_dict`, `from_dict`, equality, and representation.
    -   `test_first_law.py`: Verifies correctness of `FirstLawCalculator` methods and inverse calculation consistency.
    -   `test_json_io.py`: Ensures JSON save/load round-trip integrity and handles error cases.
-   **Documentation**:
    -   Comprehensive `README.md` including scope, non-goals, quick start, physics conventions, API overview, and stability guarantees.
    -   Detailed docstrings for all classes, methods, and functions.
-   **Examples**: `basic_usage.py` demonstrating fundamental SDK operations.
-   **Project Metadata**: `pyproject.toml` configured for packaging.
-   **Versioning**: Established Semantic Versioning contract.

### Changed
-   (Formerly `thermodynamics_sdk.py` is now split into `thermodynamics_sdk/__init__.py` and `thermodynamics_sdk/core.py` for better structure.)

### Removed
-   (No components removed, this is the initial release.)

### Fixed
-   (No bugs fixed, this is the initial release.)
