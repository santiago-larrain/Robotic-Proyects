`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 18.08.2023 01:10:15
// Design Name: 
// Module Name: value_saver
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


module voltage_memory(
    input clk,
    input sw,
    input rst,
    input rx_rdy,
    input [7:0] rx_data,
    output [15:0] voltage
    );
    
    reg [15:0] V1;
    reg [15:0] V2;
    
    // Save Values
    always @(posedge clk) begin
        if (rst) begin
            V1 = 0;
            V2 = 0;
        end
        else if (rx_rdy)
            case(rx_data[7:4])
                4'b0000 : V1[3:0] = rx_data[3:0];    //uno v1
                4'b0001 : V1[7:4] = rx_data[3:0];    //diez v1
                4'b0010 : V1[11:8] = rx_data[3:0];   //cien v1
                4'b0011 : V1[15:12] = rx_data[3:0];  //mil v1
                4'b0100 : V2[3:0] = rx_data[3:0];    //uno v2
                4'b0101 : V2[7:4] = rx_data[3:0];    //diez v2
                4'b0110 : V2[11:8] = rx_data[3:0];   //dien v2
                4'b0111 : V2[15:12] = rx_data[3:0];  //mil v2
                default : begin
                          V1 = 16'b1001100001110101;
                          V2 = 16'b1001100001110101;
                          end
            endcase
    end
    
    assign voltage = sw ? V2 : V1;
endmodule
