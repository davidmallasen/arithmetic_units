# SPDX-FileCopyrightText: 2024 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

import os
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer


@cocotb.test()
async def exhaustive_test(dut):
    """Test the full adder for all possible input combinations."""

    # List of all possible input combinations (x, y, cin)
    test_cases = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 1),
    ]

    # Iterate over each test case
    for x, y, cin in test_cases:
        # Apply inputs to the DUT
        dut.x.value = x
        dut.y.value = y
        dut.cin.value = cin

        # Wait for a simulation timestep
        await Timer(1, units="ns")

        # Compute expected outputs
        expected_sum = x ^ y ^ cin
        expected_cout = (x & y) | (cin & (x ^ y))

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
    """Run the test using the Cocotb test runner."""

    # Get simulator from the environment
    sim = os.getenv("SIM", "icarus")

    # Get the path to the sources
    proj_path = Path(__file__).resolve().parent.parent.parent.parent
    sources = [proj_path / "hw" / "int" / "add" / "full_adder.sv"]

    # Set the parameters of the design
    parameters = {}

    # Instantiate the test runner based on the simulator
    runner = get_runner(sim)
    # Build the HDL using the design sources and the top-level module
    runner.build(
        sources=sources,
        parameters=parameters,
        hdl_toplevel="full_adder",
        always=True,
        build_dir=proj_path / "build" / "test" / sim,
        timescale=("1ns", "1ps"),
    )
    # Run the test using the python test module
    runner.test(hdl_toplevel="full_adder", test_module="test_full_adder")


if __name__ == "__main__":
    test_full_adder_runner()
