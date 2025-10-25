#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

import requests
from datetime import datetime
import os
import schedule
import time

from transfert_git import push_to_git  # on importe la fonction depuis transfert_git.py

URL = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=csv&limit=-1"
LOGFILE = "fichier_suivi.log"

def telecharger():
    # Créer dossier du jour
    date_jour = datetime.now().strftime("%Y-%m-%d")
    chemin_complet_jour = os.path.join("data", date_jour)
    os.makedirs(chemin_complet_jour, exist_ok=True)

    # Nom du fichier horodaté pour la capture temps réel
    horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fichier_sortie = os.path.join(chemin_complet_jour, f"{horodatage}.csv")

    try:
        response = requests.get(URL)

        with open(LOGFILE, "a", encoding="utf-8") as suivi:
            if response.status_code == 200:
                # on écrit le CSV
                with open(fichier_sortie, "wb") as f:
                    f.write(response.content)

                # console (tu peux garder les emojis ici)
                print(f"[✅] Fichier téléchargé : {fichier_sortie}")

                # log (sans emoji pour éviter les encodages chelous si jamais tu l'ouvres ailleurs)
                suivi.write(f"[{horodatage}] OK {fichier_sortie}\n")

            else:
                print(f"[❌] Échec du téléchargement : code {response.status_code}")
                suivi.write(f"[{horodatage}] ERROR {response.status_code} sur {URL}\n")

    except Exception as e:
        print(f"[⚠️] Exception pendant le téléchargement : {e}")
        with open(LOGFILE, "a", encoding="utf-8") as suivi:
            suivi.write(f"[{horodatage}] EXCEPTION {e}\n")

    # après avoir téléchargé et loggé, on versionne et on pousse
    push_to_git()


# Lancement immédiat
telecharger()

# Planification toutes les 2 minutes
schedule.every(2).minutes.do(telecharger)

# Boucle infinie
while True:
    schedule.run_pending()
    time.sleep(1)
