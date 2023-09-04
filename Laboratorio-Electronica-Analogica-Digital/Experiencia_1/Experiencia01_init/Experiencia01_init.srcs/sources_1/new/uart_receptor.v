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

//module uart_receptor_2(
//    input clk,
//    input rst,
//    input [15:0] baudrate,
//    input rx,
//    output reg rx_rdy,
//    output reg [7:0] rx_data
//    );
    
//    // ESTADOS
//    parameter IDLE =  3'b000;
//    parameter START = 3'b001;
//    parameter BIT =   3'b010;
//    parameter STOP =  3'b011;
//    parameter WAIT =  3'b100;
    
//    reg [2:0] state, nextstate = IDLE;
//    reg [2:0] bit_cnt = 0;
//    reg [3:0] clk_cnt = 0;
//    reg rst_clk = 0;
//    wire baud_en;
    
//    // Instanciar divisor de clock (16 veces más rápido que el baudrate)
//    one_shot_clock_divider clk_2 (clk, rst_clk || rst, 100000000/(baudrate*16), baud_en);
//    always @(posedge clk) begin
//        // Resetear clock en el instante que comienza a recibir información
//        if (state == IDLE && nextstate == START) begin
//            clk_cnt <= 0;
//            rst_clk <= 1;
//        end
//        else rst_clk = 0;
//    end
    
//    // Actualización del estado
//    // Ojo: Esta parte es secuancial
//    always @(posedge clk) begin
//        if (rst) begin
//            nextstate <= IDLE;
//            clk_cnt <= 0;
//            bit_cnt <= 0;
//            rx_rdy <= 0;
//            rx_data <= 8'd0;
//        end
//        else begin
//            state <= nextstate;
//            if (baud_en) begin
//                clk_cnt <= clk_cnt + 1;
//                if (clk_cnt == 15 && state == BIT) begin
//                    rx_data[bit_cnt] = rx;
//                    bit_cnt <= bit_cnt + 1;
//                end
//            end
//        end
//    end
    
//    // Logica para siguiente estado
//    // Ojo: Esta parte depende del clock dividido
//    always @(posedge baud_en) begin
//        case(state)
//            IDLE: begin 
//                if (rx == 0) begin         // 0 = bit de inicio
//                    nextstate <= START;    // Comenzar
//                    bit_cnt <= 0;          // Resetear conteo de bits
//                    clk_cnt <= 0;          // Resetear conteo de clocks para estar en fase
//                end
//                else nextstate <= IDLE;    // Conservar el estado en rx = 1
//            end
        
//            START: begin
//                if (clk_cnt < 7 && rx == 0) nextstate <= START;      // Mantenerse en Start durante medio ciclo
//                else if (clk_cnt < 7 && rx == 1) nextstate <= IDLE;  // Volver a IDLE, pues indica error en mensaje.
//                else if (clk_cnt == 7) begin
//                    nextstate <= BIT;                                // Entrar al estado de guardar datos
//                    clk_cnt <= 0;                                    // Desfasarse en 90° Con bits de entrada para muestrear sin errores
//                    bit_cnt <= 0;                                    // Resetear conteo de bits
//                end
//            end
    
//            BIT: begin
//                if (bit_cnt <= 7) nextstate <= BIT;                   // Quedarse en BIT hasta que se lean todos los datos del Byte
//                if (bit_cnt == 7 && clk_cnt == 15) nextstate <= STOP;  // Volver a desfasarme 90° para entrar correctamente a STOP
//            end
            
//            STOP: begin
//                if (clk_cnt < 15) nextstate = STOP;                    // Quedarse en STOP por medio ciclo y luego volver a IDLE, esto permite
//                else nextstate = IDLE;                                 // estar listo inmediatamente a recibir el siguiente Byte, pues se empieza
//            end                                                        // a esperar el bit de START incluso antes de que haya terminado el bit de STOP.
//        endcase
//    end
    
//    // Indicar que llegó un dato cuando este se recibió por completo, levantando una señal durante el bit de STOP.
//    always @(posedge clk) begin
//        case(state)
//            IDLE: begin
//                rx_rdy <= 0;
//            end
//            START: begin
//                rx_rdy <= 0;
//            end
//            BIT: begin
//                rx_rdy <= 0;
//            end
//            STOP: begin
//                rx_rdy <= 1;
//            end
//         endcase
//    end
//endmodule

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////
// File Downloaded from http://www.nandland.com
//////////////////////////////////////////////////////////////////////
// This file contains the UART Receiver.  This receiver is able to
// receive 8 bits of serial data, one start bit, one stop bit,
// and no parity bit.  When receive is complete o_rx_dv will be
// driven high for one clock cycle.
// 
// Set Parameter CLKS_PER_BIT as follows:
// CLKS_PER_BIT = (Frequency of i_Clock)/(Frequency of UART)
// Example: 10 MHz Clock, 115200 baud UART
// (10000000)/(115200) = 87
  
module uart_rx (
   input        i_Clock,
   input        i_Rx_Serial,
   output       o_Rx_DV,
   output [7:0] o_Rx_Byte
   );
  
  parameter CLKS_PER_BIT = 16'd20833;
  
  parameter s_IDLE         = 3'b000;
  parameter s_RX_START_BIT = 3'b001;
  parameter s_RX_DATA_BITS = 3'b010;
  parameter s_RX_STOP_BIT  = 3'b011;
  parameter s_CLEANUP      = 3'b100;
   
  reg           r_Rx_Data_R = 1'b1;
  reg           r_Rx_Data   = 1'b1;
   
  reg [15:0]    r_Clock_Count = 0;
  reg [2:0]     r_Bit_Index   = 0; //8 bits total
  reg [7:0]     r_Rx_Byte     = 0;
  reg           r_Rx_DV       = 0;
  reg [2:0]     r_SM_Main     = 0;
   
  // Purpose: Double-register the incoming data.
  // This allows it to be used in the UART RX Clock Domain.
  // (It removes problems caused by metastability)
  always @(posedge i_Clock)
    begin
      r_Rx_Data_R <= i_Rx_Serial;
      r_Rx_Data   <= r_Rx_Data_R;
    end
   
   
  // Purpose: Control RX state machine
  always @(posedge i_Clock)
    begin
       
      case (r_SM_Main)
        s_IDLE :
          begin
            r_Rx_DV       <= 1'b0;
            r_Clock_Count <= 0;
            r_Bit_Index   <= 0;
             
            if (r_Rx_Data == 1'b0)          // Start bit detected
              r_SM_Main <= s_RX_START_BIT;
            else
              r_SM_Main <= s_IDLE;
          end
         
        // Check middle of start bit to make sure it's still low
        s_RX_START_BIT :
          begin
            if (r_Clock_Count == (CLKS_PER_BIT-1)/2)
              begin
                if (r_Rx_Data == 1'b0)
                  begin
                    r_Clock_Count <= 0;  // reset counter, found the middle
                    r_SM_Main     <= s_RX_DATA_BITS;
                  end
                else
                  r_SM_Main <= s_IDLE;
              end
            else
              begin
                r_Clock_Count <= r_Clock_Count + 1;
                r_SM_Main     <= s_RX_START_BIT;
              end
          end // case: s_RX_START_BIT
         
         
        // Wait CLKS_PER_BIT-1 clock cycles to sample serial data
        s_RX_DATA_BITS :
          begin
            if (r_Clock_Count < CLKS_PER_BIT-1)
              begin
                r_Clock_Count <= r_Clock_Count + 1;
                r_SM_Main     <= s_RX_DATA_BITS;
              end
            else
              begin
                r_Clock_Count          <= 0;
                r_Rx_Byte[r_Bit_Index] <= r_Rx_Data;
                 
                // Check if we have received all bits
                if (r_Bit_Index < 7)
                  begin
                    r_Bit_Index <= r_Bit_Index + 1;
                    r_SM_Main   <= s_RX_DATA_BITS;
                  end
                else
                  begin
                    r_Bit_Index <= 0;
                    r_SM_Main   <= s_RX_STOP_BIT;
                  end
              end
          end // case: s_RX_DATA_BITS
     
     
        // Receive Stop bit.  Stop bit = 1
        s_RX_STOP_BIT :
          begin
            // Wait CLKS_PER_BIT-1 clock cycles for Stop bit to finish
            if (r_Clock_Count < CLKS_PER_BIT-1)
              begin
                r_Clock_Count <= r_Clock_Count + 1;
                r_SM_Main     <= s_RX_STOP_BIT;
              end
            else
              begin
                r_Rx_DV       <= 1'b1;
                r_Clock_Count <= 0;
                r_SM_Main     <= s_CLEANUP;
              end
          end // case: s_RX_STOP_BIT
     
         
        // Stay here 1 clock
        s_CLEANUP :
          begin
            r_SM_Main <= s_IDLE;
            r_Rx_DV   <= 1'b0;
          end
         
         
        default :
          r_SM_Main <= s_IDLE;
         
      endcase
    end   
   
  assign o_Rx_DV   = r_Rx_DV;
  assign o_Rx_Byte = r_Rx_Byte;
   
endmodule // uart_rx

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

//module uart_receptor(
//    input clk,
//    input rst,
//    input baud_en,
//    input rx,
//    output reg rx_rdy,
//    output reg [7:0] rx_data
//    );
    
//    // ESTADOS
//    parameter IDLE =  3'b000;
//    parameter START = 3'b001;
//    parameter BIT =   3'b010;
//    parameter STOP =  3'b011;
//    parameter WAIT =  3'b100;
    
//    reg [2:0] state, nextstate;
//    reg [2:0] bit_cnt;
//    reg [3:0] baud_cnt;
    
//    // Actualización del estado
//    // Ojo: Esta parte es secuencial
//    // BIT_CNT es un contador, por lo que también debe cambiar 
//    // de manera secuencial
//    always @(posedge clk) begin
//        if (rst) begin
//            nextstate <= IDLE;
//            baud_cnt <= 0;
//            bit_cnt <= 0;
//            rx_rdy <= 0;
//            rx_data <= 8'd0;
//        end
//        else begin
//            state <= nextstate;
//            if (baud_en) begin
//                baud_cnt <= baud_cnt + 1;
//                if (baud_cnt == 15 && state == BIT) begin
//                    rx_data[bit_cnt] = rx;
//                    bit_cnt <= bit_cnt + 1;
//                end
//            end
//        end
//    end
    
//    // Logica para siguiente estado
//    // Ojo: Esta parte es combinacional
    
//    always @(posedge clk) begin
//        case(state)
//        IDLE: begin 
//            if (baud_en && rx == 0) begin
//                nextstate <= START;
//                baud_cnt <= 0;
//                bit_cnt <= 0;
//            end
//            else nextstate <= IDLE;
//        end
    
//        START: begin
//            if (baud_cnt < 7) nextstate = START;
//            if (baud_cnt == 7 && rx == 0) begin
//                nextstate <= BIT;
//                baud_cnt <= 0;
//            end
//            if (rx == 1) nextstate = IDLE;
//        end
    
//        BIT: begin 
//            if (bit_cnt <= 7) nextstate = BIT;
//            if (baud_cnt == 15 && bit_cnt == 7) begin
//                nextstate <= STOP;
//                baud_cnt <= 0;
//            end
//        end
    
//        STOP: begin 
//            if (baud_cnt < 15) nextstate = STOP;
//            else begin
//                nextstate <= WAIT;
//                baud_cnt <= 0;
//                bit_cnt <= 0;
//            end
//        end
        
//        WAIT: begin 
//            if (baud_cnt < 7) nextstate = WAIT;
//            else begin
//                nextstate <= IDLE;
//                baud_cnt <= 0;
//            end
//        end
//        endcase
//    end
        
//    always @(posedge clk) begin
//        case(state)
//            IDLE: begin
//                rx_rdy <= 0;
//            end
//            START: begin
//                rx_rdy <= 0;
//            end
//            BIT: begin
//                rx_rdy <= 0;
//            end
//            STOP: begin 
//                rx_rdy <= 0;
//            end
//            WAIT: begin
//                rx_rdy <= 1;
//            end
//         endcase
//    end
    
    
//endmodule