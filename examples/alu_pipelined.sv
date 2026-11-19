// 4-bit Pipelined Arithmetic Logic Unit (ALU)
module alu_pipelined (
    input  logic        clk,
    input  logic        rst_n,
    input  logic [1:0]  opcode, // 00: ADD, 01: SUB, 10: AND, 11: OR
    input  logic [3:0]  op_a,
    input  logic [3:0]  op_b,
    output logic [3:0]  result,
    output logic        carry_out
);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      result    <= 4'b0000;
      carry_out <= 1'b0;
    end else begin
      case (opcode)
        2'b00: {carry_out, result} <= op_a + op_b;
        2'b01: {carry_out, result} <= {1'b0, op_a} - {1'b0, op_b};
        2'b10: begin
          result    <= op_a & op_b;
          carry_out <= 1'b0;
        end
        2'b11: begin
          result    <= op_a | op_b;
          carry_out <= 1'b0;
        end
      endcase
    end
  end

endmodule
