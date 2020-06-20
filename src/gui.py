import os
import tkinter as tk

import yaml

from src import battlefortune as bf

os.chdir('/Users/pfass/code/BattleFortune')


class BattleFortuneInputs:

    def __init__(self, master):

        frame = tk.Frame(master)
        frame.pack(side=tk.TOP)

        self.dp_label = tk.Label(frame, text='Dominions Path: ')
        self.dp_entry = tk.Entry(frame)

        self.gp_label = tk.Label(frame, text='Saved Games Path: ')
        self.gp_entry = tk.Entry(frame)

        if os.path.exists('data/config.yaml'):
            with open('data/config.yaml', 'r') as file:
                config = yaml.load(stream=file, Loader=yaml.Loader)
                self.dp_entry.insert(0, config['dom_path'])
                self.gp_entry.insert(0, config['game_path'])

        self.gn_label = tk.Label(frame, text='Game Name: ')
        self.gn_entry = tk.Entry(frame)

        self.pn_label = tk.Label(frame, text='Province Number: ')
        self.pn_entry = tk.Entry(frame)

        self.sr_label = tk.Label(frame, text='Rounds: ')
        self.sr_entry = tk.Entry(frame)

        self.dp_label.grid(row=0, column=0, sticky=tk.W)
        self.dp_entry.grid(row=0, column=1)

        self.gp_label.grid(row=1, column=0, sticky=tk.W)
        self.gp_entry.grid(row=1, column=1)

        self.gn_label.grid(row=2, column=0, sticky=tk.W)
        self.gn_entry.grid(row=2, column=1)

        self.pn_label.grid(row=3, column=0, sticky=tk.W)
        self.pn_entry.grid(row=3, column=1)

        self.sr_label.grid(row=4, column=0, sticky=tk.W)
        self.sr_entry.grid(row=4, column=1)

    def get_values(self):

        inputs = {
            'dp': self.dp_entry.get(),
            'gp': self.gp_entry.get(),
            'gn': self.gn_entry.get(),
            'pn': self.pn_entry.get(),
            'sr': self.sr_entry.get(),
        }

        bf.startup(inputs)


def initialize():

    root = tk.Tk()
    print('test')

    title = tk.Label(text='BattleFortune')
    title.pack()

    bf_inputs = BattleFortuneInputs(root)
    button = tk.Button(root, text='Simulate', command=bf_inputs.get_values)

    sep_1 = tk.Frame(height=10)
    sep_1.pack()
    button.pack(fill=tk.X)
    sep_2 = tk.Frame(height=10)
    sep_2.pack()

    root.mainloop()
