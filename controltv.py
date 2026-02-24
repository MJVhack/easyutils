import subprocess
import colorama
from enum import Enum

class PrintType(Enum):
    INFO = "info"
    ERROR = "error"
    SUCCESS = "success"

class TV:
    def __init__(self, ip):
        self.ip = ip
        self.template_ke = ["adb", "shell", "input", "keyevent"]
        self.table_control = {"haut" : "19",
                               "bas" : "20", 
                               "gauche" : "21",
                               "droite" : "22", 
                               "OK" : "23", 
                               "retour" : "4", 
                               "home" : "3", 
                               "menu" : "82",
                               "volume_haut" : "24",
                               "volume_bas" : "25",
                               "mute" : "164",
                               "power" : "26",
                               "shutdown" : "223",
                               "wake" : "224",
                               }
        self.table_app = {
            "netflix": "com.netflix.ninja",
            "youtube": "com.google.android.youtube.tv",
            "primevideo": "com.amazon.avod.thirdpartyclient",
            "disneyplus": "com.disney.disneyplus",
            "hbo": "com.hbo.hbonow",
            "spotify": "com.spotify.tv.android",
            "plex": "com.plexapp.android",
            "vlc": "org.videolan.vlc",
            "twitch": "tv.twitch.android.viewer",
            "hulu": "com.hulu.livingroomplus",
            "youtube_kids": "com.google.android.apps.youtube.kids",
            "google_play_movies": "com.google.android.videos",
            "google_play_music": "com.google.android.music",
            "tiktok": "com.zhiliaoapp.musically",
            "primevideo_kids": "com.amazon.avod.thirdpartyclient.kids",
            "crunchyroll": "com.crunchyroll.crunchyroid",
            "bbc_iplayer": "uk.co.bbc.iplayer.android.tv",
            "apple_tv": "com.apple.tv",
        }
        self.table_info_sys = [["adb", "shell", "getprop"],
                                ["adb", "shell", "dumpsys"],
                                ["adb", "shell", "wm", "size"],
                                ["adb", "shell", "wm", "density"]]
        self.color = {
            "green": colorama.Fore.GREEN,
            "black": colorama.Fore.BLACK,
            "blue": colorama.Fore.BLUE,
            "cyan": colorama.Fore.CYAN,
            "magenta": colorama.Fore.MAGENTA,
            "white": colorama.Fore.WHITE,
            "reset": colorama.Fore.RESET,
            "yellow": colorama.Fore.YELLOW,
            "red": colorama.Fore.RED
        }

        self.adbs = ["adb", "shell"]
        self.init_colorama()
    def init_colorama(self):
        # A faire que avec une instance, je le mets ici pour que
        # l'utilisation soit facile
        colorama.init()

    def print_std(self, stdobject):
        print()
        print(f"{self.color["blue"]}STDOUT: {stdobject.stdout}")
        print(f"{self.color["red"]}STDERR: {stdobject.stderr}")
        if stdobject.returncode == 0:
            print(f"{self.color["green"]}Return code: {stdobject.returncode}{self.color["reset"]}")
            print()
        else:
            print(f"{self.color["red"]}Return code: {stdobject.returncode}{self.color["reset"]}")
            print()

    def call_subp(self, cmd = None, returnres = False):
        if cmd is None:
            cmd = []
        res = subprocess.run(cmd, capture_output=True, text=True)
        if returnres:
            if res.returncode != 0:
                self.espaced_print(f"Error [Returnres]: le returncode est {res.returncode}")
            return res
        if res.returncode == 0:
            self.espaced_print(f"Returncode: {res.returncode}", PrintType.INFO)
        else:
            self.print_std(res)
        
    def espaced_print(self, msg: str, type_str):
        if type_str == PrintType.INFO:
            print()
            print(self.color["blue"] + msg + self.color["reset"])
            print()
        elif type_str == PrintType.ERROR:
            print()
            print(self.color["red"] + msg + self.color["reset"])
            print()
        elif type_str == PrintType.SUCCESS:
            print()
            print(self.color["green"] + msg + self.color["reset"])
            print()
    
    def connect(self):
        self.call_subp(["adb", "connect", self.ip])
        self.espaced_print("Adb connecté a la télé", PrintType.SUCCESS)
        

    def base_control(self, control: str):
        if control in self.table_control:
            self.call_subp(self.template_ke + [self.table_control[control]])
            return
        else:
            print(f"{control} non présent dans la table [self.table_control]")

    def manage_app(self, action: str, app: str):
        if app in self.table_app:
            app_package = self.table_app[app]
            if action == "close":
                self.call_subp(self.adbs + ["am", "force-stop", app_package])
                self.espaced_print(f"Action [{action} {app}]  éffectuer", PrintType.SUCCESS)
            elif action == "open":
                self.call_subp(self.adbs + ["monkey", "-p", app_package, "-c", "android.intent.category.LAUNCHER", "1"])
                self.espaced_print(f"Action [{action} {app}]  éffectuer", PrintType.SUCCESS)
            elif action == "uninstall":
                self.call_subp(self.adbs + ["pm", "uninstall", "-user", "0", app_package])
                self.espaced_print(f"Action [{action} {app}]  éffectuer", PrintType.SUCCESS)
            else:
                self.espaced_print(f"Error: action[{action}] n'est pas dans la liste des actions autorisé (close, open, uninstall)", PrintType.ERROR)
    
    def apk(self, action: str, app: str):
        if action == "install":
            self.call_subp(["adb", action, app])
            self.espaced_print(f"Action [{action} {app}]  éffectuer", PrintType.SUCCESS)
        elif action == "Rinstall":
            self.call_subp(["adb", "install", "-r", app])
            self.espaced_print(f"Action [{action} {app}]  éffectuer", PrintType.SUCCESS)
        else:
            self.espaced_print(f"Error: action[{action}] n'est pas dans la liste des actions autorisé (install, Rinstall)", PrintType.ERROR)

    def reboot(self):
        self.call_subp(["adb", "reboot"])
        self.espaced_print("Reboot éffectuer", PrintType.SUCCESS)

    def screenshot(self, action: str):
        if action == "screen":
            self.call_subp(self.adbs + ["screencap", "-p", "/sdcard/screen.png"])
            self.call_subp(["adb", "pull", "/sdcard/screen.png"])
            self.espaced_print(f"L'action [{action}] a été éffectuer a l'adresse [/sdcard/screen.png]", PrintType.SUCCESS)
        elif action == "record":
            self.call_subp(self.adbs +  ["screenrecord", "/sdcard/video.mp4"])
            self.espaced_print(f"L'action [{action}] a été éffectuer a l'adresse [/sdcard/video.mp4]", PrintType.SUCCESS)
        else:
            self.espaced_print(f"Error: action[{action}] n'est pas dans la liste des actions autorisé (screen, record)", PrintType.ERROR)

    def sys_info(self):
        for i in self.table_info_sys:
            res = self.call_subp(i, True)
            self.espaced_print(res.stdout, PrintType.INFO)
            if res.returncode != 0:
                self.espaced_print(res.stderr, PrintType.ERROR)