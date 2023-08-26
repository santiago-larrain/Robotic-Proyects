`timescale 100ps / 1ps
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
    wire [15:0] voltage;
    //wire rx_rdy;
    //wire [7:0] rx_data;

    top uut(clk, sw, rst, RsRx, voltage);

    initial begin 
        clk = 0;
        forever clk = #(1) ~clk;
    end

    initial begin 
    rst = 1;
    RsRx = 1;
    sw = 0;
    #20 rst = 0;
    #20;
    RsRx = 0;
    
    #128 RsRx = 1;
    #128 RsRx = 1;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    
    #128 RsRx = 1;
    #512;
    RsRx = 0;
    
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    
    #128 RsRx = 1;
    #512;
    RsRx = 0;
    
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    
    #128 RsRx = 1;
    #512;
    RsRx = 0;
    
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    
    #128 RsRx = 1;
    #512;
    sw = 1;
    RsRx = 0;
    
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    
    #128 RsRx = 1;
    #512;
    RsRx = 0;
    
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    
    #128 RsRx = 1;
    #512;
    RsRx = 0;
    
    #128 RsRx = 1;
    #128 RsRx = 1;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 0;
    #128 RsRx = 1;
    #128 RsRx = 0;
    
    #128 RsRx = 1;
    #512;
    end

    // A = 10010100

endmodule
