import logging
import time
from threading import Event

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander

logging.basicConfig(level=logging.ERROR)

class HealthTest:

    def __init__(self, uri, main_gui, test):

        self.cf = Crazyflie(rw_cache='./cache')
        self.uri = uri
        self.main_gui = main_gui
        self.link_is_open = False
        self._connect = Event()
        self.test = test


    def run_test(self):
        if self.test == 'propeller':
            self.propeller_test()
            
        else:
            self.hover_test()


    def hover_test(self):
        with MotionCommander(self.cf) as mc:
            mc.take_off(0.5)
            


    def propeller_test(self):
        self.cf.param.set_value('health.startPropTest', '0')
        time.sleep(0.2)
        self.cf.param.set_value('health.startPropTest', "1")
        time.sleep(3)

        while self.motorlog < 128:
            time.sleep(0.1)
        
        self.propeller_test_done()

    def propeller_test_done(self):
        """ Sends the results to the main gui object """
        self.main_gui.propeller_test_done(self.motorlog, self.uri)
        
    
    def add_callbacks(self):
        self.cf.connected.add_callback(self.connected)
        self.cf.disconnected.add_callback(self.disconnected)
        self.cf.connection_failed.add_callback(self.connection_failed)
        self.cf.connection_lost.add_callback(self.connection_lost)

    def open_link(self):
        """ 
        Adds callbacks then tries to connect to the Crazyflie.
        If no response, send an error msg to main_gui (GUI) and
        remove callbacks, else, add log configurations.
        """
        if self.link_is_open:
            self.main_gui.warning_msg('Link is already open')

        else:
            self.add_callbacks()
            self.main_gui.connecting(self.uri)

            self.cf.open_link(self.uri)
            self._connect.wait()

            if not self.link_is_open:
                self.remove_callbacks()
                self.main_gui.warning_msg("Couldn't open link")
            else:
                self.add_logconfigs()

            return self

    def close_link(self):
        self.cf.close_link()
        self.remove_callbacks
        self.link_is_open = False


    def __enter__(self):
        self.open_link()

    def __exit__(self, *args):
        self.close_link()

    def remove_callbacks(self):
        try:
            self.cf.connected.remove_callback(self.connected)
            self.cf.connection_lost.remove_callback(self.connection_lost)
            self.cf.connection_failed.remove_callback(self.connection_failed)
            self.cf.disconnected.remove_callback(self.disconnected)

        except ValueError:
            pass

    def add_logconfigs(self):
        """
        The TOC's are motor thrust, battery level and results from propeller test
        """
        self._log = LogConfig(self.uri, period_in_ms=50)
        self._log.add_variable("pwm.m1_pwm", "uint32_t")
        self._log.add_variable("pwm.m2_pwm", "uint32_t")
        self._log.add_variable("pwm.m3_pwm", "uint32_t")
        self._log.add_variable("pwm.m4_pwm", "uint32_t")
        self._log.add_variable("pm.vbatMV", "uint16_t")
        self._log.add_variable('health.motorPass', 'uint8_t')
        self._log.data_received_cb.add_callback(self.log_callback)

        self.cf.log.add_config(self._log)

        self._log.start()

    def log_callback(self, timestamp, data, logconf):

        m1, m2 = data['pwm.m1_pwm'], data['pwm.m2_pwm']
        m3, m4 = data['pwm.m3_pwm'], data['pwm.m4_pwm']
        battery = data['pm.vbatMV']
        self.motorlog = data['health.motorPass']

        self.main_gui.cb_logs(self.uri, [m1, m2, m3, m4], battery)


    def connected(self, callback):
        self.link_is_open = True
        self._connect.set()
        self.main_gui.connected(self.uri)

    def disconnected(self, *args):
        self.main_gui.disconnected(self.uri)

    def connection_failed(self, *args):
        self.main_gui.connection_failed(self.uri)

    def connection_lost(self, *args):
        self.main_gui.connection_lost(self.uri)

    def __repr__(self):
        return self.uri

    


    

    