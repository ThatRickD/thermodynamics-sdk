# thermodynamics_sdk/examples/basic_usage.py

import sys
import os

# Ensure the package directory is in the search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from thermodynamics_sdk.core import ThermodynamicSystem, FirstLawCalculator, save_system_to_json, load_system_from_json


def run_basic_example():
    """
    Demonstrates basic usage of the Thermodynamics SDK.
    """
    print("--- Thermodynamics SDK: Basic Usage Example ---")
    print("\nPhysics Convention: ΔU = Q - W (W = work done BY the system)")
    print("All energy quantities are in Joules (J).\n")

    # 1. Create a ThermodynamicSystem
    print("1. Creating a ThermodynamicSystem:")
    system1 = ThermodynamicSystem(internal_energy=100.0,
                                  heat_added=0.0,
                                  work_done=0.0)
    print(f"  Initial System 1: {system1}")

    # 2. Apply some changes (e.g., add heat, do work)
    print("\n2. Applying changes to System 1:")
    system1.heat_added = 200.0  # 200 J heat added TO the system
    system1.work_done = 70.0  # 70 J work done BY the system
    print(
        f"  System 1 after changes: heat_added={system1.heat_added} J, work_done={system1.work_done} J"
    )

    # 3. Calculate change in internal energy (ΔU) using FirstLawCalculator
    print("\n3. Calculating Change in Internal Energy (ΔU):")
    delta_u_system1 = FirstLawCalculator.calculate_delta_u(system1)
    print(
        f"  ΔU = Q - W = {system1.heat_added} - {system1.work_done} = {delta_u_system1} J"
    )
    print(
        f"  If System 1 started at {system1.internal_energy} J, new U would be {system1.internal_energy + delta_u_system1} J"
    )

    # 4. Demonstrate inverse calculations
    print("\n4. Demonstrating Inverse Calculations (First Law):")

    # Scenario A: Know ΔU and W, find Q
    delta_u_a = 50.0  # J
    work_done_a = 20.0  # J (done by system)
    heat_added_a = FirstLawCalculator.calculate_heat_added(
        delta_u_a, work_done_a)
    print(
        f"  Given ΔU={delta_u_a} J and W={work_done_a} J, Q = ΔU + W = {delta_u_a} + {work_done_a} = {heat_added_a} J"
    )

    # Scenario B: Know ΔU and Q, find W
    delta_u_b = -30.0  # J
    heat_added_b = 70.0  # J
    work_done_b = FirstLawCalculator.calculate_work_done(
        delta_u_b, heat_added_b)
    print(
        f"  Given ΔU={delta_u_b} J and Q={heat_added_b} J, W = Q - ΔU = {heat_added_b} - ({delta_u_b}) = {work_done_b} J"
    )

    # 5. JSON Persistence: Save and Load System State
    print("\n5. Demonstrating JSON Persistence:")
    json_filename = "system_state.json"
    system_to_save = ThermodynamicSystem(internal_energy=150.0,
                                         heat_added=100.0,
                                         work_done=60.0)
    print(f"  System to save: {system_to_save}")

    try:
        save_system_to_json(system_to_save, json_filename)
        print(f"  System saved to '{json_filename}'")

        loaded_system = load_system_from_json(json_filename)
        print(f"  System loaded from '{json_filename}': {loaded_system}")

        if system_to_save == loaded_system:
            print("  Successfully saved and loaded system (data matches).")
        else:
            print("  Warning: Saved and loaded system data mismatch!")

    except Exception as e:
        print(f"  An error occurred during JSON operations: {e}")
    finally:
        if os.path.exists(json_filename):
            os.remove(json_filename)
            print(f"  Cleaned up '{json_filename}'.")

    print("\n--- Example Complete ---")


if __name__ == "__main__":
    run_basic_example()
