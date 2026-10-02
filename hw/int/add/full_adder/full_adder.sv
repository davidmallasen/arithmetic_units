// SPDX-FileCopyrightText: 2024 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Full adder

module full_adder (
  input  logic x,    // First operand
  input  logic y,    // Second operand
  input  logic cin,  // Carry-in bit
  output logic s,    // Output sum
  output logic cout  // Carry-out bit
);

  logic p;  // Propagate
  logic g;  // Generate
  logic p_cin_carry;

  // ha1 computes the propagate/generate pair of the operands
  half_adder ha1 (
    .a   (x),
    .b   (y),
    .s   (p),
    .cout(g)
  );

  // ha2 adds the carry-in to the propagate signal
  half_adder ha2 (
    .a   (p),
    .b   (cin),
    .s   (s),
    .cout(p_cin_carry)
  );

  // A carry is produced if the operands generate one (g) or if the
  // carry-in propagates through. The two events are mutually
  // exclusive, so a plain OR is sufficient.
  assign cout = g | p_cin_carry;

endmodule
