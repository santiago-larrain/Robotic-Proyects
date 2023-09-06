`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 17.08.2023 17:24:16
// Design Name: 
// Module Name: uart_tb
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


module uart_tb;
    reg clk;
    reg sw;
    reg rst;
    reg RsRx;
    wire [6:0] sseg_ca;
    wire [3:0] sseg_an;
    wire sseg_dp;
    wire [8:0] LED;

    top uut(clk, sw, rst, RsRx, sseg_ca, sseg_an, sseg_dp, LED);

    initial begin 
        clk = 0;
        forever clk = #(5) ~clk;
    end

    initial begin 
    rst = 1;
    RsRx = 1;
    sw = 0;
    #104167 rst = 0;
    #104167 RsRx = 0;
    
    #104167 RsRx = 1;
    #104167 RsRx = 1;
    #104167 RsRx = 1;
    #104167 RsRx = 0;
    #104167 RsRx = 1;
    #104167 RsRx = 1;
    #104167 RsRx = 0;
    #104167 RsRx = 0;
    
    #104167 RsRx = 1;
    #208334;
    RsRx = 0;
    
    #104167 RsRx = 1;
    #104167 RsRx = 0;
    #104167 RsRx = 0;
    #104167 RsRx = 0;
    #104167 RsRx = 0;
    #104167 RsRx = 1;
    #104167 RsRx = 0;
    #104167 RsRx = 0;
    
    #104167 RsRx = 1;
    #208334;
//    RsRx = 0;
    
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
    
//    #128 RsRx = 1;
//    #512;
//    RsRx = 0;
    
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
    
//    #128 RsRx = 1;
//    #512;
//    sw = 1;
//    RsRx = 0;
    
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
    
//    #128 RsRx = 1;
//    #512;
//    RsRx = 0;
    
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
    
//    #128 RsRx = 1;
//    #512;
//    RsRx = 0;
    
//    #128 RsRx = 1;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 0;
//    #128 RsRx = 1;
//    #128 RsRx = 0;
    
//    #128 RsRx = 1;
//    #512;
    end

    // A = 10010100

endmodule
