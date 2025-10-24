import os
import requests
import pytz
import json
from datetime import datetime
import subprocess


def telecharger():
paris = pytz.timezone("Europe/Paris")
heure_locale = datetime.now(paris)


date_jour = heure_locale.strftime("%Y-%m-%d")
chemin_jour = os.path.join("data", date_jour)
os.makedirs(chemin_jour, exist_ok=True)


url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=csv&limit=-1"
fichier_csv = f"{heure_locale.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
fichier_sortie = os.path.join(chemin_jour, fichier_csv)
response = requests.get(url)
if response.status_code == 200:
with open(fichier_sortie, "wb") as f:
f.write(response.content)
print(f"[✅] Téléchargé : {fichier_sortie}")
with open("fichier_suivi.log", "a") as log:
log.write(f"[{heure_locale.strftime('%Y-%m-%d %H:%M:%S')}] ✅ {fichier_sortie}\n")
else:
print(f"[❌] Échec ({response.status_code})")


# Mise à jour JSON statut
with open("status.json", "w") as f:
json.dump({
"last_file": fichier_sortie,
"last_push": heure_locale.strftime('%Y-%m-%d %H:%M:%S')
}, f)


subprocess.run(["python3", "transfert_git.py"])


if __name__ == "__main__":
telecharger()
