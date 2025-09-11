import requests, httpx, time, random, string, tls_client, os, pystyle, threading, json, concurrent.futures, sys ,ctypes, secrets, websocket
from datetime import datetime; from colr import color; from colorama import Fore; from curl_cffi import requests as request

output_folder = f"output/{time.strftime('%Y-%m-%d %H-%M-%S')}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
solved = 0; genned = 0; errors = 0; locked = 0; unlock = 0  ;invaild = 0 ;genStartTime = time.time(); locked = 0
def TitleWorkerr():
    global genned, solved, errors, invaild , locked , unlock,locked
    if sys.platform == "linux" or sys.platform == "darwin":
        pass
    else:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Team-Ai | Gen : {genned} | Success+ : {unlock} | FAILD- : {locked} | INVA : {invaild} | Locked : {locked} | E! : {errors} | S+ : {solved}')
        
def remove_content(file, content):
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w") as f:
        for line in lines:
            if line.strip("\n") != content:
                f.write(line)               

def calc_Age(token):
    headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                "Authorization": token
            } 
    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    created_at = ((int(r.json()["id"]) >> 22) + 1420070400000) / 1000
    age = (time.time() - created_at) / 86400 / 30
    if age > 12:
        age_int = f"{int(age / 12)} Years"
        return age_int
    else:
        age_int = f"{int(age)} Month"
        return age_int 
       
def online_token(token):
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')        
        try:
            ws_online = websocket.WebSocket()
            ws_online.connect("wss://gateway.discord.gg/?encoding=json&v=9")
            platform = sys.platform
            status_list = ["online"]
            status = random.choice(status_list)
            ws_online.send(json.dumps({
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "$os": platform,
                        "$browser": "RTB",
                        "$device": f"{platform} Device",
                    },
                    "presence": {
                    "status": status,
                    "since": 0,
                    "activities": [],
                    "afk": False,
                },
            },
            "s": None,
            "t": None
            }))
        except:
            pass
                     
class Logger: 
    def Success(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.light_green}[ + ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()

    def Error(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.light_red}[ - ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()

    def Info(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.orange}[ $ ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()
        
    def Unlo(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.green}[ U ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()

    def Verified(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.green}[ V ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()

    def lock(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.red}[ L ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()

    def inva(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.yellow}[ I ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()

    def Captcha(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'{pystyle.Colors.cyan} [{current_time}] - {pystyle.Colors.light_blue}[ * ]  {Fore.LIGHTBLACK_EX}-> {text}')
        lock.release()  
    
class Join:
    def __init__(self):
        self.lient = request.Session(impersonate="chrome")

        
    def get_cookies(self):
        client = request.Session(impersonate="chrome")
        proxy = open('input/proxies.txt', "r", encoding="utf-8").read().splitlines()
        proxy = "http://" + random.choice(proxy).replace('sessionid', str(random.randint(1327390889,1399999999)))
        response = client.get("https://discord.com/channels/@me",proxy=proxy)

        dcfduid = response.cookies.get("__dcfduid")
        sdcfduid = response.cookies.get("__sdcfduid")
        cfruid = response.cookies.get("__cfruid")
        cfuvid = response.cookies.get("_cfuvid")
        return f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}; __cfruid={cfruid}; _cfuvid={cfuvid}; locale=en-US"
    
    def Solvecap2(self,rqd):
        global genned, solved, errors, invaild , locked , unlock,locked
        with open('config.json') as f:config = json.load(f)
        proxy = open('input/proxies.txt', "r", encoding="utf-8").read().splitlines()
        proxy = "http://" + random.choice(proxy).replace('sessionid', str(random.randint(1327390889,1399999999)))
        startedSolving = time.time()
        captchaKey = None
        while True:
            time.sleep(1)
            captchaKey = requests.post(f"http://captcha.aiclientz.com:1234/solve",
                            json={
                                "site_key": 'a9b5fb07-92ff-493f-86fe-352a2803b3df',
                                "site_url":'discord.com',
                                "rqd": rqd,
                                "proxy":proxy,
                                "key" : config['key'],
                            }
                        ,timeout=None)
            captchaKey = captchaKey.json()['captcha']
            if "P1_ey" in captchaKey or "F1_ey" in captchaKey:
                    solved = solved +1
                    TitleWorkerr()
                    Logger.Captcha(f"Solved Captcha -> {Fore.LIGHTWHITE_EX} {captchaKey[:32]} {Fore.LIGHTBLACK_EX}[Time={Fore.LIGHTWHITE_EX}{round(time.time()-startedSolving)} sec{Fore.LIGHTBLACK_EX}]")
                    return captchaKey
                
    def joiner(self,invite,Ftoken):
        try:
            client = request.Session(impersonate="chrome")
            proxy = open('input/proxies.txt', "r", encoding="utf-8").read().splitlines()
            proxy = "http://" + random.choice(proxy).replace('sessionid', str(random.randint(1327390889,1399999999)))
            global genned, solved, errors, invaild , locked , unlock,locked
            token = Ftoken.strip()
            token = token.split(':')[2]
            headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US",
            "cache-control": "no-cache",
            "content-type": "application/json",
            'cookie': self.get_cookies(),
            "origin": "https://discord.com",
            "pragma": "no-cache",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "authorization": token,
            "user-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1KTSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IFU7IFBQQyBNYWMgT1MgWDsgZGUtZGUpIEFwcGxlV2ViS2l0Lzg1LjguNSAoS0hUTUwsIGxpa2UgR2Vja28pIFNhZmFyaS84NSIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTgxODMyLCJjbGllbnRfZXZlbnRfc291cmNlIjoibnVsbCJ9",
        }
            res = client.post(f"https://discord.com/api/v9/invites/{invite}", json={},headers= headers,proxy=proxy)
            if "captcha_sitekey" in res.text:
                rqdata = res.json()['captcha_rqdata'];rqtoken = res.json()['captcha_rqtoken'];cap  = self.Solvecap2(rqdata)
                headers = {
                "authority": "discord.com",
                "accept": "*/*",
                "accept-language": "en-US",
                "cache-control": "no-cache",
                "content-type": "application/json",
                'cookie': self.get_cookies(),
                "origin": "https://discord.com",
                "pragma": "no-cache",
                "referer": "https://discord.com/channels/@me",
                "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                'x-captcha-key': cap,
                "x-captcha-rqtoken": rqtoken,
                "authorization": token,
                "user-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85",
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1KTSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IFU7IFBQQyBNYWMgT1MgWDsgZGUtZGUpIEFwcGxlV2ViS2l0Lzg1LjguNSAoS0hUTUwsIGxpa2UgR2Vja28pIFNhZmFyaS84NSIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTgxODMyLCJjbGllbnRfZXZlbnRfc291cmNlIjoibnVsbCJ9",
                }
                res = client.post(f"https://discord.com/api/v9/invites/{invite}", json={},headers=headers,proxy=proxy)

            if res.status_code == 200:
                unlock = unlock +1
                TitleWorkerr()
                Logger.Success(f"SuccessFully Joined Server -> {Fore.LIGHTWHITE_EX} {token[:32]} {Fore.LIGHTBLACK_EX}[Invite={Fore.LIGHTWHITE_EX}{invite}{Fore.LIGHTBLACK_EX}]")
                with open(f"{output_folder}/joined.txt", "a") as f:f.write(Ftoken+ "\n") 
            
            elif 'Unknown Message' in res.text:
                with open(f"{output_folder}/errors.txt", "a") as f:f.write(Ftoken+ "\n") 
                Logger.Error(f'Failed To Join Token -> {Fore.LIGHTWHITE_EX} {token[:32]} [Error={Fore.LIGHTRED_EX}Unknown Message{Fore.LIGHTBLACK_EX}]')
                errors = errors +1
                TitleWorkerr()
                
            elif res.status_code == 401:
                with open(f"{output_folder}/invalid.txt", "a") as f:f.write(Ftoken+ "\n") 
                Logger.inva(f'Token Is invalid -> {Fore.LIGHTWHITE_EX} {token[:32]}')
                invaild = invaild+1
                TitleWorkerr()
                
            elif res.status_code == 403: 
                with open(f"{output_folder}/locked.txt", "a") as f:f.write(Ftoken+ "\n") 
                Logger.lock(f'Token Is Locked -> {Fore.LIGHTWHITE_EX} {token[:32]}')
                locked = locked+1
                TitleWorkerr()
            
            elif "captcha_key" in res.text:
                with open(f"{output_folder}/captcha.txt", "a") as f:f.write(Ftoken+ "\n") 
                Logger.Info(f'Looks Like Solver or token Issue Please retry Later -> {Fore.LIGHTWHITE_EX} {token[:32]} {Fore.LIGHTBLACK_EX}[Invite={Fore.LIGHTWHITE_EX}{invite}{Fore.LIGHTBLACK_EX}]')
                locked = locked+1
                TitleWorkerr()
            
            else: 
                Logger.Error(f"Failed to Join server -> Error={Fore.LIGHTWHITE_EX} {res.text}")
                with open(f"{output_folder}/errors.txt", "a") as f:f.write(Ftoken+ "\n") 
                errors = errors +1
                TitleWorkerr()
                
        except Exception as e:
                Logger.Error(f"Failed to Join server -> Error={Fore.LIGHTWHITE_EX} {e}")
                with open(f"{output_folder}/errors.txt", "a") as f:f.write(Ftoken+ "\n") 
                errors = errors +1
                TitleWorkerr()
    def st(self, thread_limit,invite):
        with open('input/tokens.txt') as file:
            auths = file.readlines()
            self.total = len(auths)
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_limit) as executor:
                futures = []
                for combo in auths:
                    combo = combo.strip()
                    future = executor.submit(self.joiner,invite, combo)
                    futures.append(future)
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Error occurred in thread: {e}")
        time.sleep(3)

if __name__ == "__main__":
    os.system("cls")
    with open('config.json') as f:config = json.load(f)
    #with open('config.json') as config_file:config = json.load(config_file)
    k = ("""
                              _______________    __  ___      ___    ____
                             /_  __/ ____/   |  /  |/  /     /   |  /  _/
                              / / / __/ / /| | / /|_/ /_____/ /| |  / /  
                             / / / /___/ ___ |/ /  / /_____/ ___ |_/ /   
                            /_/ /_____/_/  |_/_/  /_/     /_/  |_/___/  
                            
                            
            server = https://discord.gg/recaptcha       discord = Tunable
          """)
    print(pystyle.Center.XCenter(pystyle.Colorate.Vertical(text=k, color=pystyle.Colors.cyan_to_green), spaces=15))
    thread = config['threads']
    thread = int(thread)
    invite = config['invite']
    st = Join()
    st.st(thread,invite)   

