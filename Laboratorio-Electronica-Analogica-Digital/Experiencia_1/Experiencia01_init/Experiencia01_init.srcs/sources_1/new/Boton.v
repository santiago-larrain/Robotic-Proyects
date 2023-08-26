`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12.12.2021 21:36:27
// Design Name: 
// Module Name: Boton
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

module debouncer(clk, bin, bout);
    input clk, bin;
    output bout;
    
    wire [22:0] r_max;
    reg result;
    assign r_max = 23'd5000000; 
    reg [22:0] counter;    
    
    initial begin
        result = 1'b0;
    end
    
    always @(posedge clk) 
    begin
        if (counter == r_max) 
            result = !result;
    end
    
    always @(posedge clk)
    begin
        if ((result==1'b1)^(bin == 1'b1)) 
            if (counter == r_max) 
                counter = 23'b0;
            else
                counter = counter + 23'd1;
        else
            counter = 23'b0;
    end
    
    assign bout = result;
    
endmodule

/////////////////////////////////////////////////////////////////////////


