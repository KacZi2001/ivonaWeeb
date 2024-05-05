"""
This file is responsible for holding all the constant
dictionaries and the Dictionary class.
"""
import json
import os
import tkinter as tk
from tkinter import ttk

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
    ["Save", "Zapisz"],
    ["Delete", "Usuń"]
]


class Dictionary:
    """
    This class is responsible for getting the dictionary from
    the json file and also writing the dictionary to that file.
    """
    def __init__(self):
        self.dict = self.parse_json()

    def get_dict(self) -> dict[str, str]:
        """This method returns the dictionary from the class."""
        return self.dict

    def parse_json(self) -> dict[str, str]:
        """This method parses the json file and returns the dictionary."""
        dic: dict[str, str] = {}
        if os.path.isfile("dictionary.json"):
            print("Parsing dictionary...")
            with open("dictionary.json", encoding="utf-8") as file:
                dic = json.load(file)
        return dic

    def save_json(self) -> None:
        """This method saves the dictionary to the json file."""
        if len(self.dict) > 0:
            print("Saving dictionary...")
            with open("dictionary.json", "w", encoding="utf-8") as file:
                json.dump(self.dict, file, indent=4, ensure_ascii=False)

    # New window that shows all dictionary elements
    def show_dict(self, lang: int) -> None:
        """This method shows the dictionary in the GUI."""
        root = tk.Toplevel()
        root.wm_iconphoto(True, tk.PhotoImage(file="images/icon.png"))
        root.resizable(False, False)
        root.title(LANG_LIST[14][lang])

        main_panel = ttk.Frame(root)
        main_panel.pack(side=tk.TOP, fill=tk.BOTH)
        bottom_panel = ttk.Frame(root)
        bottom_panel.pack(side=tk.BOTTOM, fill=tk.BOTH)

        def focus_next(event) -> str:
            """Function that allows moving between widgets"""
            event.widget.tk_focusNext().focus()
            return "break"

        def add_new_element(key: str, value: str) -> None:
            """Function that creates new Text objects"""
            current_row: int = main_panel.grid_size()[1]

            from_text = tk.Text(main_panel, width=25, height=1, wrap=tk.WORD)
            from_text.grid(row=current_row, column=0, padx=3, pady=3)

            to_text = tk.Text(main_panel, width=25, height=1, wrap=tk.WORD)
            to_text.grid(row=current_row, column=1, padx=3, pady=3)

            from_text.insert(tk.END, key)
            to_text.insert(tk.END, value)
            from_text.bind("<Tab>", focus_next)
            to_text.bind("<Tab>", focus_next)

            rem_button = ttk.Button(main_panel, width=15, text=LANG_LIST[20][lang])
            rem_button.grid(row=current_row, column=2, padx=3, pady=3)

            def remove_element() -> None:
                """Function that removes dictionary entries."""
                from_text.grid_remove()
                to_text.grid_remove()
                rem_button.grid_remove()

            rem_button.config(command=remove_element)

        # Add new Text objects for all dictionary elements
        for test_key in self.dict.keys():
            add_new_element(test_key, self.dict[test_key])

        def save_all_elements() -> None:
            """
            Function that clears the dictionary and adds
            all elements from the text boxes to it.
            """
            self.dict.clear()
            for key, value in zip(reversed(main_panel.grid_slaves(column=0)),
                                  reversed(main_panel.grid_slaves(column=1))):
                key: tk.Text = key
                value: tk.Text = value
                key_str: str = key.get("1.0", tk.END).strip()
                value_str: str = value.get("1.0", tk.END).strip()
                if key_str != "":
                    self.dict.update({key_str: value_str})

        def save_and_exit() -> None:
            """
            Function that calls the save all elements function
            and saves all changes to json file.
            """
            save_all_elements()
            self.save_json()
            root.destroy()

        cancel_button = ttk.Button(bottom_panel, text=LANG_LIST[16][lang], command=root.destroy)
        cancel_button.grid(row=0, column=0, padx=5, pady=5)
        add_button = ttk.Button(bottom_panel, text=LANG_LIST[18][lang], command=lambda: add_new_element("", ""))
        add_button.grid(row=0, column=1, padx=5, pady=5)
        save_button = ttk.Button(bottom_panel, text=LANG_LIST[19][lang], command=save_and_exit)
        save_button.grid(row=0, column=2, padx=5, pady=5)
        root.mainloop()
