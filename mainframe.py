import tkinter as tk

green = '#95C943'
gray = '#676767'

class MainFrame(tk.Frame):

    """ Main container for the Crazyflie Log objects. """

    def __init__(self, root, main_gui):
        super().__init__(root, width=800, height=450, bd=2, relief='ridge')

        self.main_gui = main_gui
        self.pack()
        self.pack_propagate(0)

        self.canvas = tk.Canvas(self, width=770, height=450)
        self.canvas.pack(side='left')

        self.scroll = tk.Scrollbar(self, width=30, orient='vertical')
        self.scroll.pack(side='right', fill='y')

        self.canvas.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.canvas.yview)

    def update_canvas_scroll(self):
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def warning_msg(self, msg):
        self.canvas.create_text(385, 100, font='Courier 25', fill='red', 
                                text=msg, tags='warning')


class LogFrame():

    """
    Log object that visually represents the levels of the Crazyflie.
    These are all made as object of the canvas frame in the MainFrame,
    and are tagged with their URI.
    """

    def __init__(self, master, row, column, uri):

        self.master = master
        self.uri = uri
        self.x = 255 * column
        self.y = 145 * row
        self.pad = 10
        self.test_is_done = False

        self.master.create_rectangle(self.x + self.pad, self.y + self.pad, self.x+255,
                                    self.y+145, width=2, outline='black', fill=gray, tags=self.uri)

        self.master.create_text(self.x + 130, self.y + 25, text=uri, font='Courier 11',
                                    fill=green, tags=self.uri)


    def show_battery(self):
        """ Battery visual bar, 0-4.2 Volt """

        self.master.create_rectangle(self.x + 20, self.y + 125, self.x + 235,
                                    self.y + 140, tags=self.uri)
        self.b_fill = self.master.create_rectangle(self.x + 20, self.y + 125, self.x + 20,
                                    self.y + 140, fill='green', tags=self.uri)
        self.b_text = self.master.create_text(self.x + 140, self.y + 132, text="", font='Courier 13 bold',
                                    tags=self.uri)

    def show_motors(self):

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
        self.m1_text = self.master.create_text(self.x + 45, self.y + 100, text='', tags=self.uri,
                                font='Courier 14')
        # Motor 2
        self.master.create_rectangle(self.x + 78, self.y + 60, self.x + 128, self.y + 120,
                                    outline='black', tags=self.uri)
        self.m2_fill = self.master.create_rectangle(self.x + 78, self.y + 120, self.x + 128, self.y + 120,
                                    tags=self.uri, fill='green')
        self.master.create_text(self.x + 103, self.y + 75, text='M2', tags=self.uri,
                                    font='Courier 16')
        self.m2_text = self.master.create_text(self.x + 103, self.y + 100, text='', tags=self.uri,
                                font='Courier 14')
        # Motor 3
        self.master.create_rectangle(self.x + 138, self.y + 60, self.x + 188, self.y + 120,
                                    outline='black', tags=self.uri)
        self.m3_fill = self.master.create_rectangle(self.x + 138, self.y + 120, self.x + 188, self.y + 120,
                                    tags=self.uri, fill='green')
        self.master.create_text(self.x + 163, self.y + 75, text='M3', tags=self.uri,
                                    font='Courier 16')
        self.m3_text = self.master.create_text(self.x + 160, self.y + 100, text='', tags=self.uri,
                                font='Courier 14')
        # Motor 4
        self.master.create_rectangle(self.x + 198, self.y + 60, self.x + 248, self.y + 120,
                                    outline='black', tags=self.uri)
        self.m4_fill = self.master.create_rectangle(self.x + 198, self.y + 120, self.x + 248, self.y + 120,
                                    tags=self.uri, fill='green')
        self.master.create_text(self.x + 223, self.y + 75, text='M4', tags=self.uri,
                                    font='Courier 16')
        self.m4_text = self.master.create_text(self.x + 223, self.y + 100, text='', tags=self.uri,
                                font='Courier 14')


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


    def delete(self):
        """ Deletes the object by its tags as well as the object instantiated """
        self.master.delete(self.uri)
        del self


    def update_battery(self, b_text, b_fill):
        self.master.itemconfig(self.b_text, text='{}V'.format(b_text))
        self.master.coords(self.b_fill, self.x + 20, self.y + 125, self.x + b_fill,
                        self.y + 140)


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
        """ Updates the status of the motors when a test is finished. GOOD/BAD """
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


    def reset_motors(self):
        self.test_is_done = False
        self.master.itemconfig(self.m1_text, text='')
        self.master.itemconfig(self.m2_text, text='')
        self.master.itemconfig(self.m3_text, text='')
        self.master.itemconfig(self.m4_text, text='')

        self.master.itemconfig(self.m1_fill, fill='green')
        self.master.itemconfig(self.m2_fill, fill='green')
        self.master.itemconfig(self.m3_fill, fill='green')
        self.master.itemconfig(self.m4_fill, fill='green')

        self.master.coords(self.m1_fill, self.x + 18, self.y + 120, 
                        self.x + 68, self.y + 120)
        self.master.coords(self.m2_fill, self.x + 78, self.y + 120, 
                        self.x + 128, self.y + 120)
        self.master.coords(self.m3_fill, self.x + 138, self.y + 120, 
                            self.x + 188, self.y + 120)
        self.master.coords(self.m4_fill, self.x + 198, self.y + 120, 
                            self.x + 248, self.y + 120)


    def reset_battery(self):
        self.master.coords(self.b_fill, self.x + 20, self.y + 125, self.x + 20,
                        self.y + 140)
        self.master.itemconfig(self.b_text, text='')