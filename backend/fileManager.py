import json
import utils

def readFile(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)
def writeFile(filePath, data):
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=4)
if __name__ == '__main__':
    data = {
    "kris": {
        "allegro": {
            "iv": "HqwVcJEZkupskonnYzhME4jtkP0Q==",
            "ciphertext": "zh6xJNnRX1MN1fU8nz6GLg=="
        }
    },
    "test": {},
    "test2": {}
}


    writeFile(f'{utils.getPath()}appstorage\\passwords.json', data)