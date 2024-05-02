import tkinter as tk

NAME_DICT: dict[str, str] = {
    "Jacek": "ivona",
    "Jacek (Demo)": "ivonademo",
    "Jacek (2.0)": "jacek",
    "Jan": "jan",
    "Krzysztof": "krzysztof",
    "Bogdan": "bogdan",
    "Ewa (Demo)": "ewa",
    "Ewa (2.0)": "ewa2",
    "Maja": "maja",
    "Agnieszka": "agnieszka",
    "Zosia": "zosia"
}

LANG_LIST: list[list[str]] = [
    ["Open...", "Otwórz..."],
    ["Save...", "Zapisz..."],
    ["About", "O programie"],
    ["Exit", "Wyjście"],
    ["File", "Plik"],
    ["Polish", "Polski"],
    ["English", "Angielski"],
    ["Language", "Język"],
    ["Play", "Odtwórz"],
    ["Stop", "Zatrzymaj"],
    ["Save file...", "Zapisz plik..."],
    ["Dictionary...", "Słownik..."],
    ["Pitch:", "Wysokość głosu:"],
    ["Current voice:", "Wybrany głos:"],
    ["Dictionary", "Słownik"],
    ["Add new element", "Dodaj nowy element"],
    ["Cancel", "Anuluj"],
    ["Add", "Dodaj"],
    ["Add new...", "Dodaj nowy..."],
    ["Save", "Zapisz"]
]


class Dictionary:
    def __init__(self):
        self.dict = self._parse_ini()

    def get_dict(self) -> dict[str, str]:
        return self.dict

    def _parse_ini(self) -> dict[str, str]:
        dic = dict()
        print("Parsing dictionary...")
        dict_file = open("dictionary.ini")
        lines = dict_file.readlines()

        for line in lines:
            lst = line.strip().split(" : ")
            if len(lst[0]) > 0:
                dic.update({lst[0]: lst[1]})

        dict_file.close()
        print("Dictionary parsed")
        return dic

    def _save_ini(self) -> None:
        print("Saving dictionary...")
        dict_file = open("dictionary.ini", "w")

        for key in self.dict.keys():
            dict_file.write("{} : {}\n".format(key, self.dict[key]))

        dict_file.close()
        print("Dictionary saved")

    # New window that shows all dictionary elements
    def show_dict(self, lang: int) -> None:
        root = tk.Tk()
        root.title(LANG_LIST[14][lang])

        left_panel = tk.Frame(root)
        left_panel.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        right_panel = tk.Frame(root)
        right_panel.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
        bottom_panel = tk.Frame(root)
        bottom_panel.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

        # Function that creates new Text objects
        def add_new_element(key, value) -> None:
            from_text = tk.Text(left_panel, width=25, height=1)
            from_text.insert(tk.END, key)
            from_text.config(state=tk.DISABLED)
            from_text.pack(fill=tk.X)

            to_text = tk.Text(right_panel, width=25, height=1)
            to_text.insert(tk.END, value)
            to_text.config(state=tk.DISABLED)
            to_text.pack(fill=tk.X)

        # Adding new Text objects for all dictionary elements
        for test_key in self.dict.keys():
            add_new_element(test_key, self.dict[test_key])

        # New window that allows adding new elements
        def add_dict_element() -> None:
            dict_root = tk.Tk()
            dict_root.title(LANG_LIST[15][lang])
            dict_from_text = tk.Text(dict_root, width=25, height=1)
            dict_from_text.grid(row=0, column=0, padx=5, pady=5)
            dict_to_text = tk.Text(dict_root, width=25, height=1)
            dict_to_text.grid(row=0, column=1, padx=5, pady=5)

            def add_to_dict() -> None:
                key: str = dict_from_text.get("1.0", tk.END).strip()
                value: str = dict_to_text.get("1.0", tk.END).strip()
                if key != "" and value != "":
                    self.dict.update({key: value})
                    add_new_element(key, value)
                    print("Element added")
                dict_root.destroy()

            dict_cancel_button = tk.Button(dict_root, text=LANG_LIST[16][lang], command=dict_root.destroy)
            dict_cancel_button.grid(row=1, column=0, padx=5, pady=5)
            dict_add_button = tk.Button(dict_root, text=LANG_LIST[17][lang], command=add_to_dict)
            dict_add_button.grid(row=1, column=1, padx=5, pady=5)
            dict_root.mainloop()

        def save_and_exit() -> None:
            self._save_ini()
            root.destroy()

        cancel_button = tk.Button(bottom_panel, text=LANG_LIST[16][lang], command=root.destroy)
        cancel_button.grid(row=0, column=0, padx=5, pady=5)
        add_button = tk.Button(bottom_panel, text=LANG_LIST[18][lang], command=add_dict_element)
        add_button.grid(row=0, column=1, padx=5, pady=5)
        save_button = tk.Button(bottom_panel, text=LANG_LIST[19][lang], command=save_and_exit)
        save_button.grid(row=0, column=2, padx=5, pady=5)
        root.mainloop()
