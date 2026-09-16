# SPDX-FileCopyrightText: 2024 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

import random

import cocotb
import pytest
from cocotb.triggers import Timer

from test.test_utils.sim import run_sim


@cocotb.test()
async def targeted_test(dut):
    """
    Test the barrel shifter for various shift distances and input
    values.
    """

    N = int(dut.N.value)  # Get the width of the data

    # List of test cases with specific input values and shift distances
    test_cases = [
        (0x01, 0),  # Shift 0
        (0x01, 1),  # Shift 1
        (0x01, 2),  # Shift 2
        (0xFF, 4),  # Shift 4 with all bits set
        (0x80, 1),  # Shift MSB out
        (0x01, N - 1),  # Shift one less than max
    ]

    for x_val, d_val in test_cases:
        # Apply inputs to the DUT
        dut.x.value = x_val
        dut.d.value = d_val

        # Wait for a simulation timestep
        await Timer(1, units="ns")

        # Calculate expected output
        expected_z = (x_val << d_val) & ((1 << N) - 1)

        # Check if DUT's output matches the expected output
        assert dut.z.value == expected_z, (
            f"Test failed for x={x_val:0{N}b}, d={d_val}: "
            f"Expected z={expected_z}, Got z={dut.z.value}"
        )

        # Log the result if the test passes
        dut._log.info(
            f"Test passed for x={x_val:0{N}b}, d={d_val}, with z={dut.z.value}"
        )


@cocotb.test()
async def random_test(dut):
    """Test the barrel shifter with random input combinations."""

    num_tests = 100  # Number of random tests to run

    N = int(dut.N.value)
    D_WIDTH = int(dut.D_WIDTH.value)

    for _ in range(num_tests):
        # Generate random input values
        x_val = random.randint(0, (1 << N) - 1)
        d_val = random.randint(0, (1 << D_WIDTH) - 1)

        # Apply inputs to the DUT
        dut.x.value = x_val
        dut.d.value = d_val

        # Wait for a simulation timestep
        await Timer(1, units="ns")

        # Calculate expected output
        expected_z = (x_val << d_val) & ((1 << N) - 1)

        # Check if DUT's output matches the expected output
        assert dut.z.value == expected_z, (
            f"Random test failed for x={x_val:0{N}b}, d={d_val}: "
            f"Expected z={expected_z}, Got z={dut.z.value}"
        )

        # Log the result if the test passes
        dut._log.info(
            f"Random test passed for x={x_val:0{N}b}, d={d_val}, with z={dut.z.value}"
        )


@pytest.mark.parametrize("N", [8, 16, 32])
def test_barrel_shifter_runner(N):
    """Run the test using the FuseSoC cocotb flow."""

    core = "davidmallasen:arithmetic_units:barrel_shifter:1.0.0"
    num_tests, num_failed = run_sim(core, parameters={"N": N})

    assert num_failed == 0, f"Failed {num_failed} of {num_tests} tests."


if __name__ == "__main__":
    test_barrel_shifter_runner(8)
