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


class Dictionary:
    def __init__(self):
        self.test_dict = self._parse_ini()

    def _parse_ini(self):
        dic = dict()
        dict_file = open("dictionary.ini")
        lines = dict_file.readlines()

        for line in lines:
            lst = line.strip().split(" : ")
            if len(lst[0]) > 0:
                dic.update({lst[0]: lst[1]})

        dict_file.close()
        return dic

    def _save_ini(self):
        dict_file = open("dictionary.ini", "w")
        print(self.test_dict)

        for key in self.test_dict.keys():
            dict_file.write("{} : {}\n".format(key, self.test_dict[key]))

        dict_file.close()

    # New window that shows all dictionary elements
    def show_dict(self):
        root = tk.Tk()
        root.title("Dictionary")

        left_panel = tk.Frame(root)
        left_panel.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        right_panel = tk.Frame(root)
        right_panel.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
        bottom_panel = tk.Frame(root)
        bottom_panel.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

        # Function that creates new Text objects
        def add_new_element(key, value):
            from_text = tk.Text(left_panel, width=25, height=1)
            from_text.insert(tk.END, key)
            from_text.config(state=tk.DISABLED)
            from_text.pack(fill=tk.X)

            to_text = tk.Text(right_panel, width=25, height=1)
            to_text.insert(tk.END, value)
            to_text.config(state=tk.DISABLED)
            to_text.pack(fill=tk.X)

        # Adding new Text objects for all dictionary elements
        for test_key in self.test_dict.keys():
            add_new_element(test_key, self.test_dict[test_key])

        # New window that allows adding new elements
        def add_dict_element():
            dict_root = tk.Tk()
            dict_root.title("Add new element")
            dict_from_text = tk.Text(dict_root, width=25, height=1)
            dict_from_text.grid(row=0, column=0, padx=5, pady=5)
            dict_to_text = tk.Text(dict_root, width=25, height=1)
            dict_to_text.grid(row=0, column=1, padx=5, pady=5)

            def add_to_dict():
                key = dict_from_text.get("1.0", tk.END).strip()
                value = dict_to_text.get("1.0", tk.END).strip()
                if key != "" and value != "":
                    self.test_dict.update({key: value})
                    add_new_element(key, value)
                dict_root.destroy()

            dict_cancel_button = tk.Button(dict_root, text="Cancel", command=dict_root.destroy)
            dict_cancel_button.grid(row=1, column=0, padx=5, pady=5)
            dict_add_button = tk.Button(dict_root, text="Add", command=add_to_dict)
            dict_add_button.grid(row=1, column=1, padx=5, pady=5)
            dict_root.mainloop()

        def save_and_exit():
            self._save_ini()
            root.destroy()

        cancel_button = tk.Button(bottom_panel, text="Cancel", command=root.destroy)
        cancel_button.grid(row=0, column=0, padx=5, pady=5)
        add_button = tk.Button(bottom_panel, text="Add new...", command=add_dict_element)
        add_button.grid(row=0, column=1, padx=5, pady=5)
        save_button = tk.Button(bottom_panel, text="Save", command=save_and_exit)
        save_button.grid(row=0, column=2, padx=5, pady=5)
        root.mainloop()


if __name__ == '__main__':
    Dictionary().show_dict()
