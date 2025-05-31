import hashlib

import utils
from backend import fileManager
def login(user, user_password):
    user_credentials = fileManager.readFile(f'{utils.getPath()}appstorage\\user_credentials.json')
    hash1 = hashlib.new('SHA256')
    hash1.update(user_password.encode())
    try:
        if not user_credentials[user] == hash1.hexdigest():
            return False
        elif user_credentials[user] == hash1.hexdigest():
            return True
    except KeyError:
        return False
def createAccount(user, user_password):
    user_credentials = fileManager.readFile(f'{utils.getPath()}appstorage\\user_credentials.json')
    encrypted_data = fileManager.readFile(f'{utils.getPath()}appstorage\\passwords.json')
    if not (user in user_credentials):
        hash1 = hashlib.new('SHA256')
        hash1.update(user_password.encode())
        user_credentials.update({user: hash1.hexdigest()})
        encrypted_data.update({user: {}})

        fileManager.writeFile(f'{utils.getPath()}appstorage\\user_credentials.json', user_credentials)
        fileManager.writeFile(f'{utils.getPath()}appstorage\\passwords.json', encrypted_data)
        return True
    else:
        return False