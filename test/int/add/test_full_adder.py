# SPDX-FileCopyrightText: 2024 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

import cocotb
from cocotb.triggers import Timer

from test.test_utils.sim import run_sim


@cocotb.test()
async def exhaustive_test(dut):
    """Test the full adder for all possible input combinations."""

    # Truth table for full adder: (x, y, cin) -> (s, cout)
    truth_table = {
        (0, 0, 0): (0, 0),
        (0, 0, 1): (1, 0),
        (0, 1, 0): (1, 0),
        (0, 1, 1): (0, 1),
        (1, 0, 0): (1, 0),
        (1, 0, 1): (0, 1),
        (1, 1, 0): (0, 1),
        (1, 1, 1): (1, 1),
    }

    # Iterate over each test case in the truth table
    for (x, y, cin), (expected_sum, expected_cout) in truth_table.items():
        # Apply inputs to the DUT
        dut.x.value = x
        dut.y.value = y
        dut.cin.value = cin

        # Wait for a simulation timestep
        await Timer(1, units="ns")

        # Check if DUT's outputs match expected outputs
        assert (
            dut.s.value == expected_sum
        ), f"Test failed with x={x}, y={y}, cin={cin}: Expected sum={expected_sum}, Got sum={dut.s.value}"
        assert (
            dut.cout.value == expected_cout
        ), f"Test failed with x={x}, y={y}, cin={cin}: Expected cout={expected_cout}, Got cout={dut.cout.value}"

        # Log the result if the test passes
        dut._log.info(
            f"Test passed for x={x}, y={y}, cin={cin} with s={dut.s.value} and cout={dut.cout.value}"
        )


def test_full_adder_runner():
    """Run the test using the FuseSoC cocotb flow."""

    core = "davidmallasen:arithmetic_units:full_adder:1.0.0"
    num_tests, num_failed = run_sim(core)

    assert num_failed == 0, f"Failed {num_failed} of {num_tests} tests."


if __name__ == "__main__":
    test_full_adder_runner()
