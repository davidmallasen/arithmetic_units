<!--
SPDX-FileCopyrightText: 2026 EPFL
SPDX-License-Identifier: CC-BY-SA-4.0
Author: David Mallasén
-->

# Barrel Shifter

Combinational circuit that takes an N-bit input, `x`, and a
$\log_2(N)$-bit shift distance, `d`, and outputs an N-bit result, `z`,
where `z = x << d`. It is the canonical example of a logarithmic
structure: a constant number of stages that grows with the *logarithm*
of the problem size.

**Source**: [`hw/common/barrel_shifter/barrel_shifter.sv`](../../../hw/common/barrel_shifter.sv)

**Verified by**: [`test/common/test_barrel_shifter.py`](../../../test/common/test_barrel_shifter.py)

## Architecture

A chain of $\lceil \log_2 N \rceil$ stages, one per bit of `d`. Stage
$i$ conditionally shifts its input left by $2^i$.

![Barrel shifter architecture](barrel_shifter.drawio.svg)

## Complexity

- **Area: $O(N \log N)$**
    - $\lceil \log_2 N \rceil$ stages, each an N-bit 2:1 mux ($O(N)$
        area per stage).
- **Delay: $O(\log N)$**
    - One 2:1 mux delay per stage, with $\lceil \log_2 N \rceil$ stages
        in series.

## How it works

### Logarithmic decomposition of the shift distance

Any shift distance $d < 2^{D\_WIDTH}$ decomposes uniquely over powers
of two:

$$
d = \sum_{i=0}^{D\_WIDTH-1} d_i \, 2^i,
$$

and a left shift composes over stages:

$$
x \ll d = x \ll \Big(\sum_i d_i 2^i\Big) = \Big(\big((x \ll d_0 \cdot 1) \ll d_1 \cdot 2\big) \ll \dots\Big),
$$

because shifts by $2^i$ and $2^j$ commute. Each stage $i$ is therefore
a 2:1 multiplexer: if $d_i$ is set, shift by $2^i$; otherwise pass
through. The number of stages is $\lceil \log_2 N \rceil$. Exactly
enough to represent any distance up to $N-1$, which is the largest
meaningful shift for an N-bit value.

### Worked example ($N = 8$)

Take $x = 8'b00000001$ and $d = 3'b101$ ($= 5$). The three stages
shift by 1, 2, and 4:

| Stage | $d_i$ | Shift | Value |
| --- | --- | --- | --- |
| 0 | — | — | `00000001` |
| 1 | 1 | $\ll 1$ | `00000010` |
| 2 | 0 | — | `00000010` |
| 3 | 1 | $\ll 4$ | `00100000` |

Result: $z = 32 = 1 \ll 5$. Each stage contributes at most one
conditional shift, and the composition of the selected shifts equals
the requested distance.

### Shifts that exceed the width

The stage shift is a plain `<<` on the full N-bit vector with **no
masking**: bits shifted past the MSB are discarded and zeros shift in
from the right. Consequently, any $d \ge N$ produces zero. Whether such
distances are reachable depends on $N$: if $N$ is a power of 2, then
$D\_WIDTH = \log_2 N$ and the largest representable distance is $N-1$,
so the output can never be fully shifted out; if $N$ is not a power of
2, then $D\_WIDTH = \lceil \log_2 N \rceil$ admits distances $\ge N$,
which fully zero the output. This is a *logical* left shift; a rotate
would require feeding the shifted-out bits back in, which this
implementation does not do.
