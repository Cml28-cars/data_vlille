#!/usr/bin/env python3
import subprocess
from datetime import datetime

def push_to_git(logfile_path="fichier_suivi.log"):
    now_h = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 1. Ajouter les fichiers importants dans l'index
        subprocess.run(["git", "add", "data/"], check=True)
        subprocess.run(["git", "add", "fichier_suivi.log"], check=True)
        subprocess.run(["git", "add", "mon_bot.py", "transfert_git.py"], check=True)

        # 2. Commit horodaté (n'explose pas si rien à commit)
        commit_msg = f"Auto-commit: {now_h}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=False
        )

        # 3. Push vers la branche main (et plus master)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("[✅] Push GitHub OK (branche main)")

        # 4. Tracer dans le log que le push est bien parti
        with open(logfile_path, "a", encoding="utf-8") as suivi:
            suivi.write(f"[{now_h}] PUSH_OK vers GitHub (main)\n")

    except subprocess.CalledProcessError as e:
        print(f"[❌] Erreur lors du push : {e}")
        with open(logfile_path, "a", encoding="utf-8") as suivi:
            suivi.write(f"[{now_h}] PUSH_FAIL {e}\n")
