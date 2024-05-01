import tkinter as tk
from tkinter import ttk, scrolledtext
import dicts
from scripts import voice_request
from threading import Thread


class IvonaGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.neko_img = tk.PhotoImage(file="neko.png").subsample(3)
        self.gui_create()

    def gui_create(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open...")
        file_menu.add_command(label="Save...")
        file_menu.add_separator()
        file_menu.add_command(label="About")
        file_menu.add_command(label="Exit", command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        lang_menu = tk.Menu(menu_bar, tearoff=0)
        lang_menu.add_radiobutton(label="Polish")
        lang_menu.add_radiobutton(label="English")
        lang_menu.invoke(1)
        menu_bar.add_cascade(label="Language", menu=lang_menu)
        self.config(menu=menu_bar)

        upper_frame = tk.Frame(self)
        upper_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW, columnspan=2)
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=2, padx=10, pady=10, sticky=tk.NSEW)

        neko_label = tk.Label(self, image=self.neko_img)
        neko_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        inp_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, width=40)
        inp_text.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W, columnspan=2)

        play_button = tk.Button(button_frame, text="Play", width=10)
        play_button.pack(fill=tk.X, pady=5)
        stop_button = tk.Button(button_frame, text="Stop")
        stop_button.pack(fill=tk.X, pady=5)
        save_button = tk.Button(button_frame, text="Save File")
        save_button.pack(fill=tk.X, pady=5)
        dict_button = tk.Button(button_frame, text="Dictionary")
        dict_button.pack(fill=tk.X, pady=5)

        pitch = tk.DoubleVar()
        pitch_slider = tk.Scale(upper_frame, variable=pitch, orient=tk.HORIZONTAL, from_=-30.0, to=30.0, label="Pitch:",
                                length=200)
        pitch_slider.pack(fill=tk.X, pady=5)

        current_voice = tk.StringVar()
        voice_label = tk.Label(upper_frame, text="Current Voice:", anchor=tk.W)
        voice_label.pack(fill=tk.X)
        voice_combobox = ttk.Combobox(upper_frame, textvariable=current_voice, values=list(dicts.NAME_DICT),
                                      width=30, state="readonly")
        voice_combobox.current(0)
        voice_combobox.pack(fill=tk.X)

        # voice_request.get_voice_request(current_voice.get(), inp_text.get("1.0", tk.END),
        #                                 pitch.get(), False)

        def play_audio():
            play_thread = Thread(target=voice_request.get_voice_request,
                                 args=(dicts.NAME_DICT[current_voice.get()], inp_text.get("1.0", tk.END),
                                       pitch.get(), False))
            play_thread.start()

        def save_audio():
            save_thread = Thread(target=voice_request.get_voice_request,
                                 args=(dicts.NAME_DICT[current_voice.get()], inp_text.get("1.0", tk.END),
                                       pitch.get(), True))
            save_thread.start()

        # play_thread = Thread(target=voice_request.get_voice_request,
        #                      args=(current_voice.get(), inp_text.get("1.0", tk.END), pitch.get(), False))

        play_button.config(command=play_audio)
        save_button.config(command=save_audio)

    def run(self):
        self.title("Ivona.WEEB")
        self.resizable(False, False)
        self.mainloop()
