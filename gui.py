import tkinter as tk
from threading import Thread
import time

from crazyHealthTest import HealthTest
import cflib.crtp
from top import TopFrame
from main import MainFrame, Calculate, LogFrame


class Gui:

    """ 
    Main GUI object that handles communication between the visual
    layer and the Crazyflie.
    It consists of a Top frame, which is the menu and a main frame,
    which contains all the visual logs to the Crazyflie.
    """

    def __init__(self, root):

        self.topframe = TopFrame(root, self)
        self.mainframe = MainFrame(root, self)
        self.uris = {}

    def add_uri(self, uri):
        """ 
        Tries to add a URI to the listbox and make a new LogFrame
        object out of it. Raises a warning message is URI already exists
        """
        try:
            self.mainframe.canvas.delete('warning')
        finally:
            if uri not in self.uris:
                self.topframe.uribox.insert('end', uri)
                row, column = Calculate.row_and_col(self.uris)
                self.uris[uri] = LogFrame(self.mainframe.canvas, row, column, uri)
            else:
                self.mainframe.warning_msg('You already have that URI added')

    def del_uris(self, uris):
        for uri in uris:
            if uri in self.uris:
                self.uris[uri].delete()
                self.uris.pop(uri)
                
        def reposition_uris():
            for i, uri in enumerate(self.uris):
                row, column = Calculate.new_placements(i)
                self.uris[uri].delete()
                self.uris[uri] = LogFrame(self.mainframe.canvas, row, column, uri)

        reposition_uris()


    def clear_uris(self):
        for uri in self.uris:
            self.uris[uri].delete()
            self.uris.pop(uri)


    def run_test(self, test):
        """ Runs the chosen test on all Crazyflies, with their own threads """
        if self.uris:
            for uri in self.uris:
                try:
                    self.uris[uri].reset_motors()
                except AttributeError:
                    pass
                finally:
                    Thread(target=self.start, args=(uri, test)).start()
            
    def start(self, uri, test):
        cflib.crtp.init_drivers(enable_debug_driver=False)
        # try:

        cf = HealthTest(uri, self, test)
        try:
            cf.open_link()
            cf.run_test()
        finally:
            cf.close_link()

        # except AttributeError:
        #     self.warning_msg('Cannot find a Crazyradio Dongle')


    def warning_msg(self, msg):
        self.mainframe.warning_msg(msg)


    # Callbacks from Crazyflie

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


    def hover_test_done(self):
        pass

    def propeller_test_done(self, motorlog, uri):
        results, colors = Calculate.propeller_result(motorlog)
        self.uris[uri].update_motor_status(results, colors)




if __name__ == '__main__':
    root = tk.Tk()
    off_y = int( (root.winfo_screenheight() - 600) / 4 )
    off_x = int( (root.winfo_screenwidth() - 800) / 2 )
    
    root.geometry("800x600+{}+{}".format(off_x, off_y))
    gui = Gui(root)

    root.mainloop()