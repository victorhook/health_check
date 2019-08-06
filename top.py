import tkinter as tk
from tkinter import ttk

green = '#95C943'
gray = '#676767'

class TopFrame(tk.Frame):

    def __init__(self, root, main_gui):
        super().__init__(root, width=800, height=150, bd=2, relief='ridge')

        self.main_gui = main_gui
        self.pack()
        self.pack_propagate(0)
        self.grid_propagate(0)

        self.chosen_pos_system = None

        self.uri_box()
        self.buttons()
        self.test_options()

    def test_options(self):
        """ Hover or Propeller test as well as positioning system """
        self.test_label = tk.Label(self, font='Courier 16', fg=green, text='Test')
        self.test_label.grid(row=0, column=2)
        self.test = ttk.Combobox(self, values=['Propeller Test', 'Hover Test'], state='readonly')
        self.test.grid(row=1, column=2)
        self.test.set('Propeller Test')

        self.pos_label = tk.Label(self, font='Courier 16', fg=green, text='Positioning System')
        self.pos_label.grid(row=0, column=3)

        self.pos_LH = tk.Checkbutton(self, font='Courier 12', fg=green, text='LightHouse',
                                    command=lambda: self.pos_cb('LH'))
        self.pos_LH.grid(row=1, column=3)

        self.pos_flow = tk.Checkbutton(self, font='Courier 12', fg=green, text='Flow Deck',
                                    command=lambda: self.pos_cb('flow'))
        self.pos_flow.grid(row=2, column=3)


    def buttons(self):
        """ Buttons for controlling the URI listbox """

        self.add_btn = TopButton(self, 'Add URI', self._add)
        self.add_btn.grid(row=0, column=1, padx=10, pady=5)

        self.del_btn = TopButton(self, 'Delete URI', self._del)
        self.del_btn.grid(row=1, column=1, padx=10, pady=5)
        
        self.clear_btn = TopButton(self, 'Clear all', self._clear)
        self.clear_btn.grid(row=2, column=1, padx=10, pady=5)

        self.start_btn = TopButton(self, 'START', self.start, font='Courier 25', height=2, widt=8)
        self.start_btn.grid(row=2, column=2)


    def uri_box(self):
        """ Container for the Listbox, containing the URIS, and its scrollbar """

        self.uri_frame = tk.Frame(self, height=135, width=250, bd=2, relief='ridge')
        self.uri_frame.grid(rowspan=3, column=0, pady=5, padx=5)
        self.uri_frame.pack_propagate(0)

        self.uribox = tk.Listbox(self.uri_frame, width=28, font='Courier 13', 
                                selectmode='extended', activestyle='none', 
                                selectbackground=green)
        self.uribox.pack(side='left')

        self.uriscroll = tk.Scrollbar(self.uri_frame, orient='vertical', command=self.uribox.yview)
        self.uriscroll.pack(side='right', fill='y')
        self.uribox['yscrollcommand'] = self.uriscroll.set

    
    def pos_cb(self, pos_type):
        if pos_type == 'LH':
            self.pos_flow.deselect()
            self.chosen_pos_system = 'LH'
        else:
            self.pos_LH.deselect()
            self.chosen_pos_system = 'flow'

    def add_uri(self, uri):
        self.uribox.insert('end', uri)
        self.main_gui.add_uri(uri)
        try:
            self.main_gui.mainframe.canvas.delete('warning')
        except:
            pass

    def _del(self):
        try:
            uris = self.uribox.curselection()
            self.main_gui.del_uris(self.uribox.get(uris[0], uris[-1]))
            self.uribox.delete(uris[0], uris[-1])
        except:
            pass


    def _clear(self):
        self.uribox.delete(0, 'end')

    def start(self):

        if not self.main_gui.uris:
            self.main_gui.warning_msg('You need to add a URI first')

        if self.test.get() == 'Propeller Test':
            self.main_gui.run_test('propeller')
        else:
            if self.chosen_pos_system == 'LH':
                self.start_hover_test('LH')
            elif self.chosen_pos_system == 'flow':
                self.start_hover_test('flow')
            else:
                self.warning_msg('You need to select Positioning System first')        
        
    def _add(self):
        popup = Popup(self)


class Popup:

    def __init__(self, master):

        self.popup = tk.Toplevel()
        self.popup.title('Add URI')
        self.master = master
        off_y = int( (master.winfo_screenheight() - 120) / 6 )
        off_x = int( (master.winfo_screenwidth() - 250) / 2 )
        self.popup.geometry('250x120+{}+{}'.format(off_x, off_y))

        self.uri = tk.Entry(self.popup, font='Coself.urier 12', width=28, bd=2, relief='ridge',
                            highlightthickness=0)
        self.uri.pack(pady=20)
        self.uri.insert(0, 'radio://0/10/2M/E7E7E7E7E7')

        self.add_btn = TopButton(self.popup, 'ADD', command=self.add_uri, font='Courier 20', width=6)
        self.add_btn.pack(pady=10)


    def add_uri(self):
        self.master.add_uri(self.uri.get())
        self.popup.destroy()
        del self

    
class TopButton(tk.Button):

    def __init__(self, master, text, command, **kwargs):
        super().__init__(master, font='Courier 12', fg=green, text=text, command=command)
        self.config(**kwargs)
        self.bind('<Enter>', lambda x: self.hover(True))
        self.bind('<Leave>', lambda x: self.hover(False))

    
    def hover(self, hovering):
        if hovering:
            self.config(fg='black')
        else:
            self.config(fg=green)

if __name__ == '__main__':
    root = tk.Tk()
    off_y = int( (root.winfo_screenheight() - 600) / 4 )
    off_x = int( (root.winfo_screenwidth() - 800) / 2 )
    
    root.geometry("800x600+{}+{}".format(off_x, off_y))
    gui = TopFrame(root)
    root.mainloop()


