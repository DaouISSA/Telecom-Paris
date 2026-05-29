import motors as moteur
import numpy as np
import subprocess
import sys
import time

# A modifier pour update la position sur le serveur de l'école

va = 50
vt = 50

mot = moteur.RobotControl()

def avancer(d):
    mot.avancer(d,va,True)

def tourner(theta) :
    mot.tourner(theta,vt,True)
def parcourir_colonne(cases):
    for i in range(cases):
        avancer(50)
        tourner(45+2*i)
        time.sleep(0.5)
        tourner(45+2*i)
        time.sleep(0.5)
        tourner(90)
        time.sleep(0.5)
        tourner(90)
        time.sleep(0.5)
        tourner(90)
        time.sleep(0.5)
        tourner(45)
if __name__ == "__main__":
    if (len(sys.argv) != 2):  # Si y'a pas le bon nombre d'argument
        sys.exit("Mauvais paramètre !\nIl faut la case en x (entre 1 et 3) et la case en y (entre 1 et 6)")
    argx = int(float(sys.argv[1]))
    
    if (argx>6 or argx<1):  # Ou si il ne corresponde pas à une case
        sys.exit("Mauvais paramètre, x doit être entre 1 et 6")
    #Sinon c'est bon on y va
    print(f"Allons à la case {argx}")
    parcourir_colonne(argx)
    print("Victoire !")