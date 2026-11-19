// 4-State Traffic Controller Finite State Machine
module fsm_traffic_ctrl (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       sensor_car,
    output logic [2:0] light_main, // Red[2], Yellow[1], Green[0]
    output logic [2:0] light_side
);

  localparam [1:0] S_MAIN_GREEN  = 2'b00;
  localparam [1:0] S_MAIN_YELLOW = 2'b01;
  localparam [1:0] S_SIDE_GREEN  = 2'b10;
  localparam [1:0] S_SIDE_YELLOW = 2'b11;

  logic [1:0] current_state, next_state;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      current_state <= S_MAIN_GREEN;
    else
      current_state <= next_state;
  end

  always_comb begin
    next_state = current_state;
    case (current_state)
      S_MAIN_GREEN:  if (sensor_car) next_state = S_MAIN_YELLOW;
      S_MAIN_YELLOW: next_state = S_SIDE_GREEN;
      S_SIDE_GREEN:  if (!sensor_car) next_state = S_SIDE_YELLOW;
      S_SIDE_YELLOW: next_state = S_MAIN_GREEN;
      default:       next_state = S_MAIN_GREEN;
    endcase
  end

  always_comb begin
    case (current_state)
      S_MAIN_GREEN:  begin light_main = 3'b001; light_side = 3'b100; end
      S_MAIN_YELLOW: begin light_main = 3'b010; light_side = 3'b100; end
      S_SIDE_GREEN:  begin light_main = 3'b100; light_side = 3'b001; end
      S_SIDE_YELLOW: begin light_main = 3'b100; light_side = 3'b010; end
      default:       begin light_main = 3'b100; light_side = 3'b100; end
    endcase
  end

endmodule
