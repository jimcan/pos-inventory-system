from tkinter import *
from tkinter.ttk import *
import re

list = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket', 'brackets',
        'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event', 'events', 'example', 'field',
        'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind',
        'leave', 'left', 'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 'part',
        'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless',
        'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you', 'super glyphosate']


class AutocompleteEntry(Entry):
    def __init__(self, list, master=None, **kwargs):
        Entry.__init__(self, master=master, **kwargs)
        self.list = list
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Tab>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb = Listbox(font='arial 18 bold', height=6, background='grey')

        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if self.var.get() not in words:
                    if not self.lb_up:
                        self.lb = Listbox(font='arial 18 bold', height=6, background='grey')
                        self.lb.bind("<Double-Button-1>", self.selection)
                        self.lb.bind("<Right>", self.selection)
                        self.lb.place(x=self.winfo_rootx(), y=self.winfo_rooty() - self.winfo_height())
                        self.lb_up = True

                    self.lb.delete(0, END)
                    for w in words:
                        self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
        self.focus_set()

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.list if re.match(pattern, w)]


if __name__ == '__main__':
    root = Tk()

    entry = AutocompleteEntry(list, master=root)
    entry.grid(row=0, column=0)
    Button(text='nothing').grid(row=1, column=0)
    Button(text='nothing').grid(row=2, column=0)
    Button(text='nothing').grid(row=3, column=0)

    root.mainloop()
