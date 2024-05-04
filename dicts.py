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
    ["Delete line ", "Usuń linię "]
]


class Dictionary:
    def __init__(self):
        self.dict = self._parse_json()

    def _remove_elements(self, pos_label: ttk.Label, from_text: tk.Text, to_text: tk.Text, button: ttk.Button) -> None:
        pos_label.pack_forget()
        from_text.pack_forget()
        to_text.pack_forget()
        button.pack_forget()

    def get_dict(self) -> dict[str, str]:
        return self.dict

    # def _parse_ini(self) -> dict[str, str]:
    #     dic = dict()
    #     print("Parsing dictionary...")
    #     if os.path.isfile("dictionary.ini"):
    #         dict_file = open("dictionary.ini")
    #         lines = dict_file.readlines()
    #
    #         for line in lines:
    #             lst = line.strip().split(" : ")
    #             if len(lst[0]) > 0:
    #                 dic.update({lst[0]: lst[1]})
    #
    #         dict_file.close()
    #     return dic

    def _parse_json(self) -> dict[str, str]:
        dic = dict()
        if os.path.isfile("dictionary.json"):
            print("Parsing dictionary...")
            with open("dictionary.json", encoding="utf-8") as file:
                dic = json.load(file)
        return dic

    # def _save_ini(self) -> None:
    #     print("Saving dictionary...")
    #     dict_file = open("dictionary.ini", "w")
    #
    #     for key in self.dict.keys():
    #         dict_file.write("{} : {}\n".format(key, self.dict[key]))
    #
    #     dict_file.close()

    def _save_json(self) -> None:
        if len(self.dict) > 0:
            print("Saving dictionary...")
            with open("dictionary.json", "w", encoding="utf-8") as file:
                json.dump(self.dict, file, indent=4, ensure_ascii=False)

    # New window that shows all dictionary elements
    def show_dict(self, lang: int) -> None:
        root = tk.Tk()
        root.iconbitmap("images/icon.ico")
        root.title(LANG_LIST[14][lang])

        leftmost_panel = ttk.Frame(root)
        leftmost_panel.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        left_panel = ttk.Frame(root)
        left_panel.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
        right_panel = ttk.Frame(root)
        right_panel.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)
        rightmost_panel = ttk.Frame(root)
        rightmost_panel.grid(row=0, column=3, sticky=tk.NSEW, padx=5, pady=5)
        bottom_panel = ttk.Frame(root)
        bottom_panel.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)

        # Function that allows moving between widgets
        def focus_next(event) -> str:
            if event.widget in left_panel.pack_slaves():
                current_index: int = left_panel.pack_slaves().index(event.widget)
                right_panel.pack_slaves()[current_index].focus()
            else:
                current_index: int = right_panel.pack_slaves().index(event.widget) + 1
                if current_index in range(1, len(left_panel.pack_slaves())):
                    left_panel.pack_slaves()[current_index].focus()
            return "break"

        # Function that creates new Text objects
        def add_new_element(key: str, value: str) -> None:
            pos_label = ttk.Label(leftmost_panel, padding=3)
            pos_label.pack(fill=tk.BOTH)

            from_text = tk.Text(left_panel, width=25, height=1, pady=3)
            from_text.pack(fill=tk.BOTH)

            to_text = tk.Text(right_panel, width=25, height=1, pady=3)
            to_text.pack(fill=tk.BOTH)

            from_text.insert(tk.END, key)
            to_text.insert(tk.END, value)
            from_text.bind("<Tab>", focus_next)
            to_text.bind("<Tab>", focus_next)

            rem_button = ttk.Button(rightmost_panel, width=15,
                                    command=lambda: self._remove_elements(pos_label, from_text, to_text, rem_button))
            rem_button.pack(fill=tk.BOTH)
            current_line: int = rightmost_panel.pack_slaves().index(rem_button)
            rem_button.config(text=LANG_LIST[20][lang] + str(current_line + 1))
            pos_label.config(text=str(current_line + 1) + ".")

        # Adding new Text objects for all dictionary elements
        for test_key in self.dict.keys():
            add_new_element(test_key, self.dict[test_key])

        # Clearing the dictionary and adding all text elements
        def save_all_elements() -> None:
            self.dict.clear()
            for from_text, to_text in zip(left_panel.pack_slaves(), right_panel.pack_slaves()):
                from_text: tk.Text = from_text
                to_text: tk.Text = to_text
                from_text_str = from_text.get("1.0", tk.END).strip()
                to_text_str = to_text.get("1.0", tk.END).strip()
                if from_text_str != "":
                    self.dict.update({from_text_str: to_text_str})

        def save_and_exit() -> None:
            save_all_elements()
            self._save_json()
            root.destroy()

        cancel_button = ttk.Button(bottom_panel, text=LANG_LIST[16][lang], command=root.destroy)
        cancel_button.grid(row=0, column=0, padx=5, pady=5)
        add_button = ttk.Button(bottom_panel, text=LANG_LIST[18][lang], command=lambda: add_new_element("", ""))
        add_button.grid(row=0, column=1, padx=5, pady=5)
        save_button = ttk.Button(bottom_panel, text=LANG_LIST[19][lang], command=save_and_exit)
        save_button.grid(row=0, column=2, padx=5, pady=5)
        root.mainloop()

if __name__ == "__main__":
    Dictionary().show_dict(1)