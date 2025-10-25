#!/usr/bin/env python3
import subprocess
from datetime import datetime

def push_to_git():
    try:
        # 1. Stage des fichiers qu'on veut suivre
        subprocess.run(["git", "add", "data/"], check=True)
        subprocess.run(["git", "add", "fichier_suivi.log"], check=True)
        subprocess.run(["git", "add", "mon_bot.py", "transfert_git.py"], check=True)

        # 2. Commit horodaté
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # check=False pour ne pas planter si y'a "nothing to commit"
        subprocess.run(
            ["git", "commit", "-m", f"Auto-commit: {now}"],
            check=False
        )

        # 3. Push vers la bonne branche (chez toi : master)
        subprocess.run(["git", "push", "origin", "master"], check=True)

        print("[✅] Modifications poussées sur GitHub")

    except subprocess.CalledProcessError as e:
        print(f"[❌] Erreur lors du push : {e}")
