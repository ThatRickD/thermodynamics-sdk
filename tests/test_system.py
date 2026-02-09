# thermodynamics-sdk/tests/test_system.py

import pytest
from thermodynamics_sdk.core import ThermodynamicSystem


def test_system_initialization_defaults():
    """Test ThermodynamicSystem initializes with default values."""
    system = ThermodynamicSystem()
    assert system.internal_energy == 0.0
    assert system.heat_added == 0.0
    assert system.work_done == 0.0


def test_system_initialization_custom_values():
    """Test ThermodynamicSystem initializes with custom values."""
    system = ThermodynamicSystem(internal_energy=100.0,
                                 heat_added=50.0,
                                 work_done=20.0)
    assert system.internal_energy == 100.0
    assert system.heat_added == 50.0
    assert system.work_done == 20.0


def test_system_initialization_with_integers():
    """Test ThermodynamicSystem initializes correctly with integer values (coerced to float)."""
    system = ThermodynamicSystem(internal_energy=100,
                                 heat_added=50,
                                 work_done=20)
    assert system.internal_energy == 100.0
    assert system.heat_added == 50.0
    assert system.work_done == 20.0
    assert isinstance(system.internal_energy, float)
    assert isinstance(system.heat_added, float)
    assert isinstance(system.work_done, float)


def test_system_type_validation_on_init():
    """Test that __init__ raises TypeError for non-float/int arguments."""
    with pytest.raises(TypeError,
                       match="internal_energy must be a float or an integer"):
        ThermodynamicSystem(internal_energy="invalid")
    with pytest.raises(TypeError,
                       match="heat_added must be a float or an integer"):
        ThermodynamicSystem(heat_added=[1, 2])
    with pytest.raises(TypeError,
                       match="work_done must be a float or an integer"):
        ThermodynamicSystem(work_done={"key": "value"})


def test_property_getters():
    """Test that properties return the correct values."""
    system = ThermodynamicSystem(internal_energy=150.0,
                                 heat_added=75.0,
                                 work_done=30.0)
    assert system.internal_energy == 150.0
    assert system.heat_added == 75.0
    assert system.work_done == 30.0


def test_property_setters():
    """Test that properties can be set and validate types."""
    system = ThermodynamicSystem()
    system.internal_energy = 200.0
    system.heat_added = 100.0
    system.work_done = 40.0

    assert system.internal_energy == 200.0
    assert system.heat_added == 100.0
    assert system.work_done == 40.0

    system.internal_energy = -50.5
    assert system.internal_energy == -50.5

    system.heat_added = 0
    assert system.heat_added == 0.0

    system.work_done = -15
    assert system.work_done == -15.0


def test_property_setters_type_validation():
    """Test that property setters raise TypeError for non-float/int values."""
    system = ThermodynamicSystem()
    with pytest.raises(TypeError,
                       match="internal_energy must be a float or an integer"):
        system.internal_energy = "wrong type"
    with pytest.raises(TypeError,
                       match="heat_added must be a float or an integer"):
        system.heat_added = None
    with pytest.raises(TypeError,
                       match="work_done must be a float or an integer"):
        system.work_done = [10]


def test_to_dict_method():
    """Test the to_dict method for correct dictionary representation."""
    system = ThermodynamicSystem(internal_energy=100.0,
                                 heat_added=50.0,
                                 work_done=20.0)
    expected_dict = {
        "internal_energy": 100.0,
        "heat_added": 50.0,
        "work_done": 20.0,
    }
    assert system.to_dict() == expected_dict


def test_from_dict_method():
    """Test the from_dict class method for correct object creation."""
    data = {
        "internal_energy": 100.0,
        "heat_added": 50.0,
        "work_done": 20.0,
    }
    system = ThermodynamicSystem.from_dict(data)
    assert system.internal_energy == 100.0
    assert system.heat_added == 50.0
    assert system.work_done == 20.0


def test_from_dict_missing_keys():
    """Test from_dict handles missing keys correctly."""
    data_missing_ie = {
        "heat_added": 50.0,
        "work_done": 20.0,
    }
    with pytest.raises(ValueError,
                       match="Missing key 'internal_energy' in system data"):
        ThermodynamicSystem.from_dict(data_missing_ie)

    data_missing_q = {
        "internal_energy": 100.0,
        "work_done": 20.0,
    }
    with pytest.raises(ValueError,
                       match="Missing key 'heat_added' in system data"):
        ThermodynamicSystem.from_dict(data_missing_q)


def test_from_dict_invalid_types():
    """Test from_dict handles invalid types in dictionary values."""
    data_invalid_ie = {
        "internal_energy": "not a float",
        "heat_added": 50.0,
        "work_done": 20.0,
    }
    with pytest.raises(TypeError,
                       match="Value for 'internal_energy' must be a float"):
        ThermodynamicSystem.from_dict(data_invalid_ie)

    data_invalid_q = {
        "internal_energy": 100.0,
        "heat_added": [50.0],
        "work_done": 20.0,
    }
    with pytest.raises(TypeError,
                       match="Value for 'heat_added' must be a float"):
        ThermodynamicSystem.from_dict(data_invalid_q)


def test_system_equality():
    """Test __eq__ method for ThermodynamicSystem."""
    system1 = ThermodynamicSystem(internal_energy=100.0,
                                  heat_added=50.0,
                                  work_done=20.0)
    system2 = ThermodynamicSystem(internal_energy=100.0,
                                  heat_added=50.0,
                                  work_done=20.0)
    system3 = ThermodynamicSystem(internal_energy=101.0,
                                  heat_added=50.0,
                                  work_done=20.0)
    system4 = ThermodynamicSystem(internal_energy=100,
                                  heat_added=50,
                                  work_done=20)  # Test with ints

    assert system1 == system2
    assert system1 != system3
    assert system1 == system4  # Should be equal after float coercion
    assert system1 != "not a system"  # Should return NotImplemented (and thus False for !=) or explicit False
    assert not (system1 == "not a system")  # Ensure it doesn't raise an error


def test_system_repr():
    """Test __repr__ method for ThermodynamicSystem."""
    system = ThermodynamicSystem(internal_energy=100.0,
                                 heat_added=50.0,
                                 work_done=20.0)
    expected_repr = "ThermodynamicSystem(internal_energy=100.0, heat_added=50.0, work_done=20.0)"
    assert repr(system) == expected_repr
