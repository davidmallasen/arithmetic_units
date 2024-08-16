// SPDX-FileCopyrightText: 2024 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Barrel shifter
//
// Description: Combinational circuit that takes an N-bit input, x, and
// a log2(N)-bit shift distance, d, and outputs an N-bit result, z,
// where z = x << d.
//
// Area: O(N log N)
// Delay: O(log N)

module barrel_shifter #(
  parameter int N = 32,  // Width of the data (N > 0)
  // Do not override the following parameter
  parameter int D_WIDTH = $clog2(N)  // Ceiling of log2(N)
) (
  input  logic [      N-1:0] x,  // Input value to shift
  input  logic [D_WIDTH-1:0] d,  // Shift distance
  output logic [      N-1:0] z   // Output value
);

  logic [N-1:0] stage[D_WIDTH+1];  // Intermediate shifted values

  assign stage[0] = x;

  // Generate the chain of shifter stages
  generate
    genvar i;
    for (i = 0; i < D_WIDTH; i++) begin : gen_shifter_stages
      // Shift the value by 2^i if the i-th bit of d is set
      assign stage[i+1] = (d[i] == 1) ? stage[i] << (1 << i) : stage[i];
    end
  endgenerate

  // Assign the output
  assign z = stage[D_WIDTH];

endmodule
