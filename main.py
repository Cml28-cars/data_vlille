import requests
import os
from datetime import datetime
from flask import Flask

# Créer dossier si besoin
os.makedirs("data", exist_ok=True)



# Télécharger le fichier
def telecharger():
    date_jour = f"{datetime.now().strftime('%Y-%m-%d')}"
    chemin_complet_jour = os.path.join("data", date_jour)
    os.makedirs(chemin_complet_jour, exist_ok=True)
    url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=csv&limit=-1"
    fichier_telecharge =  f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    fichier_sortie = os.path.join(chemin_complet_jour, fichier_telecharge )

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_sortie, "wb") as f:
            f.write(response.content)
        print(f"[✅] Fichier téléchargé : {fichier_sortie}")
    else:
        print(f"[❌] Échec : {response.status_code}")

# Lancer la tâche une fois au démarrage
telecharger()

# Petit serveur web pour garder le Repl actif
app = Flask(__name__)

@app.route("/")
def home():
    return "Vlille bot actif"

app.run(host="0.0.0.0", port=8080)
