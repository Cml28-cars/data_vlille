#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

# Charger le token GitHub depuis les secrets
token = os.getenv("GH_TOKEN")

# Sécurité : ne continue pas si le token est absent
if not token:
    print("[❌] Aucun token trouvé dans GH_TOKEN.")
    exit(1)

# Configurer Git (si pas déjà fait)
subprocess.run(["git", "config", "--global", "user.name", "Replit-Bot"])
subprocess.run(["git", "config", "--global", "user.email", "bot@replit.com"])

# Mettre à jour le remote avec le token
remote_url = f"https://{token}@github.com/Cml28-cars/data_vlille.git"
subprocess.run(["git", "remote", "set-url", "origin", remote_url])

# Récupérer les changements distants si besoin
subprocess.run(["git", "pull", "--rebase", "--autostash", "origin", "main"])

# Ajouter les fichiers dans /data et le fichier de suivi s'il existe
subprocess.run(["git", "add", "data/"])
if os.path.exists("fichier_suivi.log"):
    subprocess.run(["git", "add", "-f", "fichier_suivi.log"])  # force l'ajout même si ignoré

# Vérifier s'il y a quelque chose à commit
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

if status.stdout.strip():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "commit", "-m", f"Auto-commit: {now}"])
    subprocess.run(["git", "push", "origin", "main"])
    print("[✅] Modifications poussées avec succès.")
else:
    print("[ℹ️] Aucun changement à committer.")
