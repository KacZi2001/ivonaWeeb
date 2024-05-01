import tkinter as tk


class IvonaGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gui_create()

    def gui_create(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

        neko_img = tk.PhotoImage(file="neko.png")
        small_neko = neko_img.subsample(4, 4)
        neko_label = tk.Label(self, image=small_neko)
        neko_label.grid(row=0, column=0, columnspan=2)
        # inp_text = tk.Text(self, height=10, width=50)
        # inp_text.grid(row=0, column=0)

    def run(self):
        self.title("IvonaWeeb")
        self.resizable(False, False)
        self.geometry("500x500")
        self.mainloop()


def main():
    IvonaGui().run()


if __name__ == '__main__':
    main()
