// SPDX-FileCopyrightText: 2025 David Mallasén Quintana
// SPDX-License-Identifier: CERN-OHL-W-2.0+
// Source: https://github.com/davidmallasen/arithmetic_units
//
// Carry-skip adder
//
// Description: A carry-skip adder is a type of adder that improves the
// delay of a ripple-carry adder with little effort. The improvement is
// based on the observation that if for a group of bits the propagate
// signal is one for all of them, then the carry-out of the group is the
// same as the carry-in of the group. This allows to "skip" the ripple
// chain and reduce the delay.
//
// The adder is divided into M blocks of N/M bits each. The number of
// blocks, M, is a parameter of the module, and should be chosen to be
// close to sqrt(N) to optimize the delay. Each block is a ripple-carry
// adder. The carry-out of a block is selected between the ripple-carry
// adder's carry-out and the block's carry-in. The selection is done by
// a multiplexer controlled by the block's propagate signal.
//
// Area: O(N)
// Delay: O(sqrt(N))

module carry_skip_adder #(
  parameter int N = 32,
  parameter int M = 4    // Number of blocks
) (
  input  logic [N-1:0] x,    // First operand
  input  logic [N-1:0] y,    // Second operand
  input  logic         cin,  // Carry-in bit
  output logic [N-1:0] s,    // Output sum
  output logic         cout  // Carry-out bit
);

  localparam int BlockSize = N / M;  // Size of each block

  logic [  M:0] block_carry;  // Carry between blocks
  logic [M-1:0] block_propagate;  // Propagate signal for each block

  // Assign the carry-in of the first block
  assign block_carry[0] = cin;

  generate
    genvar i;
    for (i = 0; i < M; i++) begin : gen_blocks
      // Start and end bits for the current block
      localparam int Istart = i * BlockSize;
      localparam int Iend = (i + 1) * BlockSize - 1;

      logic block_cout;  // Carry-out of the ripple-carry adder

      // Instantiate a ripple-carry adder for each block
      carry_ripple_adder #(
        .N(BlockSize)
      ) rca_i (
        .x(x[Iend:Istart]),
        .y(y[Iend:Istart]),
        .cin(block_carry[i]),
        .s(s[Iend:Istart]),
        .cout(block_cout)
      );

      // Calculate the block's propagate signal
      assign block_propagate[i] = &((x[Iend:Istart] ^ y[Iend:Istart]));

      // Select the carry-out of the block
      assign block_carry[i+1]   = (block_propagate[i]) ? block_carry[i] : block_cout;
    end
  endgenerate

  // Assign the carry-out of the last block to the module's carry-out
  assign cout = block_carry[M];

endmodule
