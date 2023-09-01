`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 13.12.2021 00:04:11
// Design Name: 
// Module Name: display
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

module bcd7seg_base(num, dis);
    input [3:0] num;
    output reg [6:0] dis;
    
    always @(num)
        case(num)
            4'b0000: dis = 7'b1000000;   //0
            4'b0001: dis = 7'b1111001;   //1
            4'b0010: dis = 7'b0100100;   //2
            4'b0011: dis = 7'b0110000;   //3
            4'b0100: dis = 7'b0011001;   //4
            4'b0101: dis = 7'b0010010;   //5
            4'b0110: dis = 7'b0000010;   //6
            4'b0111: dis = 7'b1111000;   //7
            4'b1000: dis = 7'b0000000;   //8
            4'b1001: dis = 7'b0010000;   //9
            default: dis = 7'b1111111;   //Off
        endcase
endmodule

module bcd7seg(bcd, dis1, dis2, dis3, dis4);
    input [15:0] bcd;
    output wire [6:0] dis1, dis2, dis3, dis4;
    
    bcd7seg_base display_1 (bcd[15:12], dis1);
    bcd7seg_base display_2 (bcd[11:8], dis2);
    bcd7seg_base display_3 (bcd[7:4], dis3);
    bcd7seg_base display_4 (bcd[3:0], dis4);
endmodule

module SevenSegController(clk, dp_in, dis_a, dis_b, dis_c, dis_d, seg, an, dp);
    input clk, dp_in;
    input [6:0] dis_a, dis_b, dis_c, dis_d;
    output reg [6:0] seg;
    output reg [3:0] an;
    output reg dp;
    
    wire [16:0] clk_max;
    assign clk_max = 17'd1000;
    reg [16:0] clk_counter;
    reg [1:0] display;
    reg [3:0] number;

    always @(posedge clk)
    begin
        if (clk_counter >= clk_max) begin
            clk_counter <= 0;
            display <= display + 1;
        end
        else begin
            clk_counter <= clk_counter + 1;
        end
    end

    always @(*) begin
        case(display)
            2'b00: begin
                an = 4'b0111;
                seg = dis_a;
                dp = 1'b1;
            end
            2'b01: begin
                an = 4'b1011;
                seg = dis_b;
                dp = dp_in;
            end
            2'b10: begin
                an = 4'b1101;
                seg = dis_c;
                dp = 1'b1;
            end
            2'b11: begin
                an = 4'b1110;
                seg = dis_d;
                dp = 1'b1;
            end
            default: begin
                an = 4'b1111;
                seg = 7'b111_1111;
                dp = 1'b1;
            end
        endcase
    end

endmodule

//
//Módulo anterior, utilizado en Sistemas Digitales
//
//module bcd7seg_base(num, dis);
//  input [3:0] num;

//  output reg [6:0] dis;

//  // Variabes internas
//  wire In1, In2, In3, In4, s0, s1, s2, s3, A, B, C, D, E, F, G;

//  assign In1 = num[3];
//  assign In2 = num[2];
//  assign In3 = num[1];
//  assign In4 = num[0];
//  assign s0 = ~ num[3];
//  assign s1 = ~ num[2];
//  assign s2 = ~ num[1];
//  assign s3 = ~ num[0];

//  assign A = ((s0 & s1 & s2 & In4) | (In2 & s2 & s3));
//  assign B = ((In2 & s2 & In4) | (In2 & In3 & s3));
//  assign D = ((s0 & s1 & s2 & In4) | (In2 & s2 & s3) | (In2 & In3 & In4));
//  assign E = ((In2 & s2) | In4);
//  assign F = ((s0 & s1 & In4) | (s1 & In3) | (In3 & In4));
//  assign G = ((s0 & s1 & s2) | (s0 & In2 & In3 & In4));
//  assign C = (s1 & In3 & s3);
//  // Fin de variables internas

//  always @(*)
//    begin
//      if ( num <= 9)
//        begin
//          dis = {G, F, E, D, C, B, A};
//        end
//      else
//        begin
//          dis = 7'b1111111;
//        end
//    end
//endmodule

//module bcd7seg(a, b, c, d, dis1, dis2, dis3, dis4);
//  input [3:0] a, b, c, d;

//  output wire [6:0] dis1, dis2, dis3, dis4;

//  bcd7seg_base display_1 (.num(a), .dis(dis1));
//  bcd7seg_base display_2 (.num(b), .dis(dis2));
//  bcd7seg_base display_3 (.num(c), .dis(dis3));
//  bcd7seg_base display_4 (.num(d), .dis(dis4));
//endmodule