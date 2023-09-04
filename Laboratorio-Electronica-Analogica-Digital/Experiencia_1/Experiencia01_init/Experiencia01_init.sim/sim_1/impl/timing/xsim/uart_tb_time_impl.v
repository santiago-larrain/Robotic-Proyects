// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2020.1 (win64) Build 2902540 Wed May 27 19:54:49 MDT 2020
// Date        : Sat Sep  2 10:44:04 2023
// Host        : Phantom-YOGA running 64-bit major release  (build 9200)
// Command     : write_verilog -mode timesim -nolib -sdf_anno true -force -file
//               C:/Users/Santiago/Documentos/GitHub/Robotic-Proyects/Laboratorio-Electronica-Analogica-Digital/Experiencia_1/Experiencia01_init/Experiencia01_init.sim/sim_1/impl/timing/xsim/uart_tb_time_impl.v
// Design      : top
// Purpose     : This verilog netlist is a timing simulation representation of the design and should not be modified or
//               synthesized. Please ensure that this netlist is used with the corresponding SDF file.
// Device      : xc7a35tcpg236-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps
`define XIL_TIMING

module SevenSegController
   (sseg_an_OBUF,
    sseg_dp_OBUF,
    clk,
    rst_IBUF);
  output [3:0]sseg_an_OBUF;
  output sseg_dp_OBUF;
  input clk;
  input rst_IBUF;

  wire clear;
  wire clk;
  wire \clk_counter[0]_i_3_n_0 ;
  wire [16:3]clk_counter_reg;
  wire \clk_counter_reg[0]_i_2_n_0 ;
  wire \clk_counter_reg[0]_i_2_n_4 ;
  wire \clk_counter_reg[0]_i_2_n_5 ;
  wire \clk_counter_reg[0]_i_2_n_6 ;
  wire \clk_counter_reg[0]_i_2_n_7 ;
  wire \clk_counter_reg[12]_i_1_n_0 ;
  wire \clk_counter_reg[12]_i_1_n_4 ;
  wire \clk_counter_reg[12]_i_1_n_5 ;
  wire \clk_counter_reg[12]_i_1_n_6 ;
  wire \clk_counter_reg[12]_i_1_n_7 ;
  wire \clk_counter_reg[16]_i_1_n_7 ;
  wire \clk_counter_reg[4]_i_1_n_0 ;
  wire \clk_counter_reg[4]_i_1_n_4 ;
  wire \clk_counter_reg[4]_i_1_n_5 ;
  wire \clk_counter_reg[4]_i_1_n_6 ;
  wire \clk_counter_reg[4]_i_1_n_7 ;
  wire \clk_counter_reg[8]_i_1_n_0 ;
  wire \clk_counter_reg[8]_i_1_n_4 ;
  wire \clk_counter_reg[8]_i_1_n_5 ;
  wire \clk_counter_reg[8]_i_1_n_6 ;
  wire \clk_counter_reg[8]_i_1_n_7 ;
  wire \clk_counter_reg_n_0_[0] ;
  wire \clk_counter_reg_n_0_[1] ;
  wire \clk_counter_reg_n_0_[2] ;
  wire [1:0]display;
  wire \display[0]_i_1_n_0 ;
  wire \display[1]_i_1_n_0 ;
  wire \display[1]_i_2_n_0 ;
  wire \display[1]_i_3_n_0 ;
  wire \display[1]_i_4_n_0 ;
  wire rst_IBUF;
  wire [3:0]sseg_an_OBUF;
  wire sseg_dp_OBUF;
  wire [2:0]\NLW_clk_counter_reg[0]_i_2_CO_UNCONNECTED ;
  wire [2:0]\NLW_clk_counter_reg[12]_i_1_CO_UNCONNECTED ;
  wire [3:0]\NLW_clk_counter_reg[16]_i_1_CO_UNCONNECTED ;
  wire [3:1]\NLW_clk_counter_reg[16]_i_1_O_UNCONNECTED ;
  wire [2:0]\NLW_clk_counter_reg[4]_i_1_CO_UNCONNECTED ;
  wire [2:0]\NLW_clk_counter_reg[8]_i_1_CO_UNCONNECTED ;

  LUT6 #(
    .INIT(64'hFFFFFFFFEAAAAAAA)) 
    \clk_counter[0]_i_1 
       (.I0(clk_counter_reg[10]),
        .I1(\display[1]_i_2_n_0 ),
        .I2(clk_counter_reg[5]),
        .I3(clk_counter_reg[6]),
        .I4(clk_counter_reg[7]),
        .I5(\display[1]_i_4_n_0 ),
        .O(clear));
  LUT1 #(
    .INIT(2'h1)) 
    \clk_counter[0]_i_3 
       (.I0(\clk_counter_reg_n_0_[0] ),
        .O(\clk_counter[0]_i_3_n_0 ));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[0] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[0]_i_2_n_7 ),
        .Q(\clk_counter_reg_n_0_[0] ),
        .R(clear));
  (* ADDER_THRESHOLD = "11" *) 
  (* OPT_MODIFIED = "SWEEP" *) 
  CARRY4 \clk_counter_reg[0]_i_2 
       (.CI(1'b0),
        .CO({\clk_counter_reg[0]_i_2_n_0 ,\NLW_clk_counter_reg[0]_i_2_CO_UNCONNECTED [2:0]}),
        .CYINIT(1'b0),
        .DI({1'b0,1'b0,1'b0,1'b1}),
        .O({\clk_counter_reg[0]_i_2_n_4 ,\clk_counter_reg[0]_i_2_n_5 ,\clk_counter_reg[0]_i_2_n_6 ,\clk_counter_reg[0]_i_2_n_7 }),
        .S({clk_counter_reg[3],\clk_counter_reg_n_0_[2] ,\clk_counter_reg_n_0_[1] ,\clk_counter[0]_i_3_n_0 }));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[10] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[8]_i_1_n_5 ),
        .Q(clk_counter_reg[10]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[11] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[8]_i_1_n_4 ),
        .Q(clk_counter_reg[11]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[12] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[12]_i_1_n_7 ),
        .Q(clk_counter_reg[12]),
        .R(clear));
  (* ADDER_THRESHOLD = "11" *) 
  (* OPT_MODIFIED = "SWEEP" *) 
  CARRY4 \clk_counter_reg[12]_i_1 
       (.CI(\clk_counter_reg[8]_i_1_n_0 ),
        .CO({\clk_counter_reg[12]_i_1_n_0 ,\NLW_clk_counter_reg[12]_i_1_CO_UNCONNECTED [2:0]}),
        .CYINIT(1'b0),
        .DI({1'b0,1'b0,1'b0,1'b0}),
        .O({\clk_counter_reg[12]_i_1_n_4 ,\clk_counter_reg[12]_i_1_n_5 ,\clk_counter_reg[12]_i_1_n_6 ,\clk_counter_reg[12]_i_1_n_7 }),
        .S(clk_counter_reg[15:12]));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[13] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[12]_i_1_n_6 ),
        .Q(clk_counter_reg[13]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[14] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[12]_i_1_n_5 ),
        .Q(clk_counter_reg[14]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[15] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[12]_i_1_n_4 ),
        .Q(clk_counter_reg[15]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[16] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[16]_i_1_n_7 ),
        .Q(clk_counter_reg[16]),
        .R(clear));
  (* ADDER_THRESHOLD = "11" *) 
  CARRY4 \clk_counter_reg[16]_i_1 
       (.CI(\clk_counter_reg[12]_i_1_n_0 ),
        .CO(\NLW_clk_counter_reg[16]_i_1_CO_UNCONNECTED [3:0]),
        .CYINIT(1'b0),
        .DI({1'b0,1'b0,1'b0,1'b0}),
        .O({\NLW_clk_counter_reg[16]_i_1_O_UNCONNECTED [3:1],\clk_counter_reg[16]_i_1_n_7 }),
        .S({1'b0,1'b0,1'b0,clk_counter_reg[16]}));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[1] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[0]_i_2_n_6 ),
        .Q(\clk_counter_reg_n_0_[1] ),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[2] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[0]_i_2_n_5 ),
        .Q(\clk_counter_reg_n_0_[2] ),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[3] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[0]_i_2_n_4 ),
        .Q(clk_counter_reg[3]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[4] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[4]_i_1_n_7 ),
        .Q(clk_counter_reg[4]),
        .R(clear));
  (* ADDER_THRESHOLD = "11" *) 
  (* OPT_MODIFIED = "SWEEP" *) 
  CARRY4 \clk_counter_reg[4]_i_1 
       (.CI(\clk_counter_reg[0]_i_2_n_0 ),
        .CO({\clk_counter_reg[4]_i_1_n_0 ,\NLW_clk_counter_reg[4]_i_1_CO_UNCONNECTED [2:0]}),
        .CYINIT(1'b0),
        .DI({1'b0,1'b0,1'b0,1'b0}),
        .O({\clk_counter_reg[4]_i_1_n_4 ,\clk_counter_reg[4]_i_1_n_5 ,\clk_counter_reg[4]_i_1_n_6 ,\clk_counter_reg[4]_i_1_n_7 }),
        .S(clk_counter_reg[7:4]));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[5] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[4]_i_1_n_6 ),
        .Q(clk_counter_reg[5]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[6] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[4]_i_1_n_5 ),
        .Q(clk_counter_reg[6]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[7] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[4]_i_1_n_4 ),
        .Q(clk_counter_reg[7]),
        .R(clear));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[8] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[8]_i_1_n_7 ),
        .Q(clk_counter_reg[8]),
        .R(clear));
  (* ADDER_THRESHOLD = "11" *) 
  (* OPT_MODIFIED = "SWEEP" *) 
  CARRY4 \clk_counter_reg[8]_i_1 
       (.CI(\clk_counter_reg[4]_i_1_n_0 ),
        .CO({\clk_counter_reg[8]_i_1_n_0 ,\NLW_clk_counter_reg[8]_i_1_CO_UNCONNECTED [2:0]}),
        .CYINIT(1'b0),
        .DI({1'b0,1'b0,1'b0,1'b0}),
        .O({\clk_counter_reg[8]_i_1_n_4 ,\clk_counter_reg[8]_i_1_n_5 ,\clk_counter_reg[8]_i_1_n_6 ,\clk_counter_reg[8]_i_1_n_7 }),
        .S(clk_counter_reg[11:8]));
  FDRE #(
    .INIT(1'b0)) 
    \clk_counter_reg[9] 
       (.C(clk),
        .CE(1'b1),
        .D(\clk_counter_reg[8]_i_1_n_6 ),
        .Q(clk_counter_reg[9]),
        .R(clear));
  LUT5 #(
    .INIT(32'h0015FFEA)) 
    \display[0]_i_1 
       (.I0(\display[1]_i_4_n_0 ),
        .I1(\display[1]_i_3_n_0 ),
        .I2(\display[1]_i_2_n_0 ),
        .I3(clk_counter_reg[10]),
        .I4(display[0]),
        .O(\display[0]_i_1_n_0 ));
  LUT6 #(
    .INIT(64'h55555777AAAAA888)) 
    \display[1]_i_1 
       (.I0(display[0]),
        .I1(clk_counter_reg[10]),
        .I2(\display[1]_i_2_n_0 ),
        .I3(\display[1]_i_3_n_0 ),
        .I4(\display[1]_i_4_n_0 ),
        .I5(display[1]),
        .O(\display[1]_i_1_n_0 ));
  LUT4 #(
    .INIT(16'hE000)) 
    \display[1]_i_2 
       (.I0(clk_counter_reg[4]),
        .I1(clk_counter_reg[3]),
        .I2(clk_counter_reg[9]),
        .I3(clk_counter_reg[8]),
        .O(\display[1]_i_2_n_0 ));
  LUT3 #(
    .INIT(8'h80)) 
    \display[1]_i_3 
       (.I0(clk_counter_reg[7]),
        .I1(clk_counter_reg[6]),
        .I2(clk_counter_reg[5]),
        .O(\display[1]_i_3_n_0 ));
  LUT6 #(
    .INIT(64'hFFFFFFFFFFFFFFFE)) 
    \display[1]_i_4 
       (.I0(clk_counter_reg[15]),
        .I1(clk_counter_reg[16]),
        .I2(clk_counter_reg[13]),
        .I3(clk_counter_reg[14]),
        .I4(clk_counter_reg[12]),
        .I5(clk_counter_reg[11]),
        .O(\display[1]_i_4_n_0 ));
  FDRE #(
    .INIT(1'b0)) 
    \display_reg[0] 
       (.C(clk),
        .CE(1'b1),
        .D(\display[0]_i_1_n_0 ),
        .Q(display[0]),
        .R(1'b0));
  FDRE #(
    .INIT(1'b0)) 
    \display_reg[1] 
       (.C(clk),
        .CE(1'b1),
        .D(\display[1]_i_1_n_0 ),
        .Q(display[1]),
        .R(1'b0));
  LUT3 #(
    .INIT(8'hEF)) 
    dp
       (.I0(display[1]),
        .I1(rst_IBUF),
        .I2(display[0]),
        .O(sseg_dp_OBUF));
  LUT2 #(
    .INIT(4'h7)) 
    \sseg_an_OBUF[0]_inst_i_1 
       (.I0(display[1]),
        .I1(display[0]),
        .O(sseg_an_OBUF[0]));
  LUT2 #(
    .INIT(4'hB)) 
    \sseg_an_OBUF[1]_inst_i_1 
       (.I0(display[0]),
        .I1(display[1]),
        .O(sseg_an_OBUF[1]));
  LUT2 #(
    .INIT(4'hB)) 
    \sseg_an_OBUF[2]_inst_i_1 
       (.I0(display[1]),
        .I1(display[0]),
        .O(sseg_an_OBUF[2]));
  LUT2 #(
    .INIT(4'hE)) 
    \sseg_an_OBUF[3]_inst_i_1 
       (.I0(display[1]),
        .I1(display[0]),
        .O(sseg_an_OBUF[3]));
endmodule

(* ECO_CHECKSUM = "612d6d4b" *) (* baudrate = "16'b0010010110000000" *) 
(* NotValidForBitStream *)
module top
   (clk,
    sw,
    rst,
    RsRx,
    sseg_ca,
    sseg_an,
    sseg_dp,
    LED);
  input clk;
  input sw;
  input rst;
  input RsRx;
  output [6:0]sseg_ca;
  output [3:0]sseg_an;
  output sseg_dp;
  output [8:0]LED;

  wire [8:0]LED;
  wire [8:8]LED_OBUF;
  wire RsRx;
  wire RsRx_IBUF;
  wire clk;
  wire clk_IBUF;
  wire clk_IBUF_BUFG;
  wire rst;
  wire rst_IBUF;
  wire [3:0]sseg_an;
  wire [3:0]sseg_an_OBUF;
  wire [6:0]sseg_ca;
  wire sseg_dp;
  wire sseg_dp_OBUF;

initial begin
 $sdf_annotate("uart_tb_time_impl.sdf",,,,"tool_control");
end
  OBUF \LED_OBUF[0]_inst 
       (.I(1'b0),
        .O(LED[0]));
  OBUF \LED_OBUF[1]_inst 
       (.I(1'b0),
        .O(LED[1]));
  OBUF \LED_OBUF[2]_inst 
       (.I(1'b0),
        .O(LED[2]));
  OBUF \LED_OBUF[3]_inst 
       (.I(1'b0),
        .O(LED[3]));
  OBUF \LED_OBUF[4]_inst 
       (.I(1'b0),
        .O(LED[4]));
  OBUF \LED_OBUF[5]_inst 
       (.I(1'b0),
        .O(LED[5]));
  OBUF \LED_OBUF[6]_inst 
       (.I(1'b0),
        .O(LED[6]));
  OBUF \LED_OBUF[7]_inst 
       (.I(1'b0),
        .O(LED[7]));
  OBUF \LED_OBUF[8]_inst 
       (.I(LED_OBUF),
        .O(LED[8]));
  LUT1 #(
    .INIT(2'h1)) 
    \LED_OBUF[8]_inst_i_1 
       (.I0(RsRx_IBUF),
        .O(LED_OBUF));
  IBUF RsRx_IBUF_inst
       (.I(RsRx),
        .O(RsRx_IBUF));
  BUFG clk_IBUF_BUFG_inst
       (.I(clk_IBUF),
        .O(clk_IBUF_BUFG));
  IBUF clk_IBUF_inst
       (.I(clk),
        .O(clk_IBUF));
  SevenSegController nolabel_line51
       (.clk(clk_IBUF_BUFG),
        .rst_IBUF(rst_IBUF),
        .sseg_an_OBUF(sseg_an_OBUF),
        .sseg_dp_OBUF(sseg_dp_OBUF));
  IBUF rst_IBUF_inst
       (.I(rst),
        .O(rst_IBUF));
  OBUF \sseg_an_OBUF[0]_inst 
       (.I(sseg_an_OBUF[0]),
        .O(sseg_an[0]));
  OBUF \sseg_an_OBUF[1]_inst 
       (.I(sseg_an_OBUF[1]),
        .O(sseg_an[1]));
  OBUF \sseg_an_OBUF[2]_inst 
       (.I(sseg_an_OBUF[2]),
        .O(sseg_an[2]));
  OBUF \sseg_an_OBUF[3]_inst 
       (.I(sseg_an_OBUF[3]),
        .O(sseg_an[3]));
  OBUF \sseg_ca_OBUF[0]_inst 
       (.I(1'b0),
        .O(sseg_ca[0]));
  OBUF \sseg_ca_OBUF[1]_inst 
       (.I(1'b0),
        .O(sseg_ca[1]));
  OBUF \sseg_ca_OBUF[2]_inst 
       (.I(1'b0),
        .O(sseg_ca[2]));
  OBUF \sseg_ca_OBUF[3]_inst 
       (.I(1'b0),
        .O(sseg_ca[3]));
  OBUF \sseg_ca_OBUF[4]_inst 
       (.I(1'b0),
        .O(sseg_ca[4]));
  OBUF \sseg_ca_OBUF[5]_inst 
       (.I(1'b0),
        .O(sseg_ca[5]));
  OBUF \sseg_ca_OBUF[6]_inst 
       (.I(1'b1),
        .O(sseg_ca[6]));
  OBUF sseg_dp_OBUF_inst
       (.I(sseg_dp_OBUF),
        .O(sseg_dp));
endmodule
`ifndef GLBL
`define GLBL
`timescale  1 ps / 1 ps

module glbl ();

    parameter ROC_WIDTH = 100000;
    parameter TOC_WIDTH = 0;
    parameter GRES_WIDTH = 10000;
    parameter GRES_START = 10000;

//--------   STARTUP Globals --------------
    wire GSR;
    wire GTS;
    wire GWE;
    wire PRLD;
    wire GRESTORE;
    tri1 p_up_tmp;
    tri (weak1, strong0) PLL_LOCKG = p_up_tmp;

    wire PROGB_GLBL;
    wire CCLKO_GLBL;
    wire FCSBO_GLBL;
    wire [3:0] DO_GLBL;
    wire [3:0] DI_GLBL;
   
    reg GSR_int;
    reg GTS_int;
    reg PRLD_int;
    reg GRESTORE_int;

//--------   JTAG Globals --------------
    wire JTAG_TDO_GLBL;
    wire JTAG_TCK_GLBL;
    wire JTAG_TDI_GLBL;
    wire JTAG_TMS_GLBL;
    wire JTAG_TRST_GLBL;

    reg JTAG_CAPTURE_GLBL;
    reg JTAG_RESET_GLBL;
    reg JTAG_SHIFT_GLBL;
    reg JTAG_UPDATE_GLBL;
    reg JTAG_RUNTEST_GLBL;

    reg JTAG_SEL1_GLBL = 0;
    reg JTAG_SEL2_GLBL = 0 ;
    reg JTAG_SEL3_GLBL = 0;
    reg JTAG_SEL4_GLBL = 0;

    reg JTAG_USER_TDO1_GLBL = 1'bz;
    reg JTAG_USER_TDO2_GLBL = 1'bz;
    reg JTAG_USER_TDO3_GLBL = 1'bz;
    reg JTAG_USER_TDO4_GLBL = 1'bz;

    assign (strong1, weak0) GSR = GSR_int;
    assign (strong1, weak0) GTS = GTS_int;
    assign (weak1, weak0) PRLD = PRLD_int;
    assign (strong1, weak0) GRESTORE = GRESTORE_int;

    initial begin
	GSR_int = 1'b1;
	PRLD_int = 1'b1;
	#(ROC_WIDTH)
	GSR_int = 1'b0;
	PRLD_int = 1'b0;
    end

    initial begin
	GTS_int = 1'b1;
	#(TOC_WIDTH)
	GTS_int = 1'b0;
    end

    initial begin 
	GRESTORE_int = 1'b0;
	#(GRES_START);
	GRESTORE_int = 1'b1;
	#(GRES_WIDTH);
	GRESTORE_int = 1'b0;
    end

endmodule
`endif
