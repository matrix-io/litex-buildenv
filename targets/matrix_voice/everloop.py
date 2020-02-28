# Support for the MATRIX everloop
# https://www.matrix.one
# Author: Andres Calderon <andres.calderon@admobilize.com>
# FPGA: Spartan 6 xc6slx9-2-ftg256
# Copyright 2020 MATRIX Labs
# License: BSD

import os

from migen import *

from litex.soc.interconnect import wishbone

class Everloop(Module):
    def __init__(self, platform, nleds, everloop_pads):
        self.platform  = platform
        self.reset     = Signal()
        self.bus      = dbus = wishbone.Interface()

        # add verilog sources
        self.add_sources(platform)

        self.specials += Instance(
            "wb_everloop",
            name="everloop0",
            p_MEM_FILE_NAME="image.ram",
            p_SYS_FREQ_HZ=75000000,
            p_ADDR_WIDTH=dbus.adr_width,
            p_DATA_WIDTH=dbus.data_width,
            p_N_LEDS=nleds,

            i_clk=ClockSignal(),
            i_resetn=ResetSignal(),
            i_wb_stb_i=dbus.stb,
            i_wb_cyc_i=dbus.cyc,
            i_wb_we_i=dbus.we,
            i_wb_adr_i=dbus.adr,
            i_wb_sel_i=dbus.sel,
            i_wb_dat_i=dbus.dat_w,
            o_wb_dat_o=dbus.dat_r,
            o_wb_ack_o=dbus.ack,
            o_everloop_ctl=everloop_pads.ctl,
        )


    @staticmethod
    def add_sources(platform):
        platform.add_sources(os.path.join(
                             os.path.abspath(os.path.dirname(__file__)), "everloop"),
            "everloop_bram.v",
            "everloop_fsm.v",
            "everloop.v",
            "wb_everloop.v")
