`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 15.08.2023 18:24:50
// Design Name: 
// Module Name: top
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


module top(
    input clk,
    input sw,
    input btnC,
    input RsRx,
    output [6:0] sseg_ca,
    output [3:0] sseg_an,
    output sseg_dp
    //output [15:0] voltage 
    );
    
    parameter [15:0] period = 16'd651; // f = 100 MHz clock -> period = f/baud_rate * 1/16
    
    wire rst;
    wire baud_en;
    wire rx_rdy;
    wire [7:0] rx_data;
    wire [15:0] voltage;
    wire [6:0] dis1, dis2, dis3, dis4;
    
    debouncer rst_debouncer(clk, btnC, rst);
    
    // Receptor
    one_shot_clock_divider os_cd(clk, rst, period, baud_en);
    uart_receptor uart_rx(clk, rst, baud_en, RsRx, rx_rdy, rx_data);
    voltage_memory v_mem(clk, sw, rst, rx_rdy, rx_data, voltage);
    
    // Display
    bcd7seg bcd_7seg(voltage[15:12], voltage[11:8], voltage[7:4], voltage[3:0], dis1, dis2, dis3, dis4);
    SevenSegController(clk, 1'b0, dis1, dis2, dis3, dis4, sseg_ca, sseg_an, sseg_dp);
    
endmodule
