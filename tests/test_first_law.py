# thermodynamics-sdk/tests/test_first_law.py

import pytest
from thermodynamics_sdk.core import ThermodynamicSystem, FirstLawCalculator


def test_calculate_delta_u_correctness():
    """Test delta_u calculation (ΔU = Q - W)."""
    # Test cases: (Q, W, expected_delta_u)
    test_cases = [
        (100.0, 50.0, 50.0),  # Q > W
        (50.0, 100.0, -50.0),  # W > Q
        (100.0, 100.0, 0.0),  # Q = W
        (0.0, 0.0, 0.0),  # All zero
        (200.0, 0.0, 200.0),  # No work done
        (0.0, 75.0, -75.0),  # No heat added
        (-50.0, -20.0, -30.0),  # Negative Q, negative W
        (-10.0, 20.0, -30.0),  # Negative Q, positive W
        (30.0, -10.0, 40.0),  # Positive Q, negative W
    ]

    for q, w, expected_delta_u in test_cases:
        system = ThermodynamicSystem(heat_added=q, work_done=w)
        actual_delta_u = FirstLawCalculator.calculate_delta_u(system)
        assert actual_delta_u == pytest.approx(expected_delta_u), \
            f"For Q={q}, W={w}: Expected ΔU={expected_delta_u}, Got {actual_delta_u}"


def test_calculate_delta_u_type_validation():
    """Test type validation for calculate_delta_u input."""
    with pytest.raises(
            TypeError,
            match="Input must be an instance of ThermodynamicSystem"):
        FirstLawCalculator.calculate_delta_u("not a system")

    # Test system with invalid internal attributes (should be caught by ThermodynamicSystem's own validation)
    # This specific test case might not directly trigger FirstLawCalculator validation but ThermodynamicSystem's
    # constructor/setter already handles it.


def test_calculate_heat_added_correctness():
    """Test heat added calculation (Q = ΔU + W)."""
    # Test cases: (delta_u, work_done, expected_heat_added)
    test_cases = [
        (50.0, 50.0, 100.0),
        (-50.0, 100.0, 50.0),
        (0.0, 0.0, 0.0),
        (200.0, 0.0, 200.0),
        (-75.0, 75.0, 0.0),
        (-30.0, -20.0, -50.0),
        (-30.0, 20.0, -10.0),
        (40.0, -10.0, 30.0),
    ]

    for delta_u, work_done, expected_heat_added in test_cases:
        actual_heat_added = FirstLawCalculator.calculate_heat_added(
            delta_u, work_done)
        assert actual_heat_added == pytest.approx(expected_heat_added), \
            f"For ΔU={delta_u}, W={work_done}: Expected Q={expected_heat_added}, Got {actual_heat_added}"


def test_calculate_heat_added_type_validation():
    """Test type validation for calculate_heat_added inputs."""
    with pytest.raises(TypeError, match="delta_u must be a float"):
        FirstLawCalculator.calculate_heat_added("invalid", 10.0)
    with pytest.raises(TypeError, match="work_done must be a float"):
        FirstLawCalculator.calculate_heat_added(10.0, [20.0])


def test_calculate_work_done_correctness():
    """Test work done calculation (W = Q - ΔU)."""
    # Test cases: (delta_u, heat_added, expected_work_done)
    test_cases = [
        (50.0, 100.0, 50.0),
        (100.0, 50.0, -50.0),
        (0.0, 0.0, 0.0),
        (0.0, 200.0, 200.0),
        (75.0, 0.0, -75.0),
        (-30.0, -50.0, -20.0),
        (-20.0, -10.0, 10.0),
        (-10.0, 30.0, 40.0),
    ]

    for delta_u, heat_added, expected_work_done in test_cases:
        actual_work_done = FirstLawCalculator.calculate_work_done(
            delta_u, heat_added)
        assert actual_work_done == pytest.approx(expected_work_done), \
            f"For ΔU={delta_u}, Q={heat_added}: Expected W={expected_work_done}, Got {actual_work_done}"


def test_calculate_work_done_type_validation():
    """Test type validation for calculate_work_done inputs."""
    with pytest.raises(TypeError, match="delta_u must be a float"):
        FirstLawCalculator.calculate_work_done("invalid", 10.0)
    with pytest.raises(TypeError, match="heat_added must be a float"):
        FirstLawCalculator.calculate_work_done(10.0, {"Q": 20.0})


def test_inverse_calculations_round_trip():
    """
    Test that inverse calculations yield consistent results.
    1. Calculate Q from ΔU and W.
    2. Then, calculate ΔU back from that Q and the original W.
    3. And calculate W back from that Q and the original ΔU.
    """
    delta_u_orig = 75.0
    work_done_orig = 25.0

    # 1. Calculate Q
    heat_added_calc_q = FirstLawCalculator.calculate_heat_added(
        delta_u_orig, work_done_orig)
    assert heat_added_calc_q == pytest.approx(100.0)

    # 2. Calculate ΔU back from calculated Q and original W
    system_for_delta_u = ThermodynamicSystem(heat_added=heat_added_calc_q,
                                             work_done=work_done_orig)
    delta_u_recalc_from_q = FirstLawCalculator.calculate_delta_u(
        system_for_delta_u)
    assert delta_u_recalc_from_q == pytest.approx(delta_u_orig)

    # 3. Calculate W back from calculated Q and original ΔU
    work_done_recalc_from_q = FirstLawCalculator.calculate_work_done(
        delta_u_orig, heat_added_calc_q)
    assert work_done_recalc_from_q == pytest.approx(work_done_orig)

    # Repeat with different values, including negatives
    delta_u_orig_neg = -30.0
    work_done_orig_neg = 20.0

    heat_added_calc_q_neg = FirstLawCalculator.calculate_heat_added(
        delta_u_orig_neg, work_done_orig_neg)
    assert heat_added_calc_q_neg == pytest.approx(-10.0)

    system_for_delta_u_neg = ThermodynamicSystem(
        heat_added=heat_added_calc_q_neg, work_done=work_done_orig_neg)
    delta_u_recalc_from_q_neg = FirstLawCalculator.calculate_delta_u(
        system_for_delta_u_neg)
    assert delta_u_recalc_from_q_neg == pytest.approx(delta_u_orig_neg)

    work_done_recalc_from_q_neg = FirstLawCalculator.calculate_work_done(
        delta_u_orig_neg, heat_added_calc_q_neg)
    assert work_done_recalc_from_q_neg == pytest.approx(work_done_orig_neg)
