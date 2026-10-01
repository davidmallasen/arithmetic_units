<!--
SPDX-FileCopyrightText: 2026 EPFL
SPDX-License-Identifier: CC-BY-SA-4.0
Author: David Mallasén
-->

# Full Adder

Combinational circuit that takes two 1-bit numbers, `x` and `y`, and a
carry-in bit, `cin`, and outputs a sum bit, `s`, and a carry bit,
`cout`. It is the universal building block of multi-bit adders.

**Source**: [`hw/int/add/full_adder/full_adder.sv`](../../../../hw/int/add/full_adder/full_adder.sv)

**Verified by**: [`test/int/add/test_full_adder.py`](../../../../test/int/add/test_full_adder.py)

## Architecture

A structural decomposition into two [`half_adder`](../half_adder/half_adder.md)
instances and one OR gate. The first half adder computes the
generate/propagate pair of the operands and the second adds the carry-in
to the propagate signal. The OR merges the two ways a carry can be
produced.

![Full adder schematic](full_adder.drawio.svg)

The decomposition into two half adders is a *structural* choice, not
the only possible one: a flat implementation of the same equations
would produce the same function with the same gate count. The
hierarchical form makes the generate/propagate decomposition explicit
and reuses the `half_adder`.

## Complexity

- **Area: $O(1)$**
    - Two half adders (two XOR + two AND) and one OR gate.
- **Delay: $O(1)$**
    - The sum path in this form has two XOR delays, while the carry path
        has one AND delay plus one OR delay.

## How it works

All eight input combinations are shown in the table below:

| `x` | `y` | `cin` | `s` | `cout` |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |
