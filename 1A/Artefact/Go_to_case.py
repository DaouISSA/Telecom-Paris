import motors as moteur
import numpy as np
import subprocess
import sys
import requests

# Script pour envoyer le robot d'une certaine position vers une case donnée

url = "http://proj103.r2.enst.fr"

# Démarrer une course
start = requests.post(url, "/api/start")

# Sous process pour envoyer la position (x, y) au serveur de suivi chaque seconde en continu
# Pensez à l'arrêter si vous le décommentez, pos_update.py marche avec un while True donc ne fini pas par lui-même
process = subprocess.Popen(['python3', '/home/go4t/team5/Main_file/pos_update.py'])

# Vitesse de translation et de rotation
va = 50
vt = 50

mot = moteur.RobotControl()


# Fonctions moteurs
def avancer(d):
    mot.avancer(d,va,True)

def tourner(theta) :
    mot.tourner(theta,vt,True)

def strategy(idx,idy) :
    # Stratégie mécanique dans lequel le robot se rend directement sur la case demandée, sans utiliser la caméra
    avancer(50)  # Se positionne sur la case 2 6 (au milieu, juste après la ligne de départ
    vectx = (idx - 2) * 50  # La distance en x qui le sépare de la case
    vecty = (6 - idy) * 50  # La distance en y qui le sépare de la case
    if vecty == 0 :  # Pour ne pas diviser par 0
        if vectx > 0 :
            tourner(90)
        elif vectx < 0 :
            tourner(-90)
    else :
        tourner(np.arctan(vectx/vecty)*180/np.pi)  # Sinon le calcule classique
    print(f"Avancer de {np.sqrt(vectx*vectx + vecty*vecty)}")
    avancer(np.sqrt(vectx*vectx + vecty*vecty))  # Et on avance de la norme (pythagore je vais pas t'apprendre)
    tourner(360)  # Danse de la victoire
    process.terminate()
    # Arrêter une course
    requests.post(url, "/api/stop")


if __name__ == "__main__":
    if (len(sys.argv) != 3):  # Si y'a pas le bon nombre d'argument
        sys.exit("Mauvais paramètre !\nIl faut la case en x (entre 1 et 3) et la case en y (entre 1 et 6)")
    argx = int(float(sys.argv[1]))
    argy = int(float(sys.argv[2]))
    if (argx < 1 or argx > 3 or argy < 1 or argy > 6):  # Ou si il ne corresponde pas à une case
        sys.exit("Mauvais paramètre !\nIl faut la case en x (entre 1 et 3) et la case en y (entre 1 et 6)")
    #Sinon c'est bon on y va
    print(f"Allons à la case {argx}{argy}")
    strategy(argx, argy)
    print("Victoire !")
