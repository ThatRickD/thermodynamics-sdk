import json
from typing import Dict, Any


class ThermodynamicSystem:
    """
    Represents a single, lumped thermodynamic system.

    All energy quantities are treated as scalars in Joules.
    The sign convention for the First Law of Thermodynamics used throughout this SDK is:
    ΔU = Q - W, where W is work done BY the system.

    Attributes:
        internal_energy (float): The current internal energy of the system (Joules).
        heat_added (float): Heat added TO the system (Joules).
                            Positive for heat added, negative for heat removed.
        work_done (float): Work done BY the system (Joules).
                           Positive for work done by the system, negative for work done on the system.
    """

    def __init__(self,
                 internal_energy: float = 0.0,
                 heat_added: float = 0.0,
                 work_done: float = 0.0):
        """
        Initializes a ThermodynamicSystem instance.

        Args:
            internal_energy (float): Initial internal energy. Defaults to 0.0 J.
            heat_added (float): Initial heat added. Defaults to 0.0 J.
            work_done (float): Initial work done. Defaults to 0.0 J.

        Raises:
            TypeError: If any argument is not a float.
        """
        self._internal_energy = self._validate_float("internal_energy",
                                                     internal_energy)
        self._heat_added = self._validate_float("heat_added", heat_added)
        self._work_done = self._validate_float("work_done", work_done)

    def _validate_float(self, name: str, value: Any) -> float:
        """Helper to validate if a value is a float."""
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"{name} must be a float or an integer, but got {type(value).__name__}."
            )
        return float(value)

    @property
    def internal_energy(self) -> float:
        """Get the internal energy of the system in Joules."""
        return self._internal_energy

    @internal_energy.setter
    def internal_energy(self, value: float) -> None:
        """Set the internal energy of the system in Joules."""
        self._internal_energy = self._validate_float("internal_energy", value)

    @property
    def heat_added(self) -> float:
        """
        Get the heat added to the system in Joules.
        Positive for heat added, negative for heat removed.
        """
        return self._heat_added

    @heat_added.setter
    def heat_added(self, value: float) -> None:
        """
        Set the heat added to the system in Joules.
        Positive for heat added, negative for heat removed.
        """
        self._heat_added = self._validate_float("heat_added", value)

    @property
    def work_done(self) -> float:
        """
        Get the work done by the system in Joules.
        Positive for work done by the system, negative for work done on the system.
        """
        return self._work_done

    @work_done.setter
    def work_done(self, value: float) -> None:
        """
        Set the work done by the system in Joules.
        Positive for work done by the system, negative for work done on the system.
        """
        self._work_done = self._validate_float("work_done", value)

    def to_dict(self) -> Dict[str, float]:
        """Converts the system state to a dictionary for serialization."""
        return {
            "internal_energy": self.internal_energy,
            "heat_added": self.heat_added,
            "work_done": self.work_done,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "ThermodynamicSystem":
        """Creates a ThermodynamicSystem instance from a dictionary."""
        # Ensure all expected keys are present and are floats
        for key in ["internal_energy", "heat_added", "work_done"]:
            if key not in data:
                raise ValueError(
                    f"Missing key '{key}' in system data for deserialization.")
            if not isinstance(data[key], (int, float)):
                raise TypeError(
                    f"Value for '{key}' must be a float, but got {type(data[key]).__name__}."
                )

        return cls(internal_energy=data["internal_energy"],
                   heat_added=data["heat_added"],
                   work_done=data["work_done"])

    def __eq__(self, other: Any) -> bool:
        """Compares two ThermodynamicSystem objects for equality."""
        if not isinstance(other, ThermodynamicSystem):
            return False
        return (self.internal_energy == other.internal_energy
                and self.heat_added == other.heat_added
                and self.work_done == other.work_done)

    def __repr__(self) -> str:
        return (f"ThermodynamicSystem(internal_energy={self.internal_energy}, "
                f"heat_added={self.heat_added}, work_done={self.work_done})")


class FirstLawCalculator:
    """
    Provides static methods for performing First Law of Thermodynamics calculations.

    The sign convention used is: ΔU = Q - W, where W is work done BY the system.
    All quantities are expected to be in Joules.
    """

    @staticmethod
    def _validate_calculation_inputs(delta_u: float = None,
                                     heat_added: float = None,
                                     work_done: float = None):
        """Helper to validate if calculation inputs are floats."""
        for name, value in [("delta_u", delta_u), ("heat_added", heat_added),
                            ("work_done", work_done)]:
            if value is not None and not isinstance(value, (int, float)):
                raise TypeError(
                    f"{name} must be a float or an integer, but got {type(value).__name__}."
                )

    @staticmethod
    def calculate_delta_u(system: ThermodynamicSystem) -> float:
        """
        Calculates the change in internal energy (ΔU) for a given system.

        Formula: ΔU = Q - W
        where Q = heat added to the system, W = work done by the system.

        Args:
            system (ThermodynamicSystem): The system object containing Q and W.

        Returns:
            float: The change in internal energy (ΔU) in Joules.
        """
        if not isinstance(system, ThermodynamicSystem):
            raise TypeError(
                "Input must be an instance of ThermodynamicSystem.")

        # Ensure that the values are floats before calculation
        FirstLawCalculator._validate_calculation_inputs(
            heat_added=system.heat_added, work_done=system.work_done)
        return system.heat_added - system.work_done

    @staticmethod
    def calculate_heat_added(delta_u: float, work_done: float) -> float:
        """
        Calculates the heat added (Q) to a system.

        Formula: Q = ΔU + W
        where ΔU = change in internal energy, W = work done by the system.

        Args:
            delta_u (float): Change in internal energy (ΔU) in Joules.
            work_done (float): Work done by the system (W) in Joules.

        Returns:
            float: The heat added (Q) in Joules.
        """
        FirstLawCalculator._validate_calculation_inputs(delta_u=delta_u,
                                                        work_done=work_done)
        return delta_u + work_done

    @staticmethod
    def calculate_work_done(delta_u: float, heat_added: float) -> float:
        """
        Calculates the work done (W) by a system.

        Formula: W = Q - ΔU
        where Q = heat added to the system, ΔU = change in internal energy.

        Args:
            delta_u (float): Change in internal energy (ΔU) in Joules.
            heat_added (float): Heat added to the system (Q) in Joules.

        Returns:
            float: The work done by the system (W) in Joules.
        """
        FirstLawCalculator._validate_calculation_inputs(delta_u=delta_u,
                                                        heat_added=heat_added)
        return heat_added - delta_u


def save_system_to_json(system: ThermodynamicSystem, filename: str) -> None:
    """
    Serializes a ThermodynamicSystem instance to a JSON file.

    Args:
        system (ThermodynamicSystem): The system instance to save.
        filename (str): The path to the JSON file.

    Raises:
        TypeError: If 'system' is not a ThermodynamicSystem instance.
        IOError: If there's an issue writing the file.
    """
    if not isinstance(system, ThermodynamicSystem):
        raise TypeError(
            "Input 'system' must be an instance of ThermodynamicSystem.")
    if not isinstance(filename, str):
        raise TypeError("Input 'filename' must be a string.")

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(system.to_dict(), f, indent=4)
    except IOError as e:
        raise IOError(f"Failed to save system to {filename}: {e}") from e


def load_system_from_json(filename: str) -> ThermodynamicSystem:
    """
    Deserializes a ThermodynamicSystem instance from a JSON file.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        ThermodynamicSystem: The loaded system instance.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        ValueError: If the JSON data is missing expected keys.
        TypeError: If the JSON data contains incorrect types for system properties.
        IOError: If there's an issue reading the file.
    """
    if not isinstance(filename, str):
        raise TypeError("Input 'filename' must be a string.")

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return ThermodynamicSystem.from_dict(data)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filename}") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON format in {filename}: {e.msg}", e.doc, e.pos) from e
    except (ValueError, TypeError, KeyError
            ) as e:  # KeyError can happen if from_dict doesn't catch it
        raise type(e)(f"Error parsing system data from {filename}: {e}") from e
    except IOError as e:
        raise IOError(f"Failed to load system from {filename}: {e}") from e
