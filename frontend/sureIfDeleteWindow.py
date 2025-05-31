import customtkinter
class SureIfDeleteWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x100+750+400")
        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.didAgree = False
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack()
        self.label_sure_If_Delete_Window = customtkinter.CTkLabel(self.frame, text="Are you sure you want to delete this password?")
        self.label_sure_If_Delete_Window.pack(padx=5, pady=5)
        self.button_yes = customtkinter.CTkButton(self, text="Yes", width=50, height=30, command=self.yes)
        self.button_yes.place(anchor="nw", y=50, x=90)
        self.button_no = customtkinter.CTkButton(self, text="No", width=50, height=30, command=self.onClosing)
        self.button_no.place(anchor="nw", y=50, x=160)
        self.transient(master)
        self.grab_set()
        self.wait_window()
    def onClosing(self):
        self.destroy()
    def yes(self):
        self.didAgree = True
        self.onClosing()