`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 16.08.2023 22:52:20
// Design Name: 
// Module Name: clock_divider_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module clock_divider_tb;
    reg clk;
    reg rst;
    reg [15:0] period = 11'd20; // T/2
    wire sub_clk;
    
    clock_divider uut(clk, rst, period, sub_clk);

    initial begin 
        clk = 0;
        forever clk = #(1) ~clk;
    end
    
    initial begin
        rst = 1;
        #10 rst = 0;
        #1000;
    end
endmodule
