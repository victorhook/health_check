import tkinter as tk
from tkinter import ttk

green = '#95C943'

class TopFrame(tk.Frame):
    """
    Top fram contains the menu to add URI's and choose which test to run
    """

    def __init__(self, root, main_gui):
        super().__init__(root, width=800, height=150, bd=2, relief='ridge')

        self.main_gui = main_gui
        self.pack()
        self.grid_propagate(0)
        self.show_uri_box()
        self.show_buttons()
        self.show_test_options()


    def show_test_options(self):
        """ Hover or Propeller test """

        self.test_label = tk.Label(self, font='Courier 16', fg=green, text='Test')
        self.test_label.grid(row=0, column=2)
        self.test = ttk.Combobox(self, values=['Propeller Test', 'Hover Test'], state='readonly')
        self.test.grid(row=1, column=2)
        self.test.set('Propeller Test')


    def show_buttons(self):
        """ Buttons for controlling the URI listbox """

        self.add_btn = TopButton(self, 'Add URI', self._add)
        self.add_btn.grid(row=0, column=1, padx=20, pady=5)

        self.del_btn = TopButton(self, 'Delete URI', self._del)
        self.del_btn.grid(row=1, column=1, padx=20, pady=5)
        
        self.clear_btn = TopButton(self, 'Clear all', self._clear)
        self.clear_btn.grid(row=2, column=1, padx=20, pady=5)

        self.start_btn = TopButton(self, 'START', self._start, font='Courier 25', width=8)
        self.start_btn.grid(row=2, column=2)


    def show_uri_box(self):
        """ Container for the Listbox, containing the URIS, and its scrollbar """

        self.uri_frame = tk.Frame(self, height=135, width=350, bd=2, relief='ridge')
        self.uri_frame.grid(rowspan=3, column=0, pady=5, padx=5)
        self.uri_frame.pack_propagate(0)

        self.uribox = tk.Listbox(self.uri_frame, width=35, font='Courier 11', 
                                selectmode='extended', activestyle='none', 
                                selectbackground=green)
        self.uribox.pack(side='left')

        self.uriscroll = tk.Scrollbar(self.uri_frame, orient='vertical', command=self.uribox.yview)
        self.uriscroll.pack(side='right', fill='y')
        self.uribox['yscrollcommand'] = self.uriscroll.set


    # Callback from buttons
    def _add(self):
        popup = Popup(self)
    
    def add_uri(self, uri):
        """ Gets called from the popup window """
        self.main_gui.add_uri(uri)

    def _del(self):
        try:
            uris = self.uribox.curselection()
            self.main_gui.del_uris(self.uribox.get(uris[0], uris[-1]))
            self.uribox.delete(uris[0], uris[-1])
        except:
            pass

    def _clear(self):
        self.uribox.delete(0, 'end')
        self.main_gui.clear_uris()

    def _start(self):
        if not self.main_gui.uris:
            self.main_gui.warning_msg('You need to add a URI first')

        if self.test.get() == 'Propeller Test':
            self.main_gui.run_test('propeller')
        else:
            self.main_gui.run_test('hover')
            


class Popup:
    """ Popup for adding a URI """

    def __init__(self, master):

        self.popup = tk.Toplevel()
        self.popup.title('Add URI')
        self.popup.bind('<Return>', self.add_uri)
        self.master = master
        off_y = int( (master.winfo_screenheight() - 120) / 6 )
        off_x = int( (master.winfo_screenwidth() - 250) / 2 )
        self.popup.geometry('250x120+{}+{}'.format(off_x, off_y))

        self.uri = tk.Entry(self.popup, font='Coself.urier 12', width=28, bd=2, relief='ridge',
                            highlightthickness=0)
        self.uri.pack(pady=20)
        self.uri.insert(0, 'radio://0/10/2M/E7E7E7E7E7')
        self.uri.focus_set()

        self.add_btn = TopButton(self.popup, 'ADD', command=self.add_uri, font='Courier 20', width=6)
        self.add_btn.pack(pady=10)

    def add_uri(self, event=None):
        self.master.add_uri(self.uri.get())
        self.popup.destroy()
        del self

    
class TopButton(tk.Button):
    """ Styled and configured Button 'mould' """

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
