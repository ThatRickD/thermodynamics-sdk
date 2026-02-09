# thermodynamics-sdk/tests/test_json_io.py

import pytest
import os
import tempfile
import json
from thermodynamics_sdk.core import ThermodynamicSystem, save_system_to_json, load_system_from_json


@pytest.fixture
def temp_json_file():
    """Fixture to create a temporary JSON file and ensure its cleanup."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)  # Close the file descriptor, as we'll open it with open()
    yield path
    os.remove(path)


def test_json_save_load_round_trip_basic(temp_json_file):
    """Test saving a basic system and loading it back, ensuring data integrity."""
    original_system = ThermodynamicSystem(internal_energy=100.0,
                                          heat_added=50.0,
                                          work_done=20.0)

    save_system_to_json(original_system, temp_json_file)
    loaded_system = load_system_from_json(temp_json_file)

    assert original_system == loaded_system
    assert original_system.internal_energy == loaded_system.internal_energy
    assert original_system.heat_added == loaded_system.heat_added
    assert original_system.work_done == loaded_system.work_done


def test_json_save_load_round_trip_zero_values(temp_json_file):
    """Test saving/loading a system with zero values."""
    original_system = ThermodynamicSystem(internal_energy=0.0,
                                          heat_added=0.0,
                                          work_done=0.0)

    save_system_to_json(original_system, temp_json_file)
    loaded_system = load_system_from_json(temp_json_file)

    assert original_system == loaded_system


def test_json_save_load_round_trip_negative_values(temp_json_file):
    """Test saving/loading a system with negative values."""
    original_system = ThermodynamicSystem(internal_energy=-50.0,
                                          heat_added=-20.0,
                                          work_done=-10.0)

    save_system_to_json(original_system, temp_json_file)
    loaded_system = load_system_from_json(temp_json_file)

    assert original_system == loaded_system


def test_json_save_load_round_trip_mixed_values(temp_json_file):
    """Test saving/loading a system with a mix of positive, negative, and zero values."""
    original_system = ThermodynamicSystem(internal_energy=75.5,
                                          heat_added=-10.0,
                                          work_done=0.0)

    save_system_to_json(original_system, temp_json_file)
    loaded_system = load_system_from_json(temp_json_file)

    assert original_system == loaded_system


def test_save_system_to_json_invalid_system_type(temp_json_file):
    """Test save_system_to_json raises TypeError for invalid system input."""
    with pytest.raises(
            TypeError,
            match="Input 'system' must be an instance of ThermodynamicSystem."
    ):
        save_system_to_json("not a system", temp_json_file)


def test_save_system_to_json_invalid_filename_type():
    """Test save_system_to_json raises TypeError for invalid filename input."""
    system = ThermodynamicSystem()
    with pytest.raises(TypeError, match="Input 'filename' must be a string."):
        save_system_to_json(system, 123)


def test_load_system_from_json_file_not_found():
    """Test load_system_from_json raises FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError,
                       match="File not found: non_existent_file.json"):
        load_system_from_json("non_existent_file.json")


def test_load_system_from_json_invalid_json_format(temp_json_file):
    """Test load_system_from_json raises JSONDecodeError for malformed JSON."""
    with open(temp_json_file, 'w', encoding='utf-8') as f:
        f.write("{'internal_energy': 100,}")  # Malformed JSON

    with pytest.raises(json.JSONDecodeError):
        load_system_from_json(temp_json_file)


def test_load_system_from_json_missing_keys(temp_json_file):
    """Test load_system_from_json raises ValueError for missing essential keys."""
    # Create a JSON file with missing 'heat_added'
    data = {"internal_energy": 100.0, "work_done": 20.0}
    with open(temp_json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    with pytest.raises(ValueError,
                       match="Missing key 'heat_added' in system data"):
        load_system_from_json(temp_json_file)


def test_load_system_from_json_invalid_data_types(temp_json_file):
    """Test load_system_from_json raises TypeError for incorrect data types in JSON."""
    # Create a JSON file with 'internal_energy' as a string
    data = {"internal_energy": "100.0", "heat_added": 50.0, "work_done": 20.0}
    with open(temp_json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    with pytest.raises(TypeError,
                       match="Value for 'internal_energy' must be a float"):
        load_system_from_json(temp_json_file)


def test_load_system_from_json_invalid_filename_type():
    """Test load_system_from_json raises TypeError for invalid filename input."""
    with pytest.raises(TypeError, match="Input 'filename' must be a string."):
        load_system_from_json(None)
