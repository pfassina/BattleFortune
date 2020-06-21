import os
from PIL import ImageTk, Image

import tkinter as tk
from tkinter import filedialog

import yaml

from src import battlefortune as bf


img_index = 0
img_len = 0


def get_config():

    config = {'dom_path': '', 'game_path': ''}
    if os.path.exists('data/config.yaml'):
        with open('data/config.yaml', 'r') as file:
            config = yaml.load(stream=file, Loader=yaml.Loader)
    return config


def get_dir(path_input):
    path = filedialog.askdirectory(title='Please select a directory')
    path_input.delete(0, 'end')
    path_input.insert(0, string=path)


def show_img(frame):

    global img_index
    global img_len

    img1 = ImageTk.PhotoImage(Image.open('img/winscore.png'))
    img2 = ImageTk.PhotoImage(Image.open('img/army_roi.png'))
    img3 = ImageTk.PhotoImage(Image.open('img/defender_roi.png'))
    img4 = ImageTk.PhotoImage(Image.open('img/defender_unit_deaths.png'))

    image_list = [img1, img2, img3, img4]
    img_len = len(image_list)

    result_label = tk.Label(frame, image=image_list[img_index])
    result_label.image = image_list[img_index]
    result_label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)


def get_values(variables, frame):

    dp, gp, gn, pn, sr = variables

    inputs = {
        'dp': dp.get(),
        'gp': gp.get(),
        'gn': gn.get(),
        'pn': pn.get(),
        'sr': sr.get(),
    }

    bf.startup(inputs)
    show_img(frame)

    button_back = tk.Button(frame, text='<<', command=lambda: last_img(frame))
    button_next = tk.Button(frame, text='>>', command=lambda: next_img(frame))

    button_back.grid(row=1, column=0, sticky=tk.W)
    button_next.grid(row=1, column=1, sticky=tk.E)


def next_img(frame):

    global img_index
    global img_len

    if img_index + 1 > img_len - 1:
        img_index = 0
    else:
        img_index += 1

    show_img(frame)


def last_img(frame):

    global img_index
    global img_len

    if img_index - 1 < 0:
        img_index = img_len - 1
    else:
        img_index -= 1

    show_img(frame)


def initialize():

    root = tk.Tk()
    root.title('BattleFortune')

    inputs_frame = tk.LabelFrame(master=root, text='BattleFortune', padx=10, pady=10)
    inputs_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

    config = get_config()

    dp_label = tk.Label(inputs_frame, text='Dominions Path: ')
    dp_entry = tk.Entry(inputs_frame, width=60)
    dp_entry.insert(0, config.get('dom_path'))
    dp_button = tk.Button(inputs_frame, text='select', command=lambda: get_dir(dp_entry))

    gp_label = tk.Label(inputs_frame, text='Saved Games Path: ')
    gp_entry = tk.Entry(inputs_frame, width=60)
    gp_entry.insert(0, config.get('game_path'))
    gp_button = tk.Button(inputs_frame, text='select', command=lambda: get_dir(gp_entry))

    gn_label = tk.Label(inputs_frame, text='Game Name: ')
    gn_entry = tk.Entry(inputs_frame, width=25)

    pn_label = tk.Label(inputs_frame, text='Province: ')
    pn_entry = tk.Entry(inputs_frame, width=10)

    sr_label = tk.Label(inputs_frame, text='Rounds: ')
    sr_entry = tk.Entry(inputs_frame, width=10)

    dp_label.grid(row=0, column=0, sticky=tk.E)
    dp_entry.grid(row=0, column=1, sticky=tk.W, columnspan=5)
    dp_button.grid(row=0, column=6, sticky=tk.E)

    gp_label.grid(row=1, column=0, sticky=tk.E)
    gp_entry.grid(row=1, column=1, sticky=tk.W, columnspan=5)
    gp_button.grid(row=1, column=6, sticky=tk.E)

    gn_label.grid(row=2, column=0, sticky=tk.E)
    gn_entry.grid(row=2, column=1, sticky=tk.W)

    pn_label.grid(row=2, column=2, sticky=tk.E)
    pn_entry.grid(row=2, column=3, sticky=tk.W)

    sr_label.grid(row=2, column=4, sticky=tk.E)
    sr_entry.grid(row=2, column=5, sticky=tk.E, columnspan=2)

    results_frame = tk.LabelFrame(master=root, text='Results', padx=10, pady=10)
    results_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

    result_label = tk.Label(results_frame, text="You can't cheat fate.")
    result_label.grid(row=0, column=0)

    input_variables = (dp_entry, gp_entry, gn_entry, pn_entry, sr_entry)

    button = tk.Button(inputs_frame, text='Simulate', command=lambda: get_values(input_variables, results_frame))
    button.grid(row=5, column=0, columnspan=7, sticky=tk.NSEW, pady=10)

    root.mainloop()
