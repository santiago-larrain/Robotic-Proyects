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
    input rst,
    input RsRx,
    output [6:0] sseg_ca,
    output [3:0] sseg_an,
    output sseg_dp
    //output [15:0] voltage 
    );
    
    parameter [15:0] baudrate = 16'd4800; // f = 100 MHz
    
    wire rx_rdy;
    wire [7:0] rx_data;
    wire [15:0] voltage;
    wire [6:0] dis1, dis2, dis3, dis4;
    
    // Receptor
    uart_rx uart_web(clk, RsRx, rx_rdy, rx_data);
    voltage_memory v_mem(clk, sw, rst, rx_rdy, rx_data[7:4], rx_data[3:0], voltage);
    
    // Display
    bcd7seg bcd_7seg(voltage, dis1, dis2, dis3, dis4);
    SevenSegController(clk, rst, dis1, dis2, dis3, dis4, sseg_ca, sseg_an, sseg_dp);
    
endmodule
