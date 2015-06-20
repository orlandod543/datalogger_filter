__author__ = 'orlando'


import minimalmodbus

class be124( minimalmodbus.Instrument ):
    """Instrument class for bernini bs124 process controller.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """
    coils = {'remote_engine_start' :        0, # hola
             'remote_genset_start' :        1,
             'remote_stop' :                2,
             'remote_alarms_ack' :          3,
             'remote_emergency' :           4,
             'remote_toggle_gcb':           5,
             'remote_datalogger_run_stop':  6,
             'remote_dagalogger_erase':     7
            }

    input_registers = {'firmware_version'	:	30001,	#firmware
                        'L1_L2'	:	30004,	#VAC
                        'L2_L3'	:	30005,	#VAC
                        'L1_L3'	:	30006,	#VAC
                        'L1_N'	:	30007,	#VAC
                        'L2_N'	:	30008,	#VAC
                        'L3_N'	:	30009,	#VAC
                        'C1_A'	:	30010,	#(If CT SIZE =< 500 then Ax10)
                        'C2_A'	:	30011,	#(If CT SIZE =< 500 then Ax10)
                        'C3_A'	:	30012,	#(If CT SIZE =< 500 then Ax10)
                        'C_GND'	:	30013,	#A (If CT SIZE =< 500 then Ax10)
                        'KW_1'	:	30014,	#KW (If CT SIZE =< 500 then KWx10)
                        'KW_2'	:	30015,	#KW (If CT SIZE =< 500 then KWx10)
                        'KW_3'	:	30016,	#KW (If CT SIZE =< 500 then KWx10)
                        'KW_TOTAL'	:	30017,#KW (If CT SIZE =< 500 then KWx10)
                        'KVA_1'	:	30018,	#KVA (If CT SIZE =< 500 then KVAx10)
                        'KVA_2'	:	30019,	#KVA (If CT SIZE =< 500 then KVAx10)
                        'KVA_3'	:	30020,	#KVA (If CT SIZE =< 500 then KVAx10)
                        'KVA_TOTAL'	:	30021,#KVA (If CT SIZE =< 500 then KVAx10)
                        'KVAR_1'	:	30022,#KVAR (If CT SIZE =< 500 then KVARx10)
                        'KVAR_2'	:	30023,#KVAR (If CT SIZE =< 500 then KVARx10)
                        'KVAR_3'	:	30024,#KVAR (If CT SIZE =< 500 then KVARx10)
                        'KVAR_TOTAL'	:	30025,	#KVAR (If CT SIZE =< 500 then KVARx10)
                        'PF_1'	:	30026,	#	PF x 100
                        'PF_2'	:	30027,	#	PF x 100
                        'PF_3'	:	30028,	#	PF x 100
                        'PF_TOTAL'	:	30029,	#	PF x 100
                        'SEQUENCE'	:	30030,	# 0 - CW, 1 - CC
                        'FREQUENCY'	:	30031	#	Hz x 10
    }

    def __init__(self, portname, slaveaddress, baudrate, bytesize, stopbits, debug):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = baudrate
        self.serial.bytesize = bytesize
        self.serial.stopbits = stopbits


    def get_pv_loop1(self):
        """Return the process value (PV) for loop1."""
        return self.read_register(289, 1)

    def is_manual_loop1(self):
        """Return True if loop1 is in manual mode."""
        return self.read_register(273, 1) > 0

    def get_sptarget_loop1(self):
        """Return the setpoint (SP) target for loop1."""
        return self.read_register(2, 1)

    def get_sp_loop1(self):
        """Return the (working) setpoint (SP) for loop1."""
        return self.read_register(5, 1)

    def set_sp_loop1(self, value):
        """Set the SP1 for loop1.

        Note that this is not necessarily the working setpoint.

        Args:
            value (float): Setpoint (most often in degrees)
        """
        self.write_register(24, value, 1)

    def disable_sprate_loop1(self):
        """Disable the setpoint (SP) change rate for loop1. """
        VALUE = 1
        self.write_register(78, VALUE, 0)

if __name__ == "__main__":
    prueba = be124('/dev/tty2',1,9600,8,2,True)
    print prueba.read_register(1)
   # prueba.print_coils()
