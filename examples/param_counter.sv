// ==============================================================================
// RTL-AutoBench Benchmark: Parameterized Up/Down Counter with Active-High Reset
// ==============================================================================
`timescale 1ns / 1ps

module param_counter #(
    parameter WIDTH = 8,
    parameter MAX_COUNT = 255
)(
    input  wire                 clk,
    input  wire                 rst,        // Active-High Synchronous Reset
    input  wire                 en,         // Count Enable
    input  wire                 up_down,    // 1: Up, 0: Down
    output reg  [WIDTH-1:0]     count,
    output reg                  overflow
);

    always @(posedge clk) begin
        if (rst) begin
            count    <= {WIDTH{1'b0}};
            overflow <= 1'b0;
        end else if (en) begin
            if (up_down) begin
                if (count == MAX_COUNT[WIDTH-1:0]) begin
                    count    <= {WIDTH{1'b0}};
                    overflow <= 1'b1;
                end else begin
                    count    <= count + 1'b1;
                    overflow <= 1'b0;
                end
            end else begin
                if (count == {WIDTH{1'b0}}) begin
                    count    <= MAX_COUNT[WIDTH-1:0];
                    overflow <= 1'b1;
                end else begin
                    count    <= count - 1'b1;
                    overflow <= 1'b0;
                end
            end
        end else begin
            overflow <= 1'b0;
        end
    end

endmodule
