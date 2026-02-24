from ezpy import Ezpy, PrintType
import os
import platform
from pathlib import Path

class EzModify(Ezpy):
    def __init__(self):
        super().__init__()

    def add_to_path(self, new_path: str):
        """
        Ajoute `new_path` au PATH de manière permanente selon le système.
        """
        system = platform.system()
        new_path = str(Path(new_path).resolve())
        current_path = os.environ.get("PATH", "")

        if new_path in current_path.split(os.pathsep):
            self.amel_print(f"{new_path} est déjà dans PATH", PrintType.INFO)
            return

        if system == "Windows":
            # Nettoyer current_path pour éviter doublons
            current_path = current_path.rstrip(";")
            self.call_subp(["setx", "PATH", f"{current_path};{new_path}"])
            self.amel_print(f"{new_path} ajouté au PATH utilisateur (Windows)", PrintType.SUCCESS)

        elif system in ["Linux", "Darwin"]:
            # Détection du shell courant
            shell = os.environ.get("SHELL", "")
            if "bash" in shell:
                profile_file = Path.home() / ".bashrc"
            elif "zsh" in shell:
                profile_file = Path.home() / ".zshrc"
            else:
                profile_file = Path.home() / ".profile"

            export_line = f'\n# Ajout EZModify\nexport PATH="{new_path}:$PATH"\n'

            if profile_file.exists():
                lines = profile_file.read_text().splitlines()
                # Vérification stricte si le chemin est déjà exporté
                if not any(new_path == l.split('=')[1].split(':')[0] for l in lines if l.startswith("export PATH")):
                    with open(profile_file, "a") as f:
                        f.write(export_line)
            else:
                # Créer le fichier si inexistant
                with open(profile_file, "w") as f:
                    f.write(export_line)

            self.amel_print(f"{new_path} ajouté au PATH permanent ({profile_file})", PrintType.SUCCESS)

        else:
            self.amel_print(f"Système non supporté : {system}", PrintType.ERROR)

    def remove_from_path(self, path_to_remove: str):
        """
        Supprime `path_to_remove` du PATH de manière permanente selon le système.
        """
        system = platform.system()
        path_to_remove = str(Path(path_to_remove).resolve())
        current_path = os.environ.get("PATH", "")

        if path_to_remove not in current_path.split(os.pathsep):
            self.amel_print(f"{path_to_remove} n'est pas dans PATH", PrintType.INFO)
            return

        if system == "Windows":
            # reconstruire le PATH sans le chemin à supprimer
            new_path = ";".join(p for p in current_path.split(";") if p != path_to_remove)
            self.call_subp(["setx", "PATH", new_path])
            self.amel_print(f"{path_to_remove} retiré du PATH utilisateur (Windows)", PrintType.SUCCESS)

        elif system in ["Linux", "Darwin"]:
            shell = os.environ.get("SHELL", "")
            if "bash" in shell:
                profile_file = Path.home() / ".bashrc"
            elif "zsh" in shell:
                profile_file = Path.home() / ".zshrc"
            else:
                profile_file = Path.home() / ".profile"

            if profile_file.exists():
                lines = profile_file.read_text().splitlines()
                new_lines = []
                for l in lines:
                    if l.startswith("export PATH"):
                        parts = l.split('"')
                        if len(parts) >= 2:
                            paths = parts[1].split(":")
                            paths = [p for p in paths if p != path_to_remove]
                            if paths:
                                new_lines.append(f'export PATH="{":".join(paths)}"')
                    else:
                        new_lines.append(l)
                profile_file.write_text("\n".join(new_lines))
                self.amel_print(f"{path_to_remove} retiré du PATH permanent ({profile_file})", PrintType.SUCCESS)

        else:
            self.amel_print(f"Système non supporté : {system}", PrintType.ERROR)