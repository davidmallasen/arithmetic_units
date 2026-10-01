// SPDX-FileCopyrightText: 2025 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Half adder

module half_adder (
  input  logic a,    // First operand
  input  logic b,    // Second operand
  output logic s,    // Sum output
  output logic cout  // Carry-out output
);

  // Sum: one when exactly one operand is one
  assign s = a ^ b;
  // Carry-out: one when both operands are one
  assign cout = a & b;

endmodule
