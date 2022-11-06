import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Application
app = customtkinter.CTk()
app.title("Base Converter")
app.geometry("300x500")
app.grid_columnconfigure(0, weight=1)

auto_compute = customtkinter.StringVar(value=0)

def switch_event():
    print("switch toggled, current value:", auto_compute.get())

switch_1 = customtkinter.CTkSwitch(master=app, text="Auto Compute", command=switch_event,
                                   variable=auto_compute, onvalue=1, offvalue=0)
switch_1.grid(row=0, column=0, pady=(15,0))
switch_1.grid_columnconfigure(1, weight=1)

class EntryType():
    def __init__(self, app : customtkinter.CTk, label : str, row : int) -> None:
            
        self.frame = customtkinter.CTkFrame(master=app)
        self.frame.grid(row=row, column=0, sticky="we", padx=10, pady=10) # frame.pack(fill="x")
        self.frame.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(master=self.frame, height=20, text=label, text_font=("Roboto Medium", -20))
        self.label.grid(row=0, column=0, pady=(10,5), sticky="we")

        self.entry = customtkinter.CTkEntry(master=self.frame, height=36, text_font=("Roboto", -16), justify=tkinter.CENTER)
        self.entry.grid(row=5, column=0, padx=10, pady=(0,10), sticky="we")

        self.value = tkinter.StringVar(master=self.entry)

        self.entry.configure(textvariable=self.value)

decimal = EntryType(app, "DECIMAL", 5)
hexbox = EntryType(app, "HEX", 10)
binary = EntryType(app, "BINARY", 15)

option_frame = customtkinter.CTkFrame(master=binary.frame)
option_frame.grid(row=2, column=0, sticky="we", padx=10, pady=10) # frame.pack(fill="x")
option_frame.grid_columnconfigure(0, weight=1)
option_frame.grid_columnconfigure(1, weight=1)
option_frame.grid_columnconfigure(2, weight=1)

# Bit width option
bitwidth_label = customtkinter.CTkLabel(master= option_frame, text="bit width", text_font=("Roboto Medium", -14))
bitwidth_label.grid(row=0, column=0)
bitwidth_label.grid_rowconfigure(1, weight=1)

bitwidth = customtkinter.CTkEntry(master=option_frame, height=26, width=36, text_font=("Roboto Medium", -16), justify=tkinter.CENTER, placeholder_text="8")
bitwidth.grid(row=1, column=0, pady=(0,10))
bitwidth.grid_rowconfigure(1, weight=1)
bw_value = tkinter.StringVar(master=bitwidth)
bitwidth.configure(textvariable=bw_value)
bitwidth.insert(0,"8")

# Sign option
sign_select_label = customtkinter.CTkLabel(master= option_frame, text="signed", text_font=("Roboto Medium", -14))
sign_select_label.grid(row=0, column=1)
sign_select_label.grid_rowconfigure(1, weight=1)

bit_sign = False

check_var = tkinter.StringVar()

def sign_checkbox_event():
    global bit_sign
    bit_sign = bool(int(check_var.get()))

checkbox = customtkinter.CTkCheckBox(master=option_frame, text="", command=sign_checkbox_event,
                                     variable=check_var, onvalue=1, offvalue=0)
checkbox.grid(row=1, column=1, pady=(0,10))
checkbox.grid_rowconfigure(1, weight=1)


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

val_d = 0
prev_val_d = val_d

def handleKeyPress(event):
    global val_d, prev_val_d

    txt = bw_value.get()
    try:
        binary_width = int(txt)
        bitwidth.configure(text_color="black")
    except ValueError:
        bitwidth.configure(text_color="red")

        # if the user is modifying the binary bit width, just ignore
        if app.focus_get() == bitwidth.entry:
            return

        # if the user leaves an invalid bit width and moves on, default to 8
        else:
            bitwidth.delete(0, tkinter.END)
            bitwidth.insert(0,"8")
            bitwidth.configure(text_color="black")
            binary_width = 8

    if app.focus_get() == decimal.entry.entry:

        txt = decimal.value.get()
        try:
            val_d = int(txt)
            decimal.entry.configure(text_color="black")
        except ValueError:
            decimal.entry.configure(text_color="red")
            return

    elif app.focus_get() == hexbox.entry.entry:
        txt = hexbox.value.get()
        try:
            val_d = int(int(txt, base=16))
            hexbox.entry.configure(text_color="black")
        except ValueError:
            hexbox.entry.configure(text_color="red")
            return

    elif app.focus_get() == binary.entry.entry:
        txt = binary.value.get()
        try:
            if bit_sign:
                print("signed")
                val_d = twos_comp(int(txt, base=2), len(txt))
            else:
                val_d = int(txt, base=2)
            binary.entry.configure(text_color="black")
        except ValueError:
            binary.entry.configure(text_color="red")
            return

    if val_d == prev_val_d:
        return

    if not bool(int(auto_compute.get())):
        return

    # Number valid, print to output
    decimal.entry.configure(text_color="black")
    hexbox.entry.configure(text_color="black")
    binary.entry.configure(text_color="black")

    decimal.entry.delete(0, tkinter.END)
    decimal.entry.insert(0,str(val_d))

    hex_print = str(hex(val_d))
    binary_print = f"{val_d % (1<<binary_width):b}".zfill(binary_width)

    hexbox.entry.delete(0, tkinter.END)
    hexbox.entry.insert(0,hex_print)

    binary.entry.delete(0, tkinter.END)
    binary.entry.insert(0,binary_print)

    prev_val_d = val_d


app.bind("<KeyRelease>", handleKeyPress)

app.mainloop()