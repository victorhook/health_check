import logging
import time
from threading import Event

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander

logging.basicConfig(level=logging.ERROR)


class HealthTest:

    """
    Represents the Crazyflie and handles its connection to the radio.
    The callbacks are then passed to the main gui object which handles
    the communication between the visual graphics.
    """

    def __init__(self, uri, main_gui, test):

        self.cf = Crazyflie(rw_cache='./cache')
        self.uri = uri
        self.main_gui = main_gui
        self.link_is_open = False
        self.is_hover_test_running = False
        self.motor_means = [0, 0, 0, 0]
        self.motor_mean_counter = 0
        self._connect = Event()
        self._logconfig = Event()
        self.test = test
        self.variance = {}
    
    
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
                self._logconfig.wait()


            return self

    def run_test(self):
        if self.test == 'propeller':
            self.propeller_test()
        else:
            self.hover_test()


    def hover_test(self):
        """ 
        Takes off and hovers at x m for y seconds.
        Default is 0.5m and 5 seconds.
        A mean motor thrust for each motor is taken and
        passed to the main gui for calculations.
        """
        height = 0.5
        duration = 5

        self.main_gui.running_test(self.uri)
        
        MotionCommander.VELOCITY = 0.8
        with MotionCommander(self.cf, height) as mc:
            self.is_hover_test_running = True
            mc.stop()
            time.sleep(duration)

        self.hover_test_done()

    def propeller_test(self):
        self.main_gui.running_test(self.uri)

        self.cf.param.set_value('health.startPropTest', '0')
        time.sleep(0.2)

        self.initial_counter = self.motor_pass_counter

        self.cf.param.set_value('health.startPropTest', "1")
        time.sleep(5)

        while self.initial_counter == self.motor_pass_counter:
            time.sleep(0.1)

        self.propeller_test_done()


    def hover_test_done(self):
        try:
            means = [(total / self.motor_mean_counter) for total in self.motor_means]
        finally:
            self.main_gui.hover_test_done(self.uri, means)

    def propeller_test_done(self):
        """ Sends the results to the main gui object """
        self.main_gui.propeller_test_done(self.motorlog, self.uri)
        
    
    def add_callbacks(self):
        self.cf.connected.add_callback(self.connected)
        self.cf.disconnected.add_callback(self.disconnected)
        self.cf.connection_failed.add_callback(self.connection_failed)
        self.cf.connection_lost.add_callback(self.connection_lost)

    
    def remove_callbacks(self):
        try:
            self.cf.connected.remove_callback(self.connected)
            self.cf.connection_lost.remove_callback(self.connection_lost)
            self.cf.connection_failed.remove_callback(self.connection_failed)
            self.cf.disconnected.remove_callback(self.disconnected)

        except ValueError:
            pass


    def close_link(self):
        self.cf.close_link()
        self.remove_callbacks()
        self.link_is_open = False


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
        self._log.add_variable('health.motorTestCount', 'uint16_t')
        self._log.add_variable('health.motorPass', 'uint8_t')
        self._log.data_received_cb.add_callback(self.log_callback)

        self.cf.log.add_config(self._log)
        self._log.start()
        self._logconfig.set()


    def log_callback(self, timestamp, data, logconf):

        m1, m2 = data['pwm.m1_pwm'], data['pwm.m2_pwm']
        m3, m4 = data['pwm.m3_pwm'], data['pwm.m4_pwm']
        motor_values = [m1, m2, m3, m4]
        battery = data['pm.vbatMV']
        self.motorlog = data['health.motorPass']
        self.motor_pass_counter = data['health.motorTestCount']

        if self.is_hover_test_running:
            for i, data in enumerate(motor_values):
                self.motor_means[i] += data        
            self.motor_mean_counter += 1    

        self.main_gui.cb_logs(self.uri, motor_values, battery)


    # Connection callbacks from Crazyflie

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

        
    def __enter__(self):
        """ In case of use with wrapper """
        self.open_link()

    def __exit__(self, *args):
        """ In case of use with wrapper """
        self.close_link()