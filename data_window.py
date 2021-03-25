from tkinter import Tk, RAISED
from tkinter.ttk import (
    Frame,
    Notebook,
    Style,
)


class DataWindow(Frame):
    def __init__(self, tabs, **kwargs):
        super().__init__(**kwargs)
        self.configure(style='Main.TFrame', padding=(50, 0, 50, 0))
        self.style = Style()
        self.style.configure('TNotebook.Tab', font='arial 20 italic')
        self.style.configure('TButton', font='arial 22 bold',
                             foreground='blue', width=9, relief=RAISED, borderwidth=5)
        self.style.configure('TLabel', font='arial 18 bold',
                             foreground='blue', padding=5)
        self.style.configure('Main.TFrame', background='cadet blue')
        self.style.configure('Treeview', font='arial 12 normal')
        self.tabs = tabs
        self.build()

    def build(self):
        self.pack()

        # Add Data Tab
        self.tabs.add(self, text='Database')

        # Data Tab Title
        self.title(data_tab, self.data_title)

    def data_win(self):

        # <editor-fold desc="Data Tab Functions">
        def add_new():
            data_keys = self.sort_data_dict()
            i, u, p, s = entry_item.get(), entry_unit.get(), entry_price.get(), entry_stock.get()
            if len(i) != 0 and len(u) != 0 and len(p) != 0 and len(s) != 0:
                key = f'{i}|{u}'
                if key not in data_keys:
                    try:
                        backend.add_record((i, u, float(p), float(s)))
                        self.update_data_list()
                    except ValueError:
                        messagebox.showwarning(
                            'Warning', '"Price" and "Stock" should contain numbers not words')
                else:
                    messagebox.showwarning(
                        'Warning', 'This item is already in database')
                search()
            else:
                messagebox.showwarning('Warning', "You can't add nothing")

        def display_data():
            data_keys = self.sort_data_dict()

            data = []
            for k in data_keys:
                i, u = k.split('|')
                p, s = self.data_dict[k][0], self.data_dict[k][1]
                d = [i, u, p, s]
                data.append(d)

            self.clear_tv(tv_data)
            self.display(tv_data, data)

        def clear_entries():
            entry_item.delete(0, END)
            entry_unit.delete(0, END)
            entry_price.delete(0, END)
            entry_stock.delete(0, END)
            entry_item.focus_set()

        def delete_data():
            i, u = entry_item.get(), entry_unit.get()
            if len(i) != 0 and len(u) != 0:
                k = backend.search_data(i, u)
                k = k[0][0]
                backend.delete_record(k)
                self.update_data_list()
                clear_entries()
                display_data()
            else:
                messagebox.showwarning(
                    'Warning', '"Item" and "Unit" should not be empty')

        def search():
            i, u = entry_item.get(), entry_unit.get()

            if len(i) != 0 or len(u) != 0:
                searched_data = backend.search_data(i, u)

                data = []
                for row in searched_data:
                    d = [row[1], row[2], row[3], row[4]]
                    data.append(d)

                self.clear_tv(tv_data)
                self.display(tv_data, data)

        def update():
            global k
            if isinstance(k, int):
                i, u, p, s = entry_item.get(), entry_unit.get(), entry_price.get(), entry_stock.get()
                backend.update_data(k, i, u, p, s)
                self.update_data_list()
                search()
            else:
                messagebox.showwarning('Warning', 'Select an item to update')

        def event_search(event):
            search()

        def tv_select(event):
            global k
            f = tv_data.focus()
            i = tv_data.item(f)
            x = i['values']
            k = backend.search_data(x[0], x[1])
            k = k[0][0]
            entry_item.delete(0, END)
            entry_item.insert(END, x[0])
            entry_unit.delete(0, END)
            entry_unit.insert(END, x[1])
            entry_price.delete(0, END)
            entry_price.insert(END, x[2])
            entry_stock.delete(0, END)
            entry_stock.insert(END, x[3])

        def event_item(event):
            entry_unit.focus_set()

        def event_unit(event):
            entry_price.focus_set()

        def event_price(event):
            entry_stock.focus_set()

        def event_stock(event):
            add_new()
        # </editor-fold>

        # <editor-fold desc="Data Frame">
        data_tab = Frame(self.tabs, style='Main.TFrame',
                         padding=(50, 0, 50, 0))
        data_tab.pack()

        # Add Data Tab
        self.tabs.add(data_tab, text='Database')

        # Data Tab Title
        self.title(data_tab, self.data_title)

        # <editor-fold desc="Data Mid Frame">
        d_mid_frame = Frame(data_tab, relief=SUNKEN,
                            borderwidth=5, padding=(30, 10, 30, 10))
        d_mid_frame.pack(fill=X)

        # <editor-fold desc="Data Mid Top Frame">
        d_mid_top = Frame(d_mid_frame)
        d_mid_top.pack(side=TOP, fill=X)

        # <editor-fold desc="Data Mid Top Right Frame">
        d_mid_top_right = Frame(d_mid_top, padding=(15, 65))
        d_mid_top_right.pack(side=RIGHT, fill=Y)

        # <editor-fold desc="Data Right Labels">
        lbl_item = Label(d_mid_top_right, text='Item', padding=(10, 20))
        lbl_unit = Label(d_mid_top_right, text='Unit', padding=(10, 20))
        lbl_price = Label(d_mid_top_right, text='Price', padding=(10, 20))
        lbl_stock = Label(d_mid_top_right, text='Stock', padding=(10, 20))

        lbl_item.grid(row=0, column=0, sticky=E)
        lbl_unit.grid(row=1, column=0, sticky=E)
        lbl_price.grid(row=2, column=0, sticky=E)
        lbl_stock.grid(row=3, column=0, sticky=E)
        # </editor-fold>

        # <editor-fold desc="Data Right Entries">
        entry_item = AutocompleteEntry(
            self.data_list, master=d_mid_top_right, font='arial 18 bold', foreground='green')
        entry_unit = Entry(
            d_mid_top_right, font='arial 18 bold', foreground='green')
        entry_price = Entry(
            d_mid_top_right, font='arial 18 bold', foreground='green')
        entry_stock = Entry(
            d_mid_top_right, font='arial 18 bold', foreground='green')

        entry_item.grid(row=0, column=1)
        entry_unit.grid(row=1, column=1)
        entry_price.grid(row=2, column=1)
        entry_stock.grid(row=3, column=1)

        entry_item.bind('<Tab>', event_search, True)
        entry_item.bind('<Right>', event_search, True)
        entry_item.bind('<Return>', event_search, True)
        entry_item.bind('<Return>', event_item, True)
        entry_unit.bind('<Return>', event_unit)
        entry_price.bind('<Return>', event_price)
        entry_stock.bind('<Return>', event_stock)
        # </editor-fold>
        # </editor-fold>

        # <editor-fold desc="Data Mid Top Left Frame">
        d_mid_top_left = Frame(d_mid_top, padding=(0, 0, 0, 10))
        d_mid_top_left.pack(side=LEFT, fill=Y)

        # <editor-fold desc="Data Treeview">
        cols = {
            '#0': ['No', 70, 'w'],
            'item': ['Item', 270, 'w'],
            'unit': ['Unit', 100, 'center'],
            'price': ['Price', 150, 'e'],
            'stock': ['Stock', 150, 'e'],
        }
        tv_data = self.treeviews(d_mid_top_left, cols, 20)
        tv_data.bind('<<TreeviewSelect>>', tv_select)
        # </editor-fold>
        # </editor-fold>
        # </editor-fold>

        # <editor-fold desc="Data Buttons">
        btn_texts = ['Add New', 'Display', 'Clear',
                     'Delete', 'Search', 'Update', 'Exit']
        buttons = self.buttons(d_mid_frame, btn_texts)
        buttons[0]['command'] = add_new
        buttons[1]['command'] = display_data
        buttons[2]['command'] = clear_entries
        buttons[3]['command'] = delete_data
        buttons[4]['command'] = search
        buttons[5]['command'] = update
        # </editor-fold>
        # </editor-fold>

        # <editor-fold desc="Data Footer">
        self.footer(data_tab)
        # </editor-fold>
        # </editor-fold>


if __name__ == '__main__':
    root = Tk()
    tabs = Notebook(root, width=(root.winfo_screenwidth() - 40)).pack()
    data_win = DataWindow(master=tabs, tabs=tabs).pack()
    root.mainloop()
