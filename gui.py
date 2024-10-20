"""
This file is the main GUI program for the Ivona.WEEB.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from threading import Thread
from time import sleep
import dicts
from scripts import voice_request
from scripts import audio_manipulation


class IvonaGui(tk.Tk):
    """This class is responsible for the GUI part of the Ivona.WEEB."""
    def __init__(self):
        super().__init__()
        audio_manipulation.mixer.init()
        self.frames = [tk.PhotoImage(file="images/bezi_talk.gif", format=f"gif -index {i}") for i in range(2)]
        self.neko_label = ttk.Label(self, image=self.frames[0])
        self.current_lang = 1
        self.wm_iconphoto(True, tk.PhotoImage(file="images/icon.png"))
        self.gui_create()
        self.replace_dict = dicts.Dictionary()
        self.not_playing = True

    def _replace_text_with_dict(self, text: str) -> str:
        """
        This method replaces the text from the main text box
        with the text from the dictionary.
        """
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
        """
        This method opens the text file and writes the content
        of it to the text box.
        """
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read().strip()
        return ""
    
    def lock_btn(self):
        """
        This method locks the play button.
        """
        self.play_button["state"] = "disabled"
    
    def unlock_btn(self):
        """
        This method unlocks the play button.
        """
        self.play_button["state"] = "normal"

    def gui_create(self):
        """This method creates and sets up the GUI."""
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

        self.play_button = ttk.Button(button_frame, text="Play", width=10)
        self.play_button.pack(fill=tk.X, pady=5)
        stop_button = ttk.Button(button_frame, text="Stop")
        stop_button.pack(fill=tk.X, pady=5)
        save_button = ttk.Button(button_frame, text="Save file...")
        save_button.pack(fill=tk.X, pady=5)
        dict_button = ttk.Button(button_frame, text="Dictionary...",
                                 command=lambda: self.replace_dict.show_dict(self.current_lang))
        dict_button.pack(fill=tk.X, pady=5)

        pitch = tk.DoubleVar()
        pitch_slider = tk.Scale(upper_frame, variable=pitch, orient=tk.HORIZONTAL,
                                from_=-30.0, to=30.0, label="Pitch:", length=200)
        pitch_slider.pack(fill=tk.X, pady=5)

        current_voice = tk.StringVar()
        voice_label = ttk.Label(upper_frame, text="Current voice:", anchor=tk.W)
        voice_label.pack(fill=tk.X)
        voice_combobox = ttk.Combobox(upper_frame, textvariable=current_voice, values=list(dicts.NAME_DICT),
                                      width=30, state="readonly")
        voice_combobox.current(0)
        voice_combobox.pack(fill=tk.X)

        self.progress_bar = ttk.Progressbar(upper_frame)

        # Changes program language
        def _set_language(lang_index: int):
            """Function that changes the language of the GUI."""
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
            self.play_button.config(text=lang_list[8][lang_index])
            stop_button.config(text=lang_list[9][lang_index])
            save_button.config(text=lang_list[10][lang_index])
            dict_button.config(text=lang_list[11][lang_index])
            pitch_slider.config(label=lang_list[12][lang_index])
            voice_label.config(text=lang_list[13][lang_index])

        def play_audio():
            """Function that plays the audio in another thread."""
            if current_voice.get().strip() != "" and inp_text.get("1.0", tk.END).strip() != "":
                self.lock_btn()

                if hasattr(self, "progress_bar") and self.progress_bar.winfo_exists():
                    self.progress_bar.pack_forget()

                self.progress_bar['value'] = 0
                self.progress_bar.pack(fill=tk.X, pady=20)
                play_thread = Thread(target=voice_request.get_voice_request,
                                     args=(dicts.NAME_DICT[current_voice.get()],
                                           self._replace_text_with_dict(
                                               inp_text.get("1.0", tk.END)),
                                           pitch.get(), False, self.progress_bar))
                # Check if nothing is playing
                if self.not_playing:
                    self.not_playing = False
                    play_thread.start()

                    # Animates the mascot label image when audio is being played
                    def _animate_mascot(ind) -> None:
                        """
                        Function that animates the mascot image when
                        the audio is being played.
                        """
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
                        self.not_playing = True
                        self.unlock_btn()
                        print("All done\n")

                    Thread(target=_animate_mascot, args=(0,)).start()

        def stop_audio():
            """Function that stops the audio"""
            self.unlock_btn()
            self.not_playing = True
            audio_manipulation.stop_audio()

        def save_audio():
            """Function that saves the audio in another thread."""
            if current_voice.get().strip() != "" and inp_text.get("1.0", tk.END).strip() != "":
                save_thread = Thread(target=voice_request.get_voice_request,
                                     args=(dicts.NAME_DICT[current_voice.get()],
                                           self._replace_text_with_dict(inp_text.get("1.0", tk.END)),
                                           pitch.get(), True))
                save_thread.start()

        def show_about():
            """Function that shows the About window."""
            about_root = tk.Toplevel()
            about_root.wm_iconphoto(True, tk.PhotoImage(file="images/icon.png"))
            about_root.title(dicts.LANG_LIST[2][self.current_lang])
            about_root.resizable(width=False, height=False)
            about_root.geometry("250x60")
            about_text = ttk.Label(about_root, text="Ivona.WEEB © 2024 by Feliksz", anchor=tk.CENTER)
            about_text.pack(fill=tk.X)
            about_ok_button = ttk.Button(about_root, text="OK", command=about_root.destroy, width=10)
            about_ok_button.pack(pady=5, side=tk.BOTTOM)
            about_root.mainloop()

        def read_from_file():
            """Function that inserts the text from file to text box."""
            file_string = self._open_file()
            if file_string:
                inp_text.insert(tk.END, file_string)

        def quick_play():
            inp_text.delete(inp_text.index("end-1c"))
            play_audio()

        self.bind_all("<Control-o>", lambda event: read_from_file())
        self.bind_all("<Control-O>", lambda event: read_from_file())
        self.bind_all("<Control-s>", lambda event: save_audio())
        self.bind_all("<Control-S>", lambda event: save_audio())
        self.bind_all("<Shift-Return>", lambda event: quick_play())

        self.play_button.config(command=play_audio)
        save_button.config(command=save_audio)
        stop_button.config(command=stop_audio)
        file_menu.entryconfig(0, command=read_from_file)
        file_menu.entryconfig(1, command=save_audio)
        file_menu.entryconfig(3, command=show_about)
        lang_menu.entryconfig(0, command=lambda: _set_language(1))
        lang_menu.entryconfig(1, command=lambda: _set_language(0))
        lang_menu.invoke(0)

    def run(self):
        """Method that runs the GUI."""
        self.title("Ivona.WEEB")
        self.resizable(False, False)
        self.mainloop()
