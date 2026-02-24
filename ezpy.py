import subprocess
import colorama
from enum import Enum

class PrintType(Enum):
    INFO = "info"
    ERROR = "error"
    SUCCESS = "success"

class Color(Enum):
    GREEN = "green"
    BLACK = "black"
    BLUE = "blue"
    CYAN = "cyan"
    MAGENTA = "magenta"
    WHITE = "white"
    RESET = "reset"
    YELLOW = "yellow"
    RED = "red" 


class Ezpy:
    def __init__(self):
        self.init_colorama()
        self.color = {
            Color.GREEN: colorama.Fore.GREEN,
            Color.BLACK: colorama.Fore.BLACK,
            Color.BLUE: colorama.Fore.BLUE,
            Color.CYAN: colorama.Fore.CYAN,
            Color.MAGENTA: colorama.Fore.MAGENTA,
            Color.WHITE: colorama.Fore.WHITE,
            Color.RESET: colorama.Fore.RESET,
            Color.YELLOW: colorama.Fore.YELLOW,
            Color.RED: colorama.Fore.RED
        }

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

    def call_subp(self, cmd = None, returnres = False, shell=False):
        if cmd is None:
            cmd = []
        res = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        if returnres:
            if res.returncode != 0:
                self.amel_print(f"Error [Returnres]: le returncode est {res.returncode}")
            return res
        if res.returncode == 0:
            self.amel_print(f"Returncode: {res.returncode}", PrintType.INFO)
        else:
            self.print_std(res)
    
    def amel_print(self, msg: str, type_str):
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

    def amel_input(self, msg: str, color):
        try:
            inp =  input(self.color[color] + msg + self.color[Color.RESET])
            return inp
        except KeyboardInterrupt:
            self.amel_print("ERROR: Keyboard interrupt", PrintType.ERROR)
        except Exception as e:
            self.amel_print(f"ERROR: Erreur inconue: {e}", PrintType.ERROR)
