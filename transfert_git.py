#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

import subprocess

def push_to_git():
    try:
        # Ajouter les fichiers (modifie selon ton arborescence)
        subprocess.run(["git", "add", "data/"], check=True)
        subprocess.run(["git", "add", "fichier_suivi.log"], check=True)

        # Commit horodaté
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"Auto-commit: {now}"], check=True)

        # Push
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[✅] Modifications poussées sur GitHub")
    except subprocess.CalledProcessError as e:
        print(f"[❌] Erreur lors du push : {e}")
