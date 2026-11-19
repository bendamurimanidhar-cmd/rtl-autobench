// Synchronous 8-word x 8-bit FIFO Buffer
module fifo_sync (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       wr_en,
    input  logic       rd_en,
    input  logic [7:0] wr_data,
    output logic [7:0] rd_data,
    output logic       full,
    output logic       empty
);

  logic [7:0] mem [0:7];
  logic [2:0] wr_ptr;
  logic [2:0] rd_ptr;
  logic [3:0] count;

  assign full  = (count == 4'd8);
  assign empty = (count == 4'd0);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      wr_ptr  <= 3'd0;
      rd_ptr  <= 3'd0;
      count   <= 4'd0;
      rd_data <= 8'd0;
    end else begin
      if (wr_en && !full) begin
        mem[wr_ptr] <= wr_data;
        wr_ptr      <= wr_ptr + 1'b1;
      end
      if (rd_en && !empty) begin
        rd_data <= mem[rd_ptr];
        rd_ptr  <= rd_ptr + 1'b1;
      end
      case ({wr_en && !full, rd_en && !empty})
        2'b10: count <= count + 1'b1;
        2'b01: count <= count - 1'b1;
        default: count <= count;
      endcase
    end
  end

endmodule
