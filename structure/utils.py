import signal, json, re, time, threading, sys, os
from typing import List, Dict, Tuple
from colorama import init, Fore, Style

class NatsumeUtils:
    def __init__(self, cli=True):
        init(convert=True)

        if "--colorless" in sys.argv:
            self.RED = Fore.WHITE
            self.GREEN = Fore.WHITE
            self.BLUE = Fore.WHITE
            self.CYAN = Fore.WHITE
            self.XRED = Fore.WHITE
            self.XGREEN = Fore.WHITE
            self.XBLUE = Fore.WHITE
            self.XCYAN = Fore.WHITE
            self.CLR = Fore.WHITE
        else:
            self.RED = Fore.MAGENTA
            self.GREEN = Fore.GREEN
            self.BLUE = Fore.BLUE
            self.CYAN = Fore.CYAN
            self.XRED = Fore.LIGHTMAGENTA_EX
            self.XGREEN = Fore.LIGHTGREEN_EX
            self.XBLUE = Fore.LIGHTBLUE_EX
            self.XCYAN = Fore.LIGHTCYAN_EX
            self.CLR = Style.RESET_ALL
        self.lock = threading.Lock()
        self.uptime = time.time()
        signal.signal(signal.SIGINT, self.graceExit)
        signal.signal(signal.SIGTERM, self.graceExit)

    def graceExit(self, handler=None, frame=None):
        print("Exiting...")
        exit()
    
    def getConfig(self, submodule=None) -> dict:
        try:
            with open("profile.json", "r+") as cfg:
                config = json.load(cfg)
            return config
        except FileNotFoundError:
            self.printInfo("ConfigLoader", "Existing Configuration is not existed!")
            defaultProfile = {
                "natsume": {
                    "persona": "maid",
                    "extensions": [
                        "core",
                        "misc"
                    ]
                }
            }

            with open("profile.json", "w") as f:
                f.write(json.dumps(defaultProfile, indent=3))
            return defaultProfile
    
    def getUptime(self):
        upTime = time.time() - self.uptime
        return "{} {} {}".format(
            str(upTime//3600) + "h" if upTime >= 3600 else "\0",
            str(upTime//60) + "m" if upTime >= 60 else "\0",
            str(int(upTime%60)) + "s" if upTime != 0 else '\0'
        )
            
    def reloadConfig(self) -> dict:
        with open("profile.json", "r+") as cfg:
            return json.load(cfg)

    def printError(self, mod, err):
        with self.lock: print(f"{self.RED}[{mod}] {err}{self.CLR}")

    def printInfo(self, mod, info):
        with self.lock: print(f"{self.BLUE}[{mod}] {info}{self.CLR}")

    def argsParser(self, args: str) -> Tuple[str, Dict[str, str]]:
        arg = [x.strip("\"") for x in re.findall("(?:\".*?[^\\\\]\"|\S)+", args)]
        argMap = dict()
        title = arg[0]

        # Redirect to inviduals help menu        
        if (len(arg) == 2) and str(arg[1].strip("-")).lower() == 'help':
            return "help", {'name': title}

        for i in range(1, len(arg)-1, 2):
            argMap[arg[i].strip("-")] = arg[i+1]
        return title, argMap 
        
    def isDigit(self, args: str) -> bool:
        try:
            int(args)
        except ValueError:
            return False
        else:
            return True

    def clrscr(self): 
        os.system("cls")
