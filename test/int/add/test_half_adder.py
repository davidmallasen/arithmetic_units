# SPDX-FileCopyrightText: 2025 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

import cocotb
from cocotb.triggers import Timer

from test.test_utils.sim import run_sim


@cocotb.test()
async def exhaustive_test(dut):
    """Test the half adder for all possible input combinations."""

    # Truth table for half adder: (a, b) -> (s, cout)
    truth_table = {
        (0, 0): (0, 0),
        (0, 1): (1, 0),
        (1, 0): (1, 0),
        (1, 1): (0, 1),
    }

    # Iterate over each test case in the truth table
    for (a, b), (expected_sum, expected_cout) in truth_table.items():
        # Apply inputs to the DUT
        dut.a.value = a
        dut.b.value = b

        # Wait for a simulation timestep
        await Timer(1, units="ns")

        # Check if DUT's outputs match expected outputs
        assert (
            dut.s.value == expected_sum
        ), f"Test failed with a={a}, b={b}: Expected sum={expected_sum}, Got sum={dut.s.value}"
        assert (
            dut.cout.value == expected_cout
        ), f"Test failed with a={a}, b={b}: Expected cout={expected_cout}, Got cout={dut.cout.value}"

        # Log the result if the test passes
        dut._log.info(
            f"Test passed for a={a}, b={b} with s={dut.s.value} and cout={dut.cout.value}"
        )


def test_half_adder_runner():
    """Run the test using the FuseSoC cocotb flow."""

    core = "davidmallasen:arithmetic_units:half_adder:1.0.0"
    num_tests, num_failed = run_sim(core)

    assert num_failed == 0, f"Failed {num_failed} of {num_tests} tests."


if __name__ == "__main__":
    test_half_adder_runner()
