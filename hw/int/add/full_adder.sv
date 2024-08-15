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

  assign s = x ^ y ^ cin;
  assign cout = (x & y) | (x & cin) | (y & cin);

endmodule
