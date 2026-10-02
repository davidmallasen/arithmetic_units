// SPDX-FileCopyrightText: 2025 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Carry-skip adder

module carry_skip_adder #(
  parameter int N = 32,
  parameter int M = 4    // Bit width of each block
) (
  input  logic [N-1:0] x,    // First operand
  input  logic [N-1:0] y,    // Second operand
  input  logic         cin,  // Carry-in bit
  output logic [N-1:0] s,    // Output sum
  output logic         cout  // Carry-out bit
);

  localparam int NumBlocks = N / M;  // Number of blocks

  logic [  NumBlocks:0] block_carry;  // Carry between blocks: entry 0 is cin,
                                      // entry NumBlocks is cout
  logic [NumBlocks-1:0] block_propagate;  // Group propagate of each block

  assign block_carry[0] = cin;

  generate
    genvar i;
    for (i = 0; i < NumBlocks; i++) begin : gen_blocks
      // Start and end bits for the current block
      localparam int Istart = i * M;
      localparam int Iend = (i + 1) * M - 1;

      logic block_cout;  // Carry-out of the block's carry-ripple adder

      carry_ripple_adder #(
        .N(M)
      ) cra_i (
        .x(x[Iend:Istart]),
        .y(y[Iend:Istart]),
        .cin(block_carry[i]),
        .s(s[Iend:Istart]),
        .cout(block_cout)
      );

      // Group propagate: 1 iff the block passes its carry through unchanged,
      // i.e. every bit position in the block has x ^ y = 1
      assign block_propagate[i] = &((x[Iend:Istart] ^ y[Iend:Istart]));

      // Skip mux: when the block propagates, the incoming carry bypasses
      // the block's ripple chain (the RCA's own carry-out equals its
      // carry-in in that case, so the result is unchanged)
      assign block_carry[i+1]   = (block_propagate[i]) ? block_carry[i] : block_cout;
    end
  endgenerate

  assign cout = block_carry[NumBlocks];

endmodule
