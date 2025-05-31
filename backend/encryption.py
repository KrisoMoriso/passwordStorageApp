from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

import utils
from backend import fileManager


def encrypt(key, data, iv=None):
    if iv is None:
        cipher = AES.new(key, AES.MODE_CBC)
    else:
        cipher = AES.new(key, AES.MODE_CBC, b64decode(iv))
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return {'iv': iv, 'ciphertext': ct}
def userEncryption(user, key, service, data, login):
    encrypted_data = fileManager.readFile(f'{utils.getPath()}appstorage\\passwords.json')
    #encrypt
    result = encrypt(key, data.encode())
    encrypted_data[user].update({service:result})
    _iv = result['iv']
    #encrypt login
    result = encrypt(key, login.encode(), iv=_iv)
    encrypted_data[user][service].update({"login_cipher": result['ciphertext']})
    fileManager.writeFile(f'{utils.getPath()}appstorage\\passwords.json', encrypted_data)
