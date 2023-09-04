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
    input [3:0] rx_pos,
    input [3:0] rx_data,
    output reg [15:0] voltage
    );
    
    reg [15:0] V1;
    reg [15:0] V2;
    
    // Save Values
    always @(posedge clk) begin
        if (rst) begin
            V1 <= 16'd0;
            V2 <= 16'd0;
        end
        else if (rx_rdy)
            case(rx_pos)
                4'b0000 : V1[3:0]   <= rx_data;  //uno v1
                4'b0001 : V1[7:4]   <= rx_data;  //diez v1
                4'b0010 : V1[11:8]  <= rx_data;  //cien v1
                4'b0011 : V1[15:12] <= rx_data;  //mil v1
                4'b0100 : V2[3:0]   <= rx_data;  //uno v2
                4'b0101 : V2[7:4]   <= rx_data;  //diez v2
                4'b0110 : V2[11:8]  <= rx_data;  //dien v2
                4'b0111 : V2[15:12] <= rx_data;  //mil v2
                default : begin
                              V1 <= 16'd0;
                              V2 <= 16'd0;
                          end
            endcase
            
            // Asignar voltaje según valor de switch
            case(sw)
                1'b0 : voltage = V1;
                1'b1 : voltage = V2;
            endcase
    end
    
endmodule
