import requests
import time

session = requests.Session()

# Sous processus à appeler pour l'envoi des requêtes au serveur de suivi

url = "http://proj103.r2.enst.fr"

while True:
    nb_requetes = 0
    coord = ''
    # On récupère les coordonnées depuis un document .txt dans lequel le robot écrit sa position
    while coord == '':
        with open("/home/go4t/team5/Main_file/update_position.txt", 'r') as f:
            coord = f.read()
    coord = coord.split(';')
    x, y = coord[0], 300-float(coord[1])
    try:
        pos = session.post(url+"/api/pos?x="+x+"&y="+str(y))
    except requests.exceptions.RequestException as e:
        print(f"Erreur à la requête :", e)
    time.sleep(1)