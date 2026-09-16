<!--
SPDX-FileCopyrightText: 2026 EPFL
SPDX-License-Identifier: LGPL-3.0-or-later
Source: https://github.com/davidmallasen/arithmetic_units

Author: David Mallasén
-->

# AGENTS.md

Instructions for AI coding agents working in this repository. Keep answers and
changes consistent with the rules below. When a rule here conflicts with the
current state of the code, trust the code, flag the discrepancy, and update
this file.

## Project overview

SystemVerilog arithmetic units as FuseSoC cores, verified with cocotb/pytest (Icarus).
Layout: `hw/<category>/<unit>/<unit>.sv` + `.core`; tests mirror it in `test/<category>/<unit>/test_<unit>.py`.
See `README.md` for full environment setup (conda env `arithmetic_units`, iverilog, verible).

## Commands

| Command | Purpose |
| --- | --- |
| `make test` | Run all tests (`pytest test/<path>.py` for one unit) |
| `make format` | Format SV (verible) + Python (black) |
| `make sv-lint` | Lint SystemVerilog |
| `make clean` | Remove build artifacts and Python caches |
| `reuse lint` | Check license compliance |

Simulations run through FuseSoC's Flow API: each `.core` defines a `sim` target
(`flow: sim`) that sets the simulator (`flow_options.tool`, icarus by default),
the cocotb test module (`cocotb_module`) and the test parameters. Override the
simulator with `--tool=<sim>` as a backend argument.

## Conventions

- **SPDX header first line of every file**
  - `hw/`: `CERN-OHL-W-2.0+`
  - `test/`, `util/`, root: `LGPL-3.0-or-later`
  - Add comment with author and description after the SPDX header.
- **Cores**: VLNV `davidmallasen:arithmetic_units:<unit>:1.0.0`; `.core` starts with `CAPI=2:`,
  `rtl` fileset with `file_type: systemVerilogSource`, `default` target sets `toplevel`.
  Dependencies: `depend: - ~davidmallasen:arithmetic_units:<dep>:1.0.0`.
- **SV style**: one module per file named after it; header comment with description and
  `Area: O(...)` / `Delay: O(...)`; `logic` types, commented ports, named connections;
  `parameter int N = ...` + `generate` blocks.
- **Tests**: copy an existing `test_*.py` — cocotb tests drive the DUT with
  `await Timer(1, units="ns")`; the runner calls
  `test.test_utils.sim.run_sim` with the core VLNV and asserts no test failed.
  Test parameters live in the core's `sim` target (`parameters: [N=8]`) and are
  declared top-level (`datatype: int`, `paramtype: vlogparam`); override them
  per test with `run_sim(core, parameters={"N": N})` (e.g. under
  `pytest.mark.parametrize`). Keep `.core` files consistent with files on disk.

## Adding a unit

1. `hw/<category>/<unit>/<unit>.sv` + `<unit>.core` (add `depend` if needed).
2. `test/<category>/test_<unit>.py` modeled on an existing test; `__init__.py` for new dirs.
3. Validate: `make test && make format && make sv-lint && reuse lint`.
