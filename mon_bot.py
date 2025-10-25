#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

import requests
from datetime import datetime
import os
import schedule
import time

def telecharger():
    # Créer dossier du jour
    date_jour = datetime.now().strftime("%Y-%m-%d")
    chemin_complet_jour = os.path.join("data", date_jour)
    os.makedirs(chemin_complet_jour, exist_ok=True)

    # URL + nom du fichier horodaté
    url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=csv&limit=-1"
    horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fichier_sortie = os.path.join(chemin_complet_jour, f"{horodatage}.csv")
    fichier_suivi = "fichier_suivi.log"

    try:
        response = requests.get(url)
        with open(fichier_suivi, "a") as suivi:
            if response.status_code == 200:
                with open(fichier_sortie, "wb") as f:
                    f.write(response.content)
                print(f"[✅] Fichier téléchargé : {fichier_sortie}")
                suivi.write(f"[{horodatage}] ✅ {fichier_sortie}\n")
            else:
                print(f"[❌] Échec du téléchargement : code {response.status_code}")
                suivi.write(f"[{horodatage}] ❌ Erreur {response.status_code} sur {url}\n")
    except Exception as e:
        print(f"[⚠️] Exception : {e}")
        with open(fichier_suivi, "a") as suivi:
            suivi.write(f"[{horodatage}] ⚠️ Exception : {e}\n")

# Téléchargement immédiat au lancement
telecharger()

# Planification toutes les 2 minutes
schedule.every(2).minutes.do(telecharger)

# Boucle principale
while True:
    schedule.run_pending()
    time.sleep(1)
