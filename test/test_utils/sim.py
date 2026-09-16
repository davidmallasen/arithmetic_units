# SPDX-FileCopyrightText: 2026 EPFL
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units
#
# Author: David Mallasén
# Description: Helper to run cocotb simulations of the repository cores
#   through FuseSoC's Flow API and check their results.

import os
import subprocess
import sys
from pathlib import Path

from cocotb_tools.check_results import get_results

# Repository root directory
REPO_ROOT = Path(__file__).resolve().parents[2]


def run_sim(core: str, parameters: dict[str, int] | None = None) -> tuple[int, int]:
    """
    Run the cocotb simulation of a core through FuseSoC.

    The core must define a 'sim' target based on the Edalize flow API, with
    the cocotb test module set in its 'cocotb_module' flow option.

    Args:
        core (str): VLNV name of the core to simulate.
        parameters (dict): Optional overrides for the design parameters
            declared in the core. Keys are parameter names and values are
            the values to pass to the simulator.
    Returns:
        A tuple with the number of tests run and the number of failed tests.
    """
    # The cocotb test module is imported by the simulator's embedded Python
    # interpreter, so the repository root must be in its module search path
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")

    # Work root is per-unit to allow incremental builds and parallel runs
    unit = core.split(":")[2]
    work_root = REPO_ROOT / "build" / "test" / unit

    # Backend arguments override the parameter defaults of the core
    backendargs = [f"--{name}={value}" for name, value in (parameters or {}).items()]

    subprocess.run(
        [
            "fusesoc",
            "run",
            f"--work-root={work_root}",
            "--target=sim",
            core,
            *backendargs,
        ],
        cwd=REPO_ROOT,
        env=env,
        check=True,
    )

    return get_results(work_root / "results.xml")


def main() -> None:
    """Run the simulation of a core given as a command-line argument."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <core VLNV>")
        sys.exit(1)

    num_tests, num_failed = run_sim(sys.argv[1])
    if num_failed:
        sys.exit(f"ERROR: Failed {num_failed} of {num_tests} tests.")


if __name__ == "__main__":
    main()
