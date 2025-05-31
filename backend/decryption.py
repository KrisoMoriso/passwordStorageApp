from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from backend import fileManager
import utils
def decrypt(key, iv_stored, ciphertext_stored):
    try:
        iv = b64decode(iv_stored)
        ct = b64decode(ciphertext_stored)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    except (ValueError, KeyError):
        print("Incorrect decryption")
def userDecryption(user, key, service):
    encrypted_data = fileManager.readFile(f'{utils.getPath()}appstorage\\passwords.json')
    decrypted_data = []
    try:
        iv = encrypted_data[user][service]['iv']
        ciphertext = encrypted_data[user][service]['ciphertext']
        decrypted_data.append(decrypt(key, iv, ciphertext))
        ciphertext = encrypted_data[user][service]['login_cipher']
        decrypted_data.append(decrypt(key, iv, ciphertext))
    except (ValueError, TypeError, KeyError):
        pass
    fileManager.writeFile(f'{utils.getPath()}appstorage\\passwords.json', encrypted_data)
    return decrypted_data