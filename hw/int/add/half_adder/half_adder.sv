// SPDX-FileCopyrightText: 2025 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Half adder
//
// Description: Combinational circuit that adds two 1-bit numbers.
//
// Area: O(1)
// Delay: O(1)

module half_adder (
  input  logic a,    // First operand
  input  logic b,    // Second operand
  output logic s,    // Sum output
  output logic cout  // Carry-out output
);

  assign s = a ^ b;
  assign cout = a & b;

endmodule
