import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Application
app = customtkinter.CTk()
app.title("Base Converter")
app.geometry("300x325")
app.grid_columnconfigure(0, weight=1)


class EntryType():
    def __init__(self, app : customtkinter.CTk, label : str, row : int) -> None:
            
        self.frame = customtkinter.CTkFrame(master=app)
        # frame.config(ipadx=10, ipady=10)
        self.frame.grid(row=row, column=0, sticky="we", padx=10, pady=10) # frame.pack(fill="x")
        self.frame.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(master=self.frame, height=20, text=label, text_font=("Roboto Medium", -20))
        self.label.grid(row=0, column=0, pady=(10,5), sticky="we")

        self.entry = customtkinter.CTkEntry(master=self.frame, height=24, text_font=("Roboto", -16), justify=tkinter.CENTER)
        self.entry.grid(row=2, column=0, padx=10, pady=(0,10), sticky="we")

        self.value = tkinter.StringVar(master=self.entry)

        self.entry.configure(textvariable=self.value)

decimal = EntryType(app, "DECIMAL", 0)
hexbox = EntryType(app, "HEX", 1)
binary = EntryType(app, "BINARY", 2)
binary.bitwidth = customtkinter.CTkEntry(master=binary.frame, height=20, text_font=("Roboto", -12), justify=tkinter.CENTER, placeholder_text="8")
binary.bitwidth.grid(row=1, column=0, padx=10, pady=(0,10), sticky="we")
binary.bw_value = tkinter.StringVar(master=binary.bitwidth)
binary.bitwidth.configure(textvariable=binary.bw_value)
binary.bitwidth.insert(0,"8")

def handleKeyPress(event):

    txt = binary.bw_value.get()
    try:
        binary_width = int(txt)
        binary.bitwidth.configure(text_color="black")
    except ValueError:
        binary.bitwidth.configure(text_color="red")
        if app.focus_get() == binary.bitwidth.entry:
            return
        else:
            binary.bitwidth.delete(0, tkinter.END)
            binary.bitwidth.insert(0,"8")
            binary.bitwidth.configure(text_color="black")

    if app.focus_get() == decimal.entry.entry:

        txt = decimal.value.get()
        try:
            i = int(txt)
            decimal.entry.configure(text_color="black")
        except ValueError:
            decimal.entry.configure(text_color="red")
            return

        hexbox.entry.delete(0, tkinter.END)
        hexbox.entry.insert(0,str(hex(i)))

        

        binary.entry.delete(0, tkinter.END)
        binary.entry.insert(0,f"{i % (1<<10):b}")
    


app.bind("<KeyRelease>", handleKeyPress)

app.mainloop()