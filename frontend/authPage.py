import customtkinter
from backend import authenticate

class AuthPage(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x300+750+400")
        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.didExit = False
        self.user = None
        self.password = None
        self.key = None
        #frames
        self.frame_entry = customtkinter.CTkFrame(self)
        self.frame_entry.place(in_=self, x=150, y=100, anchor='center')

        self.frame_button = customtkinter.CTkFrame(self)
        self.frame_button.place(in_=self, x=150, y=250, anchor='center')
        #buttons
        self.button_login = customtkinter.CTkButton(self.frame_button, text='Login', command=self.login, width=110, height=24)
        self.button_login.pack(padx=10,pady=10)
        self.bind('<Return>', self.login)
        self.button_create_acc = customtkinter.CTkButton(self.frame_button, text='Create new account', command=self.createAccount, width=110, height=24)
        self.button_create_acc.pack(padx=10,pady=10)
        #entries
        self.entry_login = customtkinter.CTkEntry(self.frame_entry, placeholder_text='Login', width=160, height=28)
        self.entry_login.pack(padx=10, pady=10)

        self.entry_password = customtkinter.CTkEntry(self.frame_entry, placeholder_text='Password', width=160, height=28)
        self.entry_password.pack(padx=10, pady=10)

        self.entry_key = customtkinter.CTkEntry(self.frame_entry, placeholder_text='Input your key', width=160, height=28)
        self.entry_key.pack(padx=10, pady=10)
        #login
        self.loggedIn = False
        self.incorrect_label = customtkinter.CTkLabel(self.frame_entry, text='Incorrect login or password')
        self.user_exists_label = customtkinter.CTkLabel(self.frame_entry, text='User already exists')
        self.wait_window() #IMPORTANT this is hashtagged for when you want autologin
    def login(self, event=None):
        self.user = self.entry_login.get() #IMPORTANT this is hashtagged for when you want autologin
        self.password = self.entry_password.get() #IMPORTANT this is hashtagged for when you want autologin
        self.key = self.entry_key.get() #IMPORTANT this is hashtagged for when you want autologin
        if self.user == "" or self.password == "":
            return None
        if authenticate.login(self.user, self.password):
            self.loggedIn = True

            self.destroy()
        else:
            self.entry_password.delete(0, "end")
            self.entry_login.delete(0, "end")
            self.entry_key.delete(0, "end")
            self.loggedIn = False
            self.incorrect_label.pack(padx=5, pady=5)
    def createAccount(self):
        self.user = self.entry_login.get()
        self.password = self.entry_password.get()
        self.key = self.entry_key.get()
        if self.user == "" or self.password == "":
            return None
        self.loggedIn = authenticate.createAccount(self.user, self.password)
        if self.loggedIn:
            self.destroy()
        else:
            self.incorrect_label.pack_forget()
            self.user_exists_label.pack(padx=5, pady=5)
    def onClosing(self):
        self.destroy()
        self.didExit = True
        exit()


