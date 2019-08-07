import tkinter as tk

green = '#95C943'
gray = '#676767'

class MainFrame(tk.Frame):

    def __init__(self, root, main_gui):
        super().__init__(root, width=800, height=450, bd=2, relief='ridge')

        self.main_gui = main_gui

        self.pack()
        self.pack_propagate(0)

        self.canvas = tk.Canvas(self, width=770, height=450)
        self.canvas.pack(side='left')

        self.scroll = tk.Scrollbar(self, width=30, orient='vertical')
        self.scroll.pack(side='right', fill='y')

        self.canvas.config(yscrollcommand=self.scroll.set, scrollregion=self.canvas.bbox('all'))
        self.scroll.config(command=self.canvas.yview)

    def warning_msg(self, msg):
        self.canvas.delete('warning')
        self.canvas.create_text(385, 100, font='Courier 25', fill='red', text=msg, tags='warning')


class LogFrame():

    def __init__(self, master, row, column, uri):

        self.master = master
        self.uri = uri
        self.x = 255 * column
        self.y = 145 * row
        self.pad = 10

        self.master.create_rectangle(self.x + self.pad, self.y + self.pad, self.x+255,
                                    self.y+145, width=2, outline='black', fill=gray, tags=self.uri)

        self.master.create_text(self.x + 127, self.y + 25, text=uri, font='Courier 14 bold',
                                    fill=green, tags=self.uri)


    def delete(self):
        self.master.delete(self.uri)
        del self

    def update_battery(self, b_text, b_fill):
        self.master.itemconfig(self.b_text, text='{}V'.format(b_text))
        self.master.coords(self.b_fill, self.x + 20, self.y + 125, self.x + b_fill,
                        self.y + 140)

    def show_battery(self):
        """ Battery visual bar, 0-4.2 Volt """

        self.master.create_rectangle(self.x + 20, self.y + 125, self.x + 235,
                                    self.y + 140, tags=self.uri)
        self.b_fill = self.master.create_rectangle(self.x + 20, self.y + 125, self.x + 20,
                                    self.y + 140, fill='green', tags=self.uri)
        self.b_text = self.master.create_text(self.x + 140, self.y + 132, text="", font='Courier 13 bold',
                                    tags=self.uri)

    def show_motor_results(self):

        """ 
        Each motor has an outer frame, an inner frame (which is filled green when 
        the motor is used), its number, eg. 'M1' and an empty string which is
        used as a string variable representing the thrust.
        """
        # Motor 1
        self.master.create_rectangle(self.x + 18, self.y + 60, self.x + 68, self.y + 120,
                                outline='black', tags=self.uri)
        self.m1_fill = self.master.create_rectangle(self.x + 18, self.y + 120, self.x + 68, self.y + 120,
                                tags=self.uri, fill='green')
        self.master.create_text(self.x + 43, self.y + 75, text='M1', tags=self.uri,
                                font='Courier 16')
        self.m1_text = self.master.create_text(self.x + 43, self.y + 100, text='', tags=self.uri,
                                font='Courier 16')
        # Motor 2
        self.master.create_rectangle(self.x + 78, self.y + 60, self.x + 128, self.y + 120,
                                    outline='black', tags=self.uri)
        self.m2_fill = self.master.create_rectangle(self.x + 78, self.y + 120, self.x + 128, self.y + 120,
                                    tags=self.uri, fill='green')
        self.master.create_text(self.x + 103, self.y + 75, text='M2', tags=self.uri,
                                    font='Courier 16')
        self.m2_text = self.master.create_text(self.x + 103, self.y + 100, text='', tags=self.uri,
                                font='Courier 16')
        # Motor 3
        self.master.create_rectangle(self.x + 138, self.y + 60, self.x + 188, self.y + 120,
                                    outline='black', tags=self.uri)
        self.m3_fill = self.master.create_rectangle(self.x + 138, self.y + 120, self.x + 188, self.y + 120,
                                    tags=self.uri, fill='green')
        self.master.create_text(self.x + 163, self.y + 75, text='M3', tags=self.uri,
                                    font='Courier 16')
        self.m3_text = self.master.create_text(self.x + 160, self.y + 100, text='', tags=self.uri,
                                font='Courier 16')
        # Motor 4
        self.master.create_rectangle(self.x + 198, self.y + 60, self.x + 248, self.y + 120,
                                    outline='black', tags=self.uri)
        self.m4_fill = self.master.create_rectangle(self.x + 198, self.y + 120, self.x + 248, self.y + 120,
                                    tags=self.uri, fill='green')
        self.master.create_text(self.x + 223, self.y + 75, text='M4', tags=self.uri,
                                    font='Courier 16')
        self.m4_text = self.master.create_text(self.x + 223, self.y + 100, text='', tags=self.uri,
                                font='Courier 16')


    def update_motors(self, thrust_fill, thrust_text):
        """ 
        Updates all the motors with the visual effect of motor thrust as green filling
        as well as the thrust percentage in text
        """

        # Thrust filling (rectangle)
        self.master.coords(self.m1_fill, self.x + 18, self.y + 120, 
                        self.x + 68, self.y + 120 - thrust_fill[0])
        self.master.coords(self.m2_fill, self.x + 78, self.y + 120, 
                        self.x + 128, self.y + 120 - thrust_fill[1])
        self.master.coords(self.m3_fill, self.x + 138, self.y + 120, 
                            self.x + 188, self.y + 120 - thrust_fill[2])
        self.master.coords(self.m4_fill, self.x + 198, self.y + 120, 
                            self.x + 248, self.y + 120 - thrust_fill[3])
        # Thrust text
        self.master.itemconfig(self.m1_text, text='{}%'.format(thrust_text[0]))
        self.master.itemconfig(self.m2_text, text='{}%'.format(thrust_text[1]))
        self.master.itemconfig(self.m3_text, text='{}%'.format(thrust_text[2]))
        self.master.itemconfig(self.m4_text, text='{}%'.format(thrust_text[3]))


    def update_motor_status(self, results, colors):

        self.master.itemconfig(self.m1_text, text=results[0])
        self.master.itemconfig(self.m2_text, text=results[1])
        self.master.itemconfig(self.m3_text, text=results[2])
        self.master.itemconfig(self.m4_text, text=results[3])
        
        self.master.itemconfig(self.m1_fill, fill=colors[0])
        self.master.itemconfig(self.m2_fill, fill=colors[1])
        self.master.itemconfig(self.m3_fill, fill=colors[2])
        self.master.itemconfig(self.m4_fill, fill=colors[3])

        self.master.coords(self.m1_fill, self.x + 18, self.y + 60, 
                        self.x + 68, self.y + 120 )
        self.master.coords(self.m2_fill, self.x + 78, self.y + 60, 
                        self.x + 128, self.y + 120)
        self.master.coords(self.m3_fill, self.x + 138, self.y + 60, 
                            self.x + 188, self.y + 120)
        self.master.coords(self.m4_fill, self.x + 198, self.y + 60, 
                            self.x + 248, self.y + 120)


    def clear_status_text(self):
        try:
            self.master.delete(self.status_text)
        except:
            pass

    def update_status_text(self, msg, fg=green):
        """ Updates connection status to the Crazyflie """
        self.clear_status_text()
        self.status_text = self.master.create_text(self.x + 127, self.y + 45, text=msg, 
                                                font='Courier 15', fill=fg, tags=self.uri)



class Calculate:

    @staticmethod
    def motor_fill(motor_values):
        """
        The pwm callback from the motors is a value from 0-65535.
        This now maps it to a value corresponding to 0-60, which
        is needed to fill the visual canvas item object.
        """
        return [ int( (val / 65535) * 60) for val in motor_values ]

    @staticmethod
    def motor_text(motor_values):
        """
        The pwm callback from the motors is a value from 0-65535.
        This is mapped to 0-100, which corresponds to the percentage thrust
        """
        return [ int( (val / 65535) * 100) for val in motor_values ]

    @staticmethod
    def battery(battery):
        """ 
        The battery TOC is mapped to fill its corresponding voltage,
        in a green rectangle, and to a 1-decimal text string.
        """
        b_text = round( (battery / 1000), 1)
        b_fill = int( battery / 4200 * 215 )

        return b_text, b_fill

    @staticmethod
    def row_and_col(uris):
        row = int( len(uris) / 3 )
        column = len(uris) % 3
        return row, column

    @staticmethod
    def propeller_result(motorlog):
        binary = '{0:b}'.format(motorlog)
        motors = [binary[7], binary[6], binary[5], binary[4]]
        results =  ["GOOD" if motor=="1" else "BAD" for motor in motors]
        colors = ['green' if result=='GOOD' else 'red' for result in results]
        return results, colors

    @staticmethod
    def is_mean_ok(means):
        means = [(mean / 65535) for mean in means]
        average = (sum(means) / 4) * 100
        motor_results = []

        for mean in means:
            if abs(mean - average) > 20:
                motor_results.append(1)
            else:
                motor_results.append(0)

        results =  ["GOOD" if motor=="1" else "BAD" for motor in motor_results]
        colors = ['green' if result=='1' else 'red' for result in motor_results]

        print(results, colors)
