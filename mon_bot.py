import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

import requests
from datetime import datetime

import os

import schedule
import time

import pytz
from flask import Flask
import threading
import json

# Créer dossier si besoin
os.makedirs("data", exist_ok=True)


# Télécharger le fichier
def telecharger():
    paris = pytz.timezone("Europe/Paris")
    heure_locale = datetime.now(paris)

    date_jour = f"{heure_locale.strftime('%Y-%m-%d')}"
    chemin_complet_jour = os.path.join("data", date_jour)
    os.makedirs(chemin_complet_jour, exist_ok=True)

    url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=csv&limit=-1"
    fichier_telecharge = f"{heure_locale.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    fichier_sortie = os.path.join(chemin_complet_jour, fichier_telecharge)

    response = requests.get(url)

    fichier_suivi = "fichier_suivi.log"

    with open(fichier_suivi, "a") as suvi:
        if response.status_code == 200:
            with open(fichier_sortie, "wb") as f:
                f.write(response.content)
            print(f"[✅] Fichier téléchargé : {fichier_sortie}")
            suvi.write(
                f"[{heure_locale.strftime('%Y-%m-%d_%H-%M-%S')}] ✅ {fichier_sortie}\n"
            )
        else:
            print(f"[❌] Échec du téléchargement (code {response.status_code})")
            suvi.write(
                f"[{heure_locale.strftime('%Y-%m-%d_%H-%M-%S')}] ❌ Erreur {response.status_code} sur {url}\n"
            )

    
    with open("status.json", "w") as f:
        json.dump(
            {
                "last_file": fichier_sortie,
                "last_push": heure_locale.strftime('%Y-%m-%d %H:%M:%S')
            },
            f)


# Lancer la tâche une fois au démarrage
telecharger()

schedule.every(2).minutes.do(telecharger)

def boucle_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Petit serveur web pour garder le Repl actif
app = Flask(__name__)

if __name__ == "__main__":
    threading.Thread(target=boucle_schedule, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
