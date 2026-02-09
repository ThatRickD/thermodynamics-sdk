# thermodynamics_sdk/__init__.py
"""
A stable, minimal, correct foundation for modeling simple thermodynamic systems
using the First Law of Thermodynamics.
"""

from .core import ThermodynamicSystem, FirstLawCalculator, save_system_to_json, load_system_from_json

__version__ = "1.0.0"
