# SPDX-FileCopyrightText: 2024 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

import os
import random
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer


def compute_expected_sum(x_val, y_val, cin_val, N):
    """Calculate the expected sum of two N-bit values with carry-in."""
    return (x_val + y_val + cin_val) & ((1 << N) - 1)


def compute_expected_cout(x_val, y_val, cin_val, N):
    """
    Calculate the expected carry-out of two N-bit values with carry-in.
    """
    return (x_val + y_val + cin_val) >> N


@cocotb.test()
async def targeted_test(dut):
    """
    Test the ripple-carry adder with specific input values and carry-in.
    """

    N = dut.N.value  # Get the width of the data

    # List of test cases with specific input values and carry-in
    test_cases = [
        (0x0, 0x0, 0),  # Trivial case
        (0x1, 0x1, 0),  # Simple addition without carry-in
        (0x1, 0x1, 1),  # Simple addition with carry-in
        (0xFF, 0x1, 0),  # Overflow case
        (0x00, 0xFF, 1),  # Overflow from carry-in
        (0x12, 0x9A, 1),  # Addition with carry-in
        (0xFF, 0xFF, 1),  # Max values with carry-in
    ]

    for x_val, y_val, cin_val in test_cases:
        # Apply inputs to the DUT
        dut.x.value = x_val
        dut.y.value = y_val
        dut.cin.value = cin_val

        # Wait for a simulation timestep
        await Timer(1, units="ns")

        # Calculate expected output
        expected_sum = compute_expected_sum(x_val, y_val, cin_val, N)
        expected_cout = compute_expected_cout(x_val, y_val, cin_val, N)

        # Check if DUT's output matches the expected output
        assert dut.s.value == expected_sum, (
            f"Test failed for x={x_val}, y={y_val}, cin={cin_val}: "
            f"Expected s={expected_sum}, Got s={dut.s.value}"
        )
        assert dut.cout.value == expected_cout, (
            f"Test failed for x={x_val}, y={y_val}, cin={cin_val}: "
            f"Expected cout={expected_cout}, Got cout={dut.cout.value}"
        )

        # Log the result if the test passes
        dut._log.info(
            f"Test passed for x={x_val}, y={y_val}, cin={cin_val}: "
            f"s={dut.s.value}, cout={dut.cout.value}"
        )


@cocotb.test()
async def random_test(dut):
    """Test the ripple-carry adder with random input combinations."""

    num_tests = 100  # Number of random tests to run

    N = dut.N.value

    for _ in range(num_tests):
        x_val = random.randint(0, (1 << N) - 1)  # Random N-bit value
        y_val = random.randint(0, (1 << N) - 1)  # Random N-bit value
        cin_val = random.randint(0, 1)  # Random carry-in

        # Apply inputs to the DUT
        dut.x.value = x_val
        dut.y.value = y_val
        dut.cin.value = cin_val

        # Wait for a simulation timestep
        await Timer(1, units="ns")

        # Calculate expected output
        expected_sum = compute_expected_sum(x_val, y_val, cin_val, N)
        expected_cout = compute_expected_cout(x_val, y_val, cin_val, N)

        # Check if DUT's output matches the expected output
        assert dut.s.value == expected_sum, (
            f"Random test failed for x={x_val}, y={y_val}, cin={cin_val}: "
            f"Expected s={expected_sum}, Got s={dut.s.value}"
        )
        assert dut.cout.value == expected_cout, (
            f"Random test failed for x={x_val}, y={y_val}, cin={cin_val}: "
            f"Expected cout={expected_cout}, Got cout={dut.cout.value}"
        )

        # Log the result if the test passes
        dut._log.info(
            f"Random test passed for x={x_val}, y={y_val}, cin={cin_val}: "
            f"s={dut.s.value}, cout={dut.cout.value}"
        )


def test_ripple_carry_adder_runner():
    """Run the test using the Cocotb test runner."""

    # Get simulator from the environment
    sim = os.getenv("SIM", "icarus")

    # Get the path to the sources
    proj_path = Path(__file__).resolve().parent.parent.parent.parent
    sources = [
        proj_path / "hw" / "int" / "add" / "ripple_carry_adder.sv",
        proj_path / "hw" / "int" / "add" / "full_adder.sv",
    ]

    # Set the parameters of the design
    parameters = {
        "N": 8,
    }

    # Instantiate the test runner based on the simulator
    runner = get_runner(sim)
    # Build the HDL using the design sources and the top-level module
    runner.build(
        sources=sources,
        parameters=parameters,
        hdl_toplevel="ripple_carry_adder",
        always=True,
        build_dir=proj_path / "build" / "test" / sim,
        timescale=("1ns", "1ps"),
    )
    # Run the test using the python test module
    runner.test(
        hdl_toplevel="ripple_carry_adder", test_module="test_ripple_carry_adder"
    )


if __name__ == "__main__":
    test_ripple_carry_adder_runner()
