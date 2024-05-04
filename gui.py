import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import dicts
from scripts import voice_request
from scripts import audio_manipulation
from threading import Thread
from time import sleep


class IvonaGui(tk.Tk):
    def __init__(self):
        super().__init__()
        audio_manipulation.mixer.init()
        self.frames = [tk.PhotoImage(file="images/bezi_talk.gif", format="gif -index %i" % i) for i in range(2)]
        self.neko_label = ttk.Label(self, image=self.frames[0])
        self.current_lang = 1
        self.iconbitmap("images/icon.ico")
        self.gui_create()
        self.replace_dict = dicts.Dictionary()

    def _replace_text_with_dict(self, text: str) -> str:
        temp_text: str = text.lower()
        if len(self.replace_dict.get_dict()) != 0:
            line_not_printed: bool = True
            for key, value in self.replace_dict.get_dict().items():
                if key.lower() in temp_text:
                    if line_not_printed:
                        print("Replacing lines with dictionary...")
                        line_not_printed = False
                    temp_text = temp_text.replace(key.lower(), value.lower())
        return temp_text

    def _open_file(self) -> str:
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read().strip()

    def gui_create(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open...", underline=0, accelerator="Ctrl+O")
        file_menu.add_command(label="Save...", underline=0, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="About", underline=3)
        file_menu.add_command(label="Exit", underline=0, command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu, underline=0)

        lang_menu = tk.Menu(menu_bar, tearoff=0)
        lang_menu.add_radiobutton(label="Polish", underline=0)
        lang_menu.add_radiobutton(label="English", underline=0)
        menu_bar.add_cascade(label="Language", menu=lang_menu, underline=0)
        self.config(menu=menu_bar)

        upper_frame = ttk.Frame(self)
        upper_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW, columnspan=2)
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=2, padx=10, pady=10, sticky=tk.NSEW)

        self.neko_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        inp_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, width=40)
        inp_text.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W, columnspan=2)

        play_button = ttk.Button(button_frame, text="Play", width=10)
        play_button.pack(fill=tk.X, pady=5)
        stop_button = ttk.Button(button_frame, text="Stop")
        stop_button.pack(fill=tk.X, pady=5)
        save_button = ttk.Button(button_frame, text="Save file...")
        save_button.pack(fill=tk.X, pady=5)
        dict_button = ttk.Button(button_frame, text="Dictionary...",
                                 command=lambda: self.replace_dict.show_dict(self.current_lang))
        dict_button.pack(fill=tk.X, pady=5)

        pitch = tk.DoubleVar()
        pitch_slider = tk.Scale(upper_frame, variable=pitch, orient=tk.HORIZONTAL, from_=-30.0, to=30.0, label="Pitch:",
                                length=200)
        pitch_slider.pack(fill=tk.X, pady=5)

        current_voice = tk.StringVar()
        voice_label = ttk.Label(upper_frame, text="Current voice:", anchor=tk.W)
        voice_label.pack(fill=tk.X)
        voice_combobox = ttk.Combobox(upper_frame, textvariable=current_voice, values=list(dicts.NAME_DICT),
                                      width=30, state="readonly")
        voice_combobox.current(0)
        voice_combobox.pack(fill=tk.X)

        # Changes program language
        def _set_language(lang_index: int):
            self.current_lang = lang_index
            lang_list = dicts.LANG_LIST
            file_menu.entryconfig(lang_index, label="penis")
            file_menu.entryconfig(0, label=lang_list[0][lang_index])
            file_menu.entryconfig(1, label=lang_list[1][lang_index])
            file_menu.entryconfig(3, label=lang_list[2][lang_index])
            file_menu.entryconfig(4, label=lang_list[3][lang_index])
            menu_bar.entryconfig(1, label=lang_list[4][lang_index])
            lang_menu.entryconfig(0, label=lang_list[5][lang_index])
            lang_menu.entryconfig(1, label=lang_list[6][lang_index])
            menu_bar.entryconfig(2, label=lang_list[7][lang_index])
            play_button.config(text=lang_list[8][lang_index])
            stop_button.config(text=lang_list[9][lang_index])
            save_button.config(text=lang_list[10][lang_index])
            dict_button.config(text=lang_list[11][lang_index])
            pitch_slider.config(label=lang_list[12][lang_index])
            voice_label.config(text=lang_list[13][lang_index])

        def play_audio():
            if current_voice.get().strip() != "" and inp_text.get("1.0", tk.END).strip() != "":
                play_thread = Thread(target=voice_request.get_voice_request,
                                     args=(dicts.NAME_DICT[current_voice.get()],
                                           self._replace_text_with_dict(inp_text.get("1.0", tk.END)),
                                           pitch.get(), False))
                # Check if nothing is playing
                if not play_thread.is_alive() and not audio_manipulation.mixer.get_busy():
                    play_thread.start()

                    # Animates the mascot label image when audio is being played
                    def _animate_mascot(ind) -> None:
                        while not audio_manipulation.mixer.get_busy():
                            sleep(0.1)
                        while audio_manipulation.mixer.get_busy():
                            frame = self.frames[ind]
                            ind += 1
                            if ind == 2:
                                ind = 0
                            self.neko_label.config(image=frame)
                            sleep(0.15)
                        self.neko_label.config(image=self.frames[0])
                        print("All done\n")

                    Thread(target=_animate_mascot, args=(0,)).start()

        def save_audio():
            if current_voice.get().strip() != "" and inp_text.get("1.0", tk.END).strip() != "":
                save_thread = Thread(target=voice_request.get_voice_request,
                                     args=(dicts.NAME_DICT[current_voice.get()],
                                           self._replace_text_with_dict(inp_text.get("1.0", tk.END)),
                                           pitch.get(), True))
                save_thread.start()

        # Creates about window and shows it
        def show_about():
            about_root = tk.Tk()
            about_root.iconbitmap("images/icon.ico")
            about_root.title(dicts.LANG_LIST[2][self.current_lang])
            about_root.resizable(width=False, height=False)
            about_root.geometry("250x60")
            about_text = ttk.Label(about_root, text="Ivona.WEEB © 2024 by Feliksz", anchor=tk.CENTER)
            about_text.pack(fill=tk.X)
            about_ok_button = ttk.Button(about_root, text="OK", command=about_root.destroy, width=10)
            about_ok_button.pack(pady=5, side=tk.BOTTOM)
            about_root.mainloop()

        def read_from_file():
            file_string = self._open_file()
            if file_string:
                inp_text.insert(tk.END, file_string)

        self.bind_all("<Control-o>", lambda event: read_from_file())
        self.bind_all("<Control-O>", lambda event: read_from_file())
        self.bind_all("<Control-s>", lambda event: save_audio())
        self.bind_all("<Control-S>", lambda event: save_audio())

        play_button.config(command=play_audio)
        save_button.config(command=save_audio)
        stop_button.config(command=audio_manipulation.stop_audio)
        file_menu.entryconfig(0, command=read_from_file)
        file_menu.entryconfig(1, command=save_audio)
        file_menu.entryconfig(3, command=show_about)
        lang_menu.entryconfig(0, command=lambda: _set_language(1))
        lang_menu.entryconfig(1, command=lambda: _set_language(0))
        lang_menu.invoke(0)

    def run(self):
        self.title("Ivona.WEEB")
        self.resizable(False, False)
        self.mainloop()
