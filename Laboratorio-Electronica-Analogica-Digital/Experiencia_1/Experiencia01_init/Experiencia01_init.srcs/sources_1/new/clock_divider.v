`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 16.08.2023 22:10:33
// Design Name: 
// Module Name: clock_divider
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: Frequency of Basys: 100 MHz -> period in [ms]. Máx T = 2.62 s
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module clock_divider(
    input clk, rst,
    input [15:0] period,
    output reg sub_clk = 0
    );
    
    reg [16:0] counter = 0;
    
    always @(posedge clk) begin
        if (rst) begin
            counter <= 17'd0;
            sub_clk = 1'b0;
        end
        else if (counter < period/2-1) begin
            counter <= counter + 1;
        end
        else begin
            sub_clk = ~sub_clk;
            counter <= 0;
        end
    end
endmodule

module one_shot_clock_divider(
    input clk, rst,
    input [15:0] period,
    output reg sub_clk = 0
    );
    
    reg [16:0] counter = 0;
    
    always @(posedge clk) begin
        if (rst) begin
            counter <= 0;
            sub_clk = 0;
        end
        else if (counter < period-1) begin
            counter <= counter + 1;
            sub_clk = 0;
        end
        else begin
            sub_clk = 1;
            counter <= 0;
        end
    end
endmodule
