<!--
SPDX-FileCopyrightText: 2026 EPFL
SPDX-License-Identifier: CC-BY-SA-4.0
Author: David Mallasén
-->

# Arithmetic Units

The documentation mirrors the layout of the `hw/` directory, so the
documentation for `hw/int/add/half_adder/` is in [`docs/int/add/half_adder/`](int/add/half_adder/half_adder.md).
Each unit page explains the architecture of one module and derives its
complexity from that architecture.

## Unit Dependencies

Each unit is a [FuseSoC](https://fusesoc.readthedocs.io/) core`. The
core file declares the filesets, the default target's toplevel, and the
`sim` target used by the tests.

Dependencies between cores are declared in the core file with `depend`
entries referencing other cores. FuseSoC resolves them automatically and
pulls in the required sources recursively, so a core only needs to
declare what it directly instantiates.

## Building and testing

Environment setup, simulation, formatting, and linting are documented
in the top-level [README](../README.md).
