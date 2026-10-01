// SPDX-FileCopyrightText: 2024 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Barrel shifter

module barrel_shifter #(
  parameter int N = 32,  // Width of the data (N > 0)
  // Do not override the following parameter
  parameter int D_WIDTH = $clog2(N)  // Ceiling of log2(N)
) (
  input  logic [      N-1:0] x,  // Input value to shift
  input  logic [D_WIDTH-1:0] d,  // Shift distance
  output logic [      N-1:0] z   // Output value
);

  logic [N-1:0] stage[D_WIDTH+1];  // Value after each stage; stage 0 is x

  assign stage[0] = x;

  // One stage per bit of d. Stage i shifts by 2^i if d[i] is set, so the
  // composition of the selected shifts equals the requested distance.
  generate
    genvar i;
    for (i = 0; i < D_WIDTH; i++) begin : gen_shifter_stages
      assign stage[i+1] = (d[i] == 1) ? stage[i] << (1 << i) : stage[i];
    end
  endgenerate

  assign z = stage[D_WIDTH];

endmodule
