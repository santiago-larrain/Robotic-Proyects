`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 16.08.2023 21:49:33
// Design Name: 
// Module Name: uart_module
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


module uart_receptor(
    input clk,
    input rst,
    input baud_en,
    input rx,
    output reg rx_rdy,
    output reg [7:0] rx_data
    );
    
    // ESTADOS
    parameter IDLE =  3'b000;
    parameter START = 3'b001;
    parameter BIT =   3'b010;
    parameter STOP =  3'b011;
    parameter WAIT =  3'b100;
    
    reg [2:0] state, nextstate;
    reg [2:0] bit_cnt;
    reg [3:0] baud_cnt;
    
    // Actualización del estado
    // Ojo: Esta parte es secuencial
    // BIT_CNT es un contador, por lo que también debe cambiar 
    // de manera secuencial
    always @(posedge clk) begin
        if (rst) begin
            nextstate <= IDLE;
            baud_cnt <= 0;
            bit_cnt <= 0;
            rx_rdy = 0;
            rx_data = 8'd0;
        end
        else begin
            state <= nextstate;
            if (baud_en) begin
                baud_cnt <= baud_cnt + 1;
                if (baud_cnt == 15 && state == BIT) begin
                    rx_data[bit_cnt] = rx;
                    bit_cnt <= bit_cnt + 1;
                end
            end
        end
    end
    
    // Logica para siguiente estado
    // Ojo: Esta parte es combinacional
    
    always @(posedge clk) begin
        case(state)
        IDLE: begin 
            if (baud_en && rx == 0) begin
                nextstate = START;
                baud_cnt <= 0;
                bit_cnt <= 0;
            end
            else nextstate = IDLE;
        end
    
        START: begin
            if (baud_cnt < 7) nextstate = START;
            if (baud_cnt == 7 && rx == 0) begin
                nextstate = BIT;
                baud_cnt <= 0;
            end
            if (rx == 1) nextstate = IDLE;
        end
    
        BIT: begin 
            if (bit_cnt <= 7) nextstate = BIT;
            if (baud_cnt == 15 && bit_cnt == 7) begin
                nextstate = STOP;
                baud_cnt <= 0;
            end
        end
    
        STOP: begin 
            if (baud_cnt < 15) nextstate = STOP;
            else begin
                nextstate = WAIT;
                baud_cnt <= 0;
                bit_cnt <= 0;
            end
        end
        
        WAIT: begin 
            if (baud_cnt < 7) nextstate = WAIT;
            else begin
                nextstate = IDLE;
                baud_cnt <= 0;
            end
        end
        endcase
    end
        
    always @(posedge clk) begin
        case(state)
            IDLE: begin
                rx_rdy = 0;
            end
            START: begin
                rx_rdy = 0;
            end
            BIT: begin
                rx_rdy = 0;
            end
            STOP: begin 
                rx_rdy = 0;
            end
            WAIT: begin
                rx_rdy = 1;
            end
         endcase
    end
    
    
endmodule

