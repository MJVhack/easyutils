import argparse
import json
from pathlib import Path
from dependences import controltv

CONFIG_FILE = Path.home() / ".tv_control.json"

MODULES = {
    "controltv": "Contrôle TV Android via ADB",
}

def save_ip(ip):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"ip": ip}, f)

def load_ip():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("ip")
    return None

def main():
    parser = argparse.ArgumentParser(
        description="EasyUtils - Collection d'utilitaires",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("module", nargs="?", help="Nom du module à utiliser")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments du module")

    args = parser.parse_args()

    if not args.module:
        print("Modules disponibles :\n")
        for mod, desc in MODULES.items():
            print(f"  {mod} : {desc}")
        print("\nUsage : easyutils <module> [args]")
        return

    mod_name = args.module.lower()
    if mod_name not in MODULES:
        print(f"Module '{mod_name}' inconnu")
        return

    if mod_name == "controltv":
        if not args.args:
            print("ControlTV - commandes disponibles :")
            print("  ip <IP>                : enregistre l'adresse IP de la TV")
            print("  reboot                 : redémarre la TV")
            print("  volume_haut / volume_bas / ok / bas / haut / gauche / droite / home / menu / retour / mute / shutdown")
            print("  open_app <app>         : ouvre une app (ex: netflix, youtube)")
            print("  close_app <app>        : ferme une app")
            print("  install <fichier.apk>  : installe un APK")
            print("  rinstall <fichier.apk> : réinstalle un APK")
            return

        cmd = args.args[0].lower()


        if cmd == "ip":
            if len(args.args) < 2:
                print("Erreur : IP requise")
                return
            ip = args.args[1]
            save_ip(ip)
            print(f"IP '{ip}' enregistrée pour ControlTV")
            return

        ip = load_ip()
        if not ip:
            print("Erreur : IP non définie. Enregistrez-la avec 'easyutils controltv ip <IP>'")
            return

        tv = controltv.TV(ip)

        simple_keys = ["reboot","volume_haut","volume_bas","ok","bas","haut","gauche",
                       "droite","home","menu","retour","mute","shutdown"]
        if cmd in simple_keys:
            if cmd == "reboot":
                tv.reboot()
            else:
                tv.base_control(cmd)
            return
        if cmd == "open_app":
            if len(args.args) < 2:
                print("Erreur : nom de l'app requis")
                return
            tv.manage_app("open", args.args[1].lower())
            return

        if cmd == "close_app":
            if len(args.args) < 2:
                print("Erreur : nom de l'app requis")
                return
            tv.manage_app("close", args.args[1].lower())
            return


        if cmd in ["install","rinstall"]:
            if len(args.args) < 2:
                print("Erreur : fichier APK requis")
                return
            tv.apk("install" if cmd=="install" else "Rinstall", args.args[1])
            return

        print(f"Commande '{cmd}' inconnue pour ControlTV")

if __name__ == "__main__":
    main()
