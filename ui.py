from tkinter import *
from tkcalendar import Calendar
import datetime as dt
from data import Billify
import webbrowser


THEME_COLOR = "#3d8361"
BUTT0N_COLOR = "#fde8cd"
BACKGROUND = "#025955"


def done_command(level, enable):
    level.destroy()
    enable.config(state="normal")


class InterFace:

    def __init__(self, func: Billify):
        self.window = Tk()
        self.window.eval('tk::PlaceWindow . center')
        self.window.title("Billify")
        self.window.config(padx=25, pady=20, bg=THEME_COLOR)
        self.date = ""
        self.billify_ = func
        self.n = 0

        # First Statement Label
        self.first_statement = Label(
            text="What year and week do you want to travel to?",
            font=("Ariel", 15, "bold"),
            bg=THEME_COLOR,
            fg="white",
            width=50,
        )
        self.first_statement.grid(row=0, column=0)

        # Select week Button
        self.select_button = Button(
            text="SELECT",
            bg=BUTT0N_COLOR,
            width=20,
            highlightthickness=5,
            borderwidth=2,
            cursor="hand2",
            command=self.select_date_window,
        )
        self.select_button.grid(row=2, column=0, pady=20)

        self.window.mainloop()

    def select_date_window(self):
        today = dt.datetime.now()
        cal = Calendar(
                       font="Arial 14",
                       selectmode='day',
                       cursor="hand2",
                       year=today.year,
                       month=today.month,
                       day=today.day,
                       background=BACKGROUND,
                       bordercolor=BACKGROUND,

                       )
        cal.grid(row=1, column=0, pady=20)

        def ok_():
            popup = Toplevel()
            popup.title("Billify - loading")
            self.window.eval(f'tk::PlaceWindow {str(popup)} center')
            popup.config(bg=THEME_COLOR, padx=25, pady=25)
            # gif = PhotoImage(file="loading.gif", format="gif -index 2")
            label = Label(
                popup,
                # image=gif,
                text="Loading...",
                font=("Ariel", 15, "bold"),
                bg=THEME_COLOR,
                width=40,
                fg="white",
            )
            label.grid(row=0, column=0)

            popup.after(100, self.start, cal, popup, ok_button)

            popup.mainloop()

        ok_button = Button(
            text="OK",
            bg=BUTT0N_COLOR,
            width=20,
            highlightthickness=5,
            borderwidth=2,
            cursor="hand2",
            command=ok_,
        )
        ok_button.grid(row=2, column=0, pady=20)

    def create_label(self, level, text, n_):
        label_ = Label(
            level,
            text=text,
            font=("Ariel", n_, "bold"),
            bg=THEME_COLOR,
            width=40,
            fg="white",
        )
        label_.bind('<Configure>',
                    lambda e: label_.config(wraplength=label_.winfo_width()))
        label_.grid(row=self.n, column=0)
        self.n += 1

    def create_link(self, level, text):

        def get_link(url):
            webbrowser.open_new(url)

        link = Label(
            level,
            text=f"Link:{text}",
            font=("Ariel", 13, "bold"),
            bg=THEME_COLOR,
            width=40,
            fg="blue",
            cursor="hand2"
        )
        link.bind('<Configure>',
                  lambda e: link.config(wraplength=link.winfo_width()))
        link.bind("<Button-1>", lambda e: get_link(text))
        link.grid(row=self.n, column=0)
        self.n += 1

    def start(self, cal, root, btn):
        btn.config(state="disabled")
        self.date = f"{cal.selection_get()}"

        link = self.billify_.start_to_finish(self.date)

        c = self.billify_.a
        if len(c) > 0:
            for item in c:
                self.create_label(root, item, 8)

        self.create_label(root, "All Done", 11)
        self.create_link(root, link)
        root.title("Billify - Done")
        self.done(root, btn)

    def done(self, level, enable):
        done_button = Button(
            level,
            text="DONE",
            bg=BUTT0N_COLOR,
            width=15,
            highlightthickness=5,
            borderwidth=2,
            cursor="hand2",
            command=lambda: done_command(level, enable)
        )
        done_button.grid(row=self.n, column=0, pady=20)
