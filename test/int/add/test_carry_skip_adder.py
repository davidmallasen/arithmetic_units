# SPDX-FileCopyrightText: 2024 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

import random

import cocotb
import pytest
from cocotb.triggers import Timer

from test.test_utils.sim import run_sim


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
    Test the carry-skip adder with specific input values and carry-in.
    """

    N = int(dut.N.value)  # Get the width of the data

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
    """Test the carry-skip adder with random input combinations."""

    num_tests = 100  # Number of random tests to run

    N = int(dut.N.value)

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


@pytest.mark.parametrize(
    "N,M",
    [
        (8, 2),
        (8, 4),
        (16, 4),
        (16, 8),
        (32, 4),
        (32, 8),
    ],
)
def test_carry_skip_adder_runner(N, M):
    """Run the test using the FuseSoC cocotb flow."""

    core = "davidmallasen:arithmetic_units:carry_skip_adder:1.0.0"
    num_tests, num_failed = run_sim(core, parameters={"N": N, "M": M})

    assert num_failed == 0, f"Failed {num_failed} of {num_tests} tests."


if __name__ == "__main__":
    test_carry_skip_adder_runner(32, 4)
