import tkinter as tk
from tkinter import messagebox
from scripts import run_scripts

LIGHT_HEAL_ACTIVE = None
STRONG_HEAL_ACTIVE = None
LIGHT_MANA_UP_ACTIVE = None
STRONG_MANA_UP_ACTIVE = None
EXURA_SIO_ACTIVE = None

LOW_HP_HOTKEY = None
LOW_HP_LEVEL = -1
CRITICAL_HP_HOTKEY = None
CRITICAL_HP_LEVEL = -1

LOW_MANA_HOTKEY = None
LOW_MANA_LEVEL = -1
CRITICAL_MANA_HOTKEY = None
CRITICAL_MANA_LEVEL = -1

FIRST_TO_SIO = None
EXURA_SIO_HOTKEY = None
SIO_TARGET = None


def setup_config_gui(window):
    def confirm_func():
        global LIGHT_HEAL_ACTIVE
        global STRONG_HEAL_ACTIVE
        global LIGHT_MANA_UP_ACTIVE
        global STRONG_MANA_UP_ACTIVE
        global EXURA_SIO_ACTIVE

        global LOW_HP_HOTKEY
        global LOW_HP_LEVEL
        global CRITICAL_HP_HOTKEY
        global CRITICAL_HP_LEVEL

        global LOW_MANA_HOTKEY
        global LOW_MANA_LEVEL
        global CRITICAL_MANA_HOTKEY
        global CRITICAL_MANA_LEVEL

        global FIRST_TO_SIO
        global EXURA_SIO_HOTKEY
        global SIO_TARGET

        any_error = False

        LIGHT_HEAL_ACTIVE = light_heal_active.get()
        STRONG_HEAL_ACTIVE = strong_heal_active.get()
        LIGHT_MANA_UP_ACTIVE = light_mana_up_active.get()
        STRONG_MANA_UP_ACTIVE = strong_mana_up_active.get()
        EXURA_SIO_ACTIVE = exura_sio_active.get()

        if LIGHT_HEAL_ACTIVE:
            LOW_HP_HOTKEY = light_heal_hotkey_entry.get().upper()
            try:
                LOW_HP_LEVEL = int(light_heal_threshold_entry.get())
            except ValueError:
                messagebox.showerror(title="Error", message="Only numbers accepted as hp values.")
                any_error = True

        if STRONG_HEAL_ACTIVE:
            CRITICAL_HP_HOTKEY = strong_heal_hotkey_entry.get().upper()
            try:
                CRITICAL_HP_LEVEL = int(strong_heal_threshold_entry.get())
            except ValueError:
                messagebox.showerror(title="Error", message="Only numbers accepted as hp values.")
                any_error = True

        if LIGHT_MANA_UP_ACTIVE:
            LOW_MANA_HOTKEY = light_mana_hotkey_entry.get().upper()
            try:
                LOW_MANA_LEVEL = int(light_mana_threshold_entry.get())
            except ValueError:
                messagebox.showerror(title="Error", message="Only numbers accepted as mana values.")
                any_error = True

        if STRONG_MANA_UP_ACTIVE:
            CRITICAL_MANA_HOTKEY = strong_mana_hotkey_entry.get().upper()
            try:
                CRITICAL_MANA_LEVEL = int(strong_mana_threshold_entry.get())
            except ValueError:
                messagebox.showerror(title="Error", message="Only numbers accepted as mana values.")
                any_error = True

        if EXURA_SIO_ACTIVE:
            FIRST_TO_SIO = exura_sio_target_entry.get()
            EXURA_SIO_HOTKEY = exura_sio_hotkey_entry.get().upper()
            SIO_TARGET = FIRST_TO_SIO[:12].replace(" ", "")

        if STRONG_HEAL_ACTIVE and not LIGHT_HEAL_ACTIVE or LOW_HP_LEVEL < CRITICAL_HP_LEVEL:
            messagebox.showerror(title="Error", message="Critical healing is being used before the light healing.")
            any_error = True
        elif STRONG_MANA_UP_ACTIVE and not LIGHT_MANA_UP_ACTIVE or LOW_MANA_LEVEL < CRITICAL_MANA_LEVEL:
            messagebox.showerror(title="Error", message="Critical mana up is being used before the regular mana up.")
            any_error = True

        if not any_error:

            if LIGHT_HEAL_ACTIVE:
                if STRONG_HEAL_ACTIVE:
                    heal_msg = f"• If you life goes bellow: {LOW_HP_LEVEL}, you heal with {LOW_HP_HOTKEY}.\n" \
                               f"And if goes bellows: {CRITICAL_HP_LEVEL}, you heal with {CRITICAL_HP_HOTKEY}"
                else:
                    heal_msg = f"• If you life goes bellow: {LOW_HP_LEVEL}, you heal with {LOW_HP_HOTKEY}."
            else:
                heal_msg = "• You are not healing yourself automatically."

            if LIGHT_MANA_UP_ACTIVE:
                if STRONG_MANA_UP_ACTIVE:
                    mana_msg = f"• If you mana goes bellow: {LOW_MANA_LEVEL}, you mana up with {LOW_MANA_HOTKEY}.\n" \
                               f"And if goes bellows: {CRITICAL_MANA_LEVEL}, you mana up with {CRITICAL_MANA_HOTKEY}"
                else:
                    mana_msg = f"• If you mana up goes bellow: {LOW_MANA_LEVEL}, you mana up with {LOW_MANA_HOTKEY}."
            else:
                mana_msg = "• You are not refilling your mana automatically."

            if EXURA_SIO_ACTIVE:
                sio_msg = f"• If {FIRST_TO_SIO} goes to yellow, you heal him/she with {EXURA_SIO_HOTKEY}"
            else:
                sio_msg = f"• You are not healing anybody."

            message = f"{heal_msg}\n\n{mana_msg}\n\n{sio_msg}"

            confirm = messagebox.askyesno(title="Confirm configurations", message=message)

            if confirm:
                window.wm_state('iconic')
                run_scripts()

    window.geometry("400x800")

    light_heal_label = tk.Label(text="LIGHT HEAL").grid(column=1, row=0)
    light_heal_hotkey_label = tk.Label(text="HOTKEY").grid(column=0, row=1)
    light_heal_hotkey_entry = tk.Entry()
    light_heal_hotkey_entry.grid(column=1, row=1)
    light_heal_threshold_label = tk.Label(text="THRESHOLD").grid(column=0, row=2)
    light_heal_threshold_entry = tk.Entry()
    light_heal_threshold_entry.grid(column=1, row=2)
    light_heal_active = tk.BooleanVar()
    tk.Checkbutton(text="Active", variable=light_heal_active).grid(column=2, row=0)

    empty_space = tk.Label(text="").grid(column=0, row=3)

    strong_heal_label = tk.Label(text="STRONG HEAL").grid(column=1, row=4)
    strong_heal_hotkey_label = tk.Label(text="HOTKEY").grid(column=0, row=5)
    strong_heal_hotkey_entry = tk.Entry()
    strong_heal_hotkey_entry.grid(column=1, row=5)
    strong_heal_threshold_label = tk.Label(text="THRESHOLD").grid(column=0, row=6)
    strong_heal_threshold_entry = tk.Entry()
    strong_heal_threshold_entry.grid(column=1, row=6)
    strong_heal_active = tk.BooleanVar()
    tk.Checkbutton(text="Active", variable=strong_heal_active).grid(column=2, row=4)

    empty_space2 = tk.Label(text="").grid(column=0, row=7)

    light_mana_label = tk.Label(text="LIGHT MANA UP").grid(column=1, row=8)
    light_mana_hotkey_label = tk.Label(text="HOTKEY").grid(column=0, row=9)
    light_mana_hotkey_entry = tk.Entry()
    light_mana_hotkey_entry.grid(column=1, row=9)
    light_mana_threshold_label = tk.Label(text="THRESHOLD").grid(column=0, row=10)
    light_mana_threshold_entry = tk.Entry()
    light_mana_threshold_entry.grid(column=1, row=10)
    light_mana_up_active = tk.BooleanVar()
    tk.Checkbutton(text="Active", variable=light_mana_up_active).grid(column=2, row=8)

    empty_space3 = tk.Label(text="").grid(column=0, row=11)

    strong_mana_label = tk.Label(text="STRONG MANA UP").grid(column=1, row=12)
    strong_mana_hotkey_label = tk.Label(text="HOTKEY").grid(column=0, row=13)
    strong_mana_hotkey_entry = tk.Entry()
    strong_mana_hotkey_entry.grid(column=1, row=13)
    strong_mana_threshold_label = tk.Label(text="THRESHOLD").grid(column=0, row=14)
    strong_mana_threshold_entry = tk.Entry()
    strong_mana_threshold_entry.grid(column=1, row=14)
    strong_mana_up_active = tk.BooleanVar()
    tk.Checkbutton(text="Active", variable=strong_mana_up_active).grid(column=2, row=12)

    empty_space4 = tk.Label(text="").grid(column=0, row=15)

    exura_sio_label = tk.Label(text="EXURA SIO").grid(column=1, row=16)
    exura_sio_target_label = tk.Label(text="TARGET").grid(column=0, row=18)
    exura_sio_target_entry = tk.Entry()
    exura_sio_target_entry.grid(column=1, row=18)
    exura_sio_hotkey_label = tk.Label(text="HOTKEY").grid(column=0, row=17)
    exura_sio_hotkey_entry = tk.Entry()
    exura_sio_hotkey_entry.grid(column=1, row=17)
    exura_sio_active = tk.BooleanVar()
    tk.Checkbutton(text="Active", variable=exura_sio_active).grid(column=2, row=16)

    confirm_button = tk.Button(window, text="Confirm", command=confirm_func)
    confirm_button.grid(column=3, row=19)

    window.mainloop()
