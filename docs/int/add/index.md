<!--
SPDX-FileCopyrightText: 2026 EPFL
SPDX-License-Identifier: CC-BY-SA-4.0
Author: David Mallasén
-->

# Addition

Binary addition is the canonical example of how a simple recurrence
becomes a family of architectures with very different delay
characteristics. This page introduces the concepts shared by the adders
implemented in `hw/int/add/`; each unit page then develops its own
architecture on top of them.

## Units

| Unit | Description | Area | Delay |
| --- | --- | --- | --- |
| [`half_adder`](half_adder/half_adder.md) | Adds two 1-bit numbers. $s = a \oplus b$, $c = a \cdot b$. It is the seed of the generate/propagate decomposition. | $O(1)$ | $O(1)$ |
| [`full_adder`](full_adder/full_adder.md) | Adds two 1-bit numbers and a carry-in. Two half adders and an OR. Its structure is the carry recurrence in hardware. | $O(1)$ | $O(1)$ |
| [`carry_ripple_adder`](carry_ripple_adder/carry_ripple_adder.md) | Adds two N-bit numbers with a ripple carry chain. N full adders in series. | $O(N)$ | $O(N)$ |
| [`carry_skip_adder`](carry_skip_adder/carry_skip_adder.md) | Ripple adder with M-bit ripple blocks with propagate-controlled bypass. | $O(N)$ | $O(\sqrt{N})$ |

## The carry recurrence

Adding two bits $x_i$ and $y_i$ together with an incoming carry $c_i$
produces a sum bit $s_i$ and an outgoing carry $c_{i+1}$. The
arithmetic identity is

$$
x_i + y_i + c_i = s_i + 2\,c_{i+1},
$$

from which the standard Boolean equations follow:

$$
s_i = x_i \oplus y_i \oplus c_i, \qquad
c_{i+1} = x_i y_i \lor (x_i \oplus y_i)\, c_i.
$$

The carry-ripple adder implements exactly these equations, N times in
a chain (see [`carry_ripple_adder`](carry_ripple_adder/carry_ripple_adder.md)).

## Generate and propagate

The two terms of the carry equation have a cleaner interpretation.
Define, for each bit position $i$:

- **Generate**: $g_i = x_i \cdot y_i$. The position *generates* a
  carry regardless of the incoming carry ($c_{i+1} = 1$ whenever
  $g_i = 1$).
- **Propagate**: $p_i = x_i \oplus y_i$. The position *propagates* an
  incoming carry to the next position ($c_{i+1} = c_i$ whenever
  $p_i = 1$).

In terms of these signals the carry recurrence becomes

$$
c_{i+1} = g_i \lor (p_i \land c_i), \qquad s_i = p_i \oplus c_i.
$$

This reformulation is the single most important abstraction in adder
design, for two reasons:

1. **It decouples the recurrence from the operands.** The carry chain
    depends on the operands only through $g_i$ and $p_i$, which are
    computed locally in one gate delay and in parallel for all
    positions. Everything that follows is a strategy for resolving the
    recurrence $c_{i+1} = g_i \lor (p_i \land c_i)$ faster than
    serially.
2. **It exposes structure across bit groups.** For a group of bits, the
    group generates a carry if some position generates
    and all more significant positions within the group propagate. The
    group propagates a carry if *all* its positions propagate.
