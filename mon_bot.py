import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

import requests
from datetime import datetime

import os

#Pour créer mon dossier de données journalier
date_jour = f"{datetime.now().strftime('%Y-%m-%d')}"
chemin_complet_jour = os.path.join("data", date_jour)
os.makedirs(chemin_complet_jour, exist_ok=True)

# URL du fichier CSV à télécharger
url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=csv&limit=-1"

# Nom du fichier de sortie avec horodatage
fichier_telecharge =  f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
#je le replace dans le dossier du jour
fichier_sortie = os.path.join(chemin_complet_jour, fichier_telecharge )

# Télécharger le fichier + le rentrer dans le fichier de suivi
response = requests.get(url)

fichier_suivi = "fichier_suivi.log"

with open(fichier_suivi, "a") as suvi:
    if response.status_code == 200:
        with open(fichier_sortie, "wb") as f:
            f.write(response.content)
        print(f"[✅] Fichier téléchargé : {fichier_sortie}")
        suvi.write(f"[{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}] ✅ {fichier_sortie}\n")
    else:
        print(f"[❌] Échec du téléchargement (code {response.status_code})")
        suvi.write(f"[{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}] ❌ Erreur {response.status_code} sur {url}\n")