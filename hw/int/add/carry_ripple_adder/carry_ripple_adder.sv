// SPDX-FileCopyrightText: 2024 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Carry-ripple adder

module carry_ripple_adder #(
  parameter int N = 32
) (
  input  logic [N-1:0] x,    // First operand
  input  logic [N-1:0] y,    // Second operand
  input  logic         cin,  // Carry-in bit
  output logic [N-1:0] s,    // Output sum
  output logic         cout  // Carry-out bit
);

  logic [N-1:0] sum;  // Sum bit of each stage
  logic [N-1:0] carry;  // Carry-out of each stage

  // Generate the chain of full adders. Stage i's carry-in is stage i-1's
  // carry-out; stage 0 takes the module's input carry instead.
  generate
    genvar i;
    for (i = 0; i < N; i++) begin : gen_full_adders
      full_adder full_adder_i (
        .x(x[i]),
        .y(y[i]),
        .cin(i == 0 ? cin : carry[i-1]),
        .s(sum[i]),
        .cout(carry[i])
      );
    end
  endgenerate

  assign s = sum;
  assign cout = carry[N-1];

endmodule
