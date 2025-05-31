import hashlib

import customtkinter, utils
from backend import fileManager, decryption, encryption
from authPage import AuthPage
from sureIfDeleteWindow import SureIfDeleteWindow
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.resizable(False, False)
        self.geometry("1000x700+430+200")
        self.login_page = AuthPage(self)
        self.login_page.update()
        #IMPORTANT this is not hashtagged when you want autologin
        #from here
        #self.login_page.user = 'test'
        #self.login_page.password = 'test'
        #self.login_page.key = 'test'
        #self.login_page.login()
        #up to here
        self.decrypted = None
        if self.login_page.didExit:
            exit()
        # appearance
        self.frame_appearance = customtkinter.CTkFrame(self, width=220, height=120)
        self.frame_appearance.place(anchor='sw', x=10, y=690)
        self.modes = ["Dark", "Light"]
        self.option_mode = customtkinter.CTkOptionMenu(self.frame_appearance, values=self.modes, command=self.optionMode)
        self.option_mode.pack(padx=8, pady=8)
        #services
        self.frame_services = customtkinter.CTkScrollableFrame(self, width=200, height=500)
        self.frame_services.place(anchor='nw', x=10, y=10)
        self.buttons_passwords = {}
        self.listServices()
        #decrypted
        self.frame_decrypt = customtkinter.CTkFrame(self, width=300, height=250)
        self.frame_decrypt.place(anchor="center", x=450, y=250, relwidth=0.33, relheight=0.33)
        self.label_service = None
        self.label_password = None
        self.pass_to_clipboard = None
        self.label_login = None
        self.login_to_clipboard = None
        self.button_delete = None
        #save new password
        self.frame_encrypt = customtkinter.CTkFrame(self, width=300, height=250)
        self.frame_encrypt.place(anchor="nw", x=690, y = 10)
        self.entry_name_of_service = customtkinter.CTkEntry(self.frame_encrypt, placeholder_text='Name of service', width=210, height=28)
        self.entry_name_of_service.pack(padx=30, pady=10)
        self.entry_login = customtkinter.CTkEntry(self.frame_encrypt, placeholder_text='Login', width=210, height=28)
        self.entry_login.pack(padx=30, pady=10)
        self.entry_password = customtkinter.CTkEntry(self.frame_encrypt, placeholder_text='Password', width=210, height=28)
        self.entry_password.pack(padx=30, pady=10)
        self.button_save_new_password = customtkinter.CTkButton(self.frame_encrypt, text="Save new password", command=self.encrypt)
        self.button_save_new_password.pack(padx=30, pady=10)


    def listServices(self):
        passwords = fileManager.readFile(f'{utils.getPath()}appstorage\\passwords.json')
        for service in passwords[self.login_page.user].keys():
            self.buttons_passwords.update({service:customtkinter.CTkButton(self.frame_services, text=f'Show: {service}', command=lambda x=service: self.decrypt(x))})
            self.buttons_passwords[service].pack(pady=5)
    def unlistServices(self):
        passwords_old = fileManager.readFile(f'{utils.getPath()}appstorage\\passwords.json')
        for service in passwords_old[self.login_page.user].keys():
            self.buttons_passwords[service].pack_forget()
    def optionMode(self, choice):
        customtkinter.set_appearance_mode(choice)
    def encrypt(self):
        hash1 = hashlib.new('SHA256')
        hash1.update(self.login_page.key.encode())
        key = hash1.digest()
        self.unlistServices()
        encryption.userEncryption(self.login_page.user, key, self.entry_name_of_service.get(), self.entry_password.get(), self.entry_login.get())
        self.listServices()
        self.entry_name_of_service.delete(0, "end")
        self.entry_password.delete(0, "end")
        self.entry_login.delete(0, "end")
    def decrypt(self, service):
        hash1 = hashlib.new('SHA256')
        hash1.update(self.login_page.key.encode())
        key = hash1.digest()
        self.decrypted = decryption.userDecryption(self.login_page.user, key, service)
        if self.label_service is not None:
            self.label_service.pack_forget()
            self.label_password.pack_forget()
            self.pass_to_clipboard.pack_forget()
            self.label_password.pack_forget()
            self.label_login.pack_forget()
            self.login_to_clipboard.pack_forget()
            self.button_delete.pack_forget()
        self.label_service = customtkinter.CTkLabel(self.frame_decrypt, text=service)
        self.label_service.pack(padx=5, pady=5)

        self.label_password = customtkinter.CTkLabel(self.frame_decrypt, text=f'Password: {self.decrypted[0]}')
        self.label_password.pack(padx=5, pady=5)

        self.pass_to_clipboard = customtkinter.CTkButton(self.frame_decrypt, text='Copy password to clipboard', command=lambda x=self.decrypted[0]: self.toClipboard(x))
        self.pass_to_clipboard.pack(padx=5, pady=5)

        self.label_login = customtkinter.CTkLabel(self.frame_decrypt, text=f'Login: {self.decrypted[1]}')
        self.label_login.pack(padx=5, pady=5)

        self.login_to_clipboard = customtkinter.CTkButton(self.frame_decrypt, text='Copy login to clipboard', command=lambda x=self.decrypted[1]: self.toClipboard(x))
        self.login_to_clipboard.pack(padx=5, pady=5)

        self.button_delete = customtkinter.CTkButton(self.frame_decrypt, text='Delete this password', command=lambda x=service: self.deletePassword(x))
        self.button_delete.pack(padx=5, pady=5)
    def deletePassword(self, service):
        sure_If_Delete_Window = SureIfDeleteWindow(master=self)
        sure_If_Delete_Window.update()
        if sure_If_Delete_Window.didAgree:
            self.unlistServices()
            passwords = fileManager.readFile(f'{utils.getPath()}appstorage\\passwords.json')
            passwords[self.login_page.user].pop(service)
            fileManager.writeFile(f'{utils.getPath()}appstorage\\passwords.json', passwords)
            self.listServices()
            self.label_service.pack_forget()
            self.label_password.pack_forget()
            self.pass_to_clipboard.pack_forget()
            self.label_password.pack_forget()
            self.label_login.pack_forget()
            self.login_to_clipboard.pack_forget()
            self.button_delete.pack_forget()
    def toClipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
app = App()
app.mainloop()