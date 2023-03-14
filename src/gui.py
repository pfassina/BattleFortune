import os
import tkinter as tk
from tkinter import filedialog

import yaml
from PIL import Image, ImageTk

from src import battlefortune as bf
from src import config
from src.config import SimConfig


class ImageViewer(tk.LabelFrame):
    def __init__(self, master) -> None:
        super().__init__(master, text="Results", padx=10, pady=10)
        super().rowconfigure(0, weight=1)

        self.current_image_index: int = 0
        self.images: list[ImageTk.PhotoImage] = []

        # widgets
        self.image_label: tk.Label = tk.Label(self)
        self.image_label.configure(text="You can't cheat fate")
        self.prev_button: tk.Button = tk.Button(
            self, text="<<", command=self.show_previous_image
        )
        self.next_button: tk.Button = tk.Button(
            self, text=">>", command=self.show_next_image
        )
        self.image_counter: tk.Label = tk.Label(self, text="0/0")

        # layout
        self.image_label.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)

    def load_images(self, image_files):
        self.images = [ImageTk.PhotoImage(Image.open(file)) for file in image_files]
        self.show_image()

    def show_image(self) -> None:
        image = self.images[self.current_image_index]
        self.image_label.configure(image=image)
        self.image_label.image = image  # type: ignore

        current_image = self.current_image_index + 1
        total_images = len(self.images)
        self.image_counter.configure(text=f"{current_image}/{total_images}")

        self.prev_button.grid(row=1, column=0, sticky=tk.W)
        self.next_button.grid(row=1, column=2, sticky=tk.E)
        self.image_counter.grid(row=1, column=1, sticky=tk.EW)

    def show_next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_image()

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()


class Form(tk.LabelFrame):
    def __init__(self, master, image_viewer):
        super().__init__(master, text="BattleFortune", padx=10, pady=10)
        super().columnconfigure(1, weight=1)

        # widgets

        self.image_viewer: ImageViewer = image_viewer

        self.dp_label = tk.Label(self, text="Dominions Path: ")
        self.dp_entry = tk.Entry(self)  # , width=60)
        self.dp_button = tk.Button(self, text="select", command=self.get_dir)

        self.gp_label = tk.Label(self, text="Saved Games Path: ")
        self.gp_entry = tk.Entry(self)  # , width=60)
        self.gp_button = tk.Button(self, text="select", command=self.get_dir)

        self.gn_label = tk.Label(self, text="Game Name: ")
        self.gn_entry = tk.Entry(self)  # , width=25)

        self.pn_label = tk.Label(self, text="Province: ")
        self.pn_entry = tk.Entry(self)  # , width=10)

        self.sr_label = tk.Label(self, text="Rounds: ")
        self.sr_entry = tk.Entry(self)  # , width=10)

        self.dx_entry = tk.Entry(self)
        self.dy_entry = tk.Entry(self)

        self.simulate_button = tk.Button(self, text="Simulate", command=self.simulate)

        ## layout
        self.dp_label.grid(row=0, column=0, sticky=tk.W)
        self.dp_entry.grid(row=0, column=1, sticky=tk.EW, columnspan=5)
        self.dp_button.grid(row=0, column=6, sticky=tk.EW)

        self.gp_label.grid(row=1, column=0, sticky=tk.W)
        self.gp_entry.grid(row=1, column=1, sticky=tk.EW, columnspan=5)
        self.gp_button.grid(row=1, column=6, sticky=tk.EW)

        self.gn_label.grid(row=2, column=0, sticky=tk.W)
        self.gn_entry.grid(row=2, column=1, sticky=tk.EW)

        self.pn_label.grid(row=2, column=2, sticky=tk.EW)
        self.pn_entry.grid(row=2, column=3, sticky=tk.EW)

        self.sr_label.grid(row=2, column=4, sticky=tk.EW)
        self.sr_entry.grid(row=2, column=5, sticky=tk.EW, columnspan=2)

        self.simulate_button.grid(
            row=5, column=0, columnspan=7, sticky=tk.NSEW, pady=10
        )

        self.get_config()

    def get_dir(self) -> str:
        return filedialog.askdirectory()

    def get_config(self) -> None:
        config_path = os.path.join("data", "config.yaml")
        with open(config_path, "r") as file:
            sim_config = yaml.load(stream=file, Loader=yaml.Loader)

        if not isinstance(sim_config, SimConfig):
            set_text(self.dx_entry, str(sim_config["banner_x"]))
            set_text(self.dy_entry, str(sim_config["banner_y"]))
            return

        set_text(self.dp_entry, sim_config.dominions_path)
        set_text(self.gp_entry, sim_config.game_dir)
        set_text(self.gn_entry, sim_config.game_name)
        set_text(self.pn_entry, str(sim_config.province))
        set_text(self.sr_entry, str(sim_config.simulations))
        set_text(self.dx_entry, str(sim_config.banner_x))
        set_text(self.dy_entry, str(sim_config.banner_y))

    def simulate(self) -> None:
        sim_config = SimConfig(
            self.dp_entry.get(),
            self.gp_entry.get(),
            self.gn_entry.get(),
            int(self.pn_entry.get()),
            int(self.sr_entry.get()),
            int(self.dx_entry.get()),
            int(self.dy_entry.get()),
        )

        config_path = os.path.join("data", "config.yaml")
        with open(config_path, "w") as file:
            yaml.dump(sim_config, file)

        bf.start(sim_config)

        image_files = [
            os.path.join("img", img)
            for img in os.listdir("img")
            if img.endswith(".png")
        ]
        self.image_viewer.load_images(image_files)
        self.image_viewer.show_image()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        super().columnconfigure(0, weight=0)
        super().rowconfigure(1, weight=0)

        self.title("BattleFortune")
        self.image_viewer = ImageViewer(self)
        self.form = Form(self, self.image_viewer)

        self.form.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.image_viewer.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)


def set_text(entry: tk.Entry, text: str) -> None:
    entry.delete(0, tk.END)
    entry.insert(0, text)


def start() -> None:
    config.generate_config_file()
    app = Application()
    app.mainloop()
