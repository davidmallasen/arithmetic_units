// SPDX-FileCopyrightText: 2024 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Ripple-carry adder
//
// Description: Combinational circuit that takes two N-bit numbers, x
// and y, and a carry-in bit, cin, and outputs an N-bit sum, s, and a
// carry-out bit, cout. Internally, it uses N full adders to perform the
// addition.
//
// Area: O(N)
// Delay: O(N)

module ripple_carry_adder #(
  parameter N = 32
) (
  input  logic [N-1:0] x,  // First operand
  input  logic [N-1:0] y,  // Second operand
  input  logic cin,        // Carry-in bit
  output logic [N-1:0] s,  // Output sum
  output logic cout        // Carry-out bit
);

  logic [N-1:0] sum;  // Intermediate sum
  logic [N-1:0] carry;  // Intermediate carry

  // Generate the chain of full adders
  generate
    genvar i;
    for (i = 0; i < N; i++) begin : gen_full_adders
      full_adder full_adder_i (
        .x(x[i]),
        .y(y[i]),
        // Carry-in is the previous carry-out. For the first full adder,
        // the carry-in is the module's input carry.
        .cin(i == 0 ? cin : carry[i-1]),
        .s(sum[i]),
        .cout(carry[i])
      );
    end
  endgenerate

  // Assign the outputs
  assign s = sum;
  assign cout = carry[N-1];

endmodule
