import tkinter as tk
from threading import Thread
import time

from crazyHealthTest import HealthTest
import cflib.crtp
from top import TopFrame
from main import MainFrame, Calculate, LogFrame


class Gui:

    def __init__(self, root):

        self.topframe = TopFrame(root, self)
        self.mainframe = MainFrame(root, self)
        self.uris = {}

    def add_uri(self, uri):
        if uri not in self.uris:
            row, column = Calculate.row_and_col(self.uris)
            self.uris[uri] = LogFrame(self.mainframe.canvas, row, column, uri)
        else:
            self.mainframe.warning_msg('You already have that URI added')

    def del_uris(self, uris):
        for uri in uris:
            if uri in self.uris:
                self.uris[uri].delete()
                self.uris.pop(uri)

    def connecting(self, uri):
        self.uris[uri].update_status_text('Connecting...')

    def connected(self, uri):
        self.uris[uri].clear_status_text()
        self.uris[uri].show_motors()
        self.uris[uri].show_battery()

    def connection_failed(self, uri):
        self.uris[uri].update_status_text('Connection Failed', fg='red')

    def connection_lost(self, uri):
        self.uris[uri].update_status_text('Connection Lost', fg='red')

    def disconnected(self, uri):
        self.uris[uri].update_status_text('Disconnected', fg='red')


    def cb_logs(self, uri, motor_values, battery):
        """
        Callback with all the logs from the Crazyflie 
        This gets sent to the LogFrame object that can represent
        the values visually
        """

        motor_text = Calculate.motor_text(motor_values)
        motor_fill = Calculate.motor_fill(motor_values)
        b_text, b_fill = Calculate.battery(battery)

        self.uris[uri].update_motors(motor_fill, motor_text)
        self.uris[uri].update_battery(b_text, b_fill)

    def run_test(self, test):
        if self.uris:
            for uri in self.uris:
                Thread(target=self.start, args=(uri, test)).start()

    def start(self, uri, test):
        cflib.crtp.init_drivers(enable_debug_driver=False)
        try:
            if test == 'propeller':
                cf = HealthTest(uri, self, 'propeller')
                try:
                    cf.open_link()
                    cf.run_test()
                finally:
                    cf.close_link()


            else:
                with HealthTest(uri, self, 'hover') as ht:
                        ht.run_test()
                        time.sleep(10)

        except AttributeError:
            self.warning_msg('Cannot find a Crazyradio Dongle')


    def hover_test_done(self):
        pass

    def propeller_test_done(self, motorlog, uri):
        results, colors = Calculate.propeller_result(motorlog)
        self.uris[uri].update_motor_status(results, colors)

    def warning_msg(self, msg):
        self.mainframe.warning_msg(msg)


if __name__ == '__main__':
    root = tk.Tk()
    off_y = int( (root.winfo_screenheight() - 600) / 4 )
    off_x = int( (root.winfo_screenwidth() - 800) / 2 )
    
    root.geometry("800x600+{}+{}".format(off_x, off_y))
    gui = Gui(root)

    root.mainloop()