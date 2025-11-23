// SPDX-FileCopyrightText: 2024 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Full adder
//
// Description: Combinational circuit that takes two 1-bit numbers, x
// and y, and a carry-in bit, cin, and outputs a sum bit, s, and a carry
// bit, cout.
//
// Area: O(1)
// Delay: O(1)

module full_adder (
  input  logic x,    // First operand
  input  logic y,    // Second operand
  input  logic cin,  // Carry-in bit
  output logic s,    // Output sum
  output logic cout  // Carry-out bit
);

  logic p; // Propagate
  logic g; // Generate
  logic p_cin_carry; 

  half_adder ha1 (
    .a    (x),
    .b    (y),
    .s    (p),
    .cout (g)
  );

  half_adder ha2 (
    .a    (p),
    .b    (cin),
    .s    (s),
    .cout (p_cin_carry)
  );

  assign cout = g | p_cin_carry;

endmodule
