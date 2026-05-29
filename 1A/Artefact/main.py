#!/usr/bin/env python3
import time
import Main_file.Detection_and_Pos_estimation as cam
import Motors.motors as moteur
import numpy as np
import cv2
import math as m
import subprocess
import requests
mot = moteur.RobotControl()


url = "http://proj103.r2.enst.fr"

# Démarrer une course
start = requests.post(url, "/api/start")

# Sous process pour envoyer la position (x, y) au serveur de suivi chaque seconde en continu
# Pensez à l'arrêter si vous le décommentez, pos_update.py marche avec un while True donc ne fini pas par lui-même
process = subprocess.Popen(['python3', '/home/go4t/team5/Main_file/pos_update.py'])

# Partie caméra

# Array for markers of size 2cm
marker_points2 = np.array([[-2 / 2, 2 / 2, 0],
                                [2 / 2, 2 / 2, 0],
                                [2 / 2, -2 / 2, 0],
                                [-2 / 2, -2 / 2, 0]], dtype=np.float32)

# Array for markers of size 10cm
marker_points10 = np.array([[-10 / 2, 10 / 2, 0],
                                [10 / 2, 10 / 2, 0],
                                [10 / 2, -10 / 2, 0],
                                [-10 / 2, -10 / 2, 0]], dtype=np.float32)

# These are the matrix from the camera calibration
# Warning, the parameters are different for each camera, you'll have to compute them again if you were to change the camera.
# Use Camera_calibration.py for that
cam_param = np.load('/home/go4t/Test_file/Calibration/Cam_calib.npz')

# Dictionnary for arUco markers
ARUCO_DICT = {"DICT_6X6_50": cv2.aruco.DICT_6X6_50}

# Load the ArUCo dictionary and grab the ArUCo parameters
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT['DICT_6X6_50'])
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# Receives the video from camera
vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_AUTOFOCUS, 0)
vs.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Vitesses de translation et de rotation
va = 30
vt = 30

# Variables relatives aux deux balises de l'épreuve intermédiaire
Balise1_coord = (0,0)
Balise2_coord = (0,0)
Balise1_id = 0
Balise2_id = 0
Balise1_found = False
Balise2_found = False


# Partie moteurs du robot
def avancer(d):
    mot.avancer(d,va,True)

def tourner(theta) :
    mot.tourner(theta,vt,True)


# Partie gestion de la stratégie du robot

def get_robot_coord():
    while RobotCoord == ['']:
        with open('/home/go4t/team5/Main_file/update_position.txt', 'r') as file:
            RobotCoord = file.read().split(';')
    return (int(float(RobotCoord[0], int(float(RobotCoord[1])), int(float(RobotCoord[2])))))

# Capture du drapeaux + rotation sur lui même
def emote(mid) :
    nb_requetes = 0
    mcol, mrow, _ = get_robot_coord()
    mcol = str(mcol//50 + 1)
    mrow = str(mrow//50 + 65)
    cap = requests.post(url+"/api/marker?id="+str(mid)+"&col="+mcol+"&row="+mrow)
    while (cap.status_code != 200 or cap.status_code != 503) and nb_requetes < 50:
        cap = requests.post(url+"/api/marker?id="+str(mid)+"&col="+mcol+"&row="+mrow)
        nb_requetes += 1
    print(f'La requête pour la capture de drapeau: {cap}')
    tourner(360)

def Coord_Relative_To_Coord_Absolue(dist: float, angle: float):
    x, y, orient = get_robot_coord()
    return (x - np.sin((orient+angle)*np.pi/180)*dist,y + np.cos((orient+angle)*np.pi/180)*dist)

def cherche_balise_ret():
    # Fais un tour sur lui même à la recherche de balises d'objectif,et renvoie la position de la plus proche
    global Balise1_coord
    global Balise1_id
    while Balise1_coord == (0,0):
        vs.grab()
        _, frame = vs.read()
        #cv2.imwrite('./image_'+str(i)+'.png', frame)
        value = cam.detection(marker_points2,marker_points10,arucoDetector,cam_param,frame)
        for id_mark in value.keys():
            if (id_mark > 4):
                    Balise1_coord = Coord_Relative_To_Coord_Absolue(value[id_mark]["Dist"], value[id_mark]["Angle"])
                    Balise1_id = id_mark
                    print(Balise1_coord)
                    return 1
        tourner(45)
        time.sleep(0.2)

def cherche_balise_222() :
    # Fais un tour sur lui même à la recherche de balises d'objectif,et renvoie la position de la plus proche
    global Balise2_coord
    global Balise2_id
    global Balise1_id
    while Balise2_coord == (0,0):
        vs.grab()
        _, frame = vs.read()
        #cv2.imwrite('./image_'+str(i)+'.png', frame)
        value = cam.detection(marker_points2,marker_points10,arucoDetector,cam_param,frame)
        for id_mark in value.keys():
            if (id_mark > 4) and (id_mark != Balise1_id):
                #time.sleep(10)
                #if isImageSameValue(value):
                    Balise2_coord = Coord_Relative_To_Coord_Absolue(value[id_mark]["Dist"], value[id_mark]["Angle"])
                    Balise2_id = id_mark
                    print(Balise2_coord)
                    return 1
        tourner(45)
        time.sleep(0.2)


points = np.array([(x, y) for x in range(0, 200, 50) for y in range(0, 350, 50)])

def point_le_plus_proche(x, y):
    # Convertir le point d'entrée en tableau NumPy
    point = np.array([x, y])

    # Calculer les distances euclidiennes entre (x, y) et tous les points de la grille
    distances = np.linalg.norm(points - point, axis=1)

    # Trouver l'index de la distance minimale
    index_min = np.argmin(distances)

    # Retourner le point correspondant
    return tuple(points[index_min])

# Va à la case de coordonnée (x,y) depuis sa position actuelle
def AllerA(x: float, y: float):
    xrobot, yrobot, orient = get_robot_coord()
    ydiff = y-yrobot
    xdiff = xrobot-x
    if (ydiff == 0):
        if (xdiff > 0):
            tourner(90)
        else:
            tourner(-90)
    else:
        if (ydiff < 0):
            tourner(180+(np.arctan((xdiff/ydiff) - (orient*np.pi/180))))
        else:
            tourner(np.arctan((xdiff/ydiff) - (orient*np.pi/180)))
    avancer(np.sqrt([(ydiff * ydiff) + (xdiff * xdiff)])[0])

# Tourne pour s'orienter vers la position de coordonnée (x,y)
def TournerA(x: float, y: float):
    xrobot, yrobot, orient = get_robot_coord()
    ydiff = y-yrobot
    xdiff = xrobot-x
    if (ydiff == 0):
        if (xdiff > 0):
            tourner(90)
        else:
            tourner(-90)
    else:
        if (ydiff < 0):
            tourner(180+(np.arctan((xdiff/ydiff) - (orient*np.pi/180))))
        else:
            tourner(np.arctan((xdiff/ydiff) - (orient*np.pi/180)))

def trier_tab(tableau_points, point_reference):
    # Convertir le tableau de couples en un tableau NumPy
    points = np.array(tableau_points)
    # Convertir le couple de référence en un tableau NumPy
    ref_point = np.array(point_reference)
    # Calculer les distances euclidiennes entre chaque point du tableau et le point de référence
    distances = np.linalg.norm(points - ref_point, axis=1)
    # Obtenir les indices triés selon la distance
    indices_triees = np.argsort(distances)
    # Récupérer le tableau trié selon les indices
    points_tries = points[indices_triees]
    # Inverser les deux derniers éléments du tableau trié
    if len(points_tries) > 1:
        points_tries[-2], points_tries[-1] = points_tries[-1].copy(), points_tries[-2].copy()
    return points_tries

def CoordToCase(x: float, y: float):
    print(f'from {x},{y} to {(np.floor(x/50) + 1, np.floor(y/50) + 1)}')
    return (np.floor(x/50) + 1, np.floor(y/50) + 1)

def CaseToCoord(x: int, y: int):
    print(f'from {x},{y} to {((x-1)*50+25, (y-1)*50+25)}')
    return ((x-1)*50+25, (y-1)*50+25)

# Fonction implémentant la stratégie adoptée pour l'évaluation intermédiaire
def strategy_4 () :
    global Balise1_coord
    global Balise1_id
    global Balise1_found
    global Balise2_coord
    global Balise2_id
    global Balise2_found
    avancer(150)
    print("je viens d'avancer de 150 !")
    cherche_balise_ret()
    print("Balise détecté !")
    for _ in range(2):
        liste = []
        # Calcul des positions où peut se trouver la face de la balise voulue 
        pointbalisex, pointbalisey = point_le_plus_proche(Balise1_coord[0], Balise1_coord[1])
        xtemp, ytemp = CoordToCase(pointbalisex+1, pointbalisey+1)
        xtemp, ytemp = CaseToCoord(xtemp, ytemp)
        liste.append( (xtemp, ytemp) )
        xtemp, ytemp = CoordToCase(pointbalisex+1, pointbalisey-1)
        xtemp, ytemp = CaseToCoord(xtemp, ytemp)
        liste.append( (xtemp, ytemp) )
        xtemp, ytemp = CoordToCase(pointbalisex-1, pointbalisey-1)
        xtemp, ytemp = CaseToCoord(xtemp, ytemp)
        liste.append( (xtemp, ytemp) )
        xtemp, ytemp = CoordToCase(pointbalisex-1, pointbalisey+1)
        xtemp, ytemp = CaseToCoord(xtemp, ytemp)
        liste.append( (xtemp, ytemp) )
        xtemp, ytemp, _ = get_robot_coord()
        liste = trier_tab(liste, (xtemp,ytemp))
        print(liste)
        # Le robot essaie d'aller sur la bonne case pour récupérer la balise
        for x, y in liste:
            xtest, ytest = CoordToCase(x, y)
            if (xtest in [1,2,3]) and (ytest in [1,2,3,4,5,6]):
                if not Balise1_found:
                    AllerA(x, y)
                    print(f"case {x}{y} atteinte")
                    TournerA(pointbalisex, pointbalisey)
                    vs.grab()
                    _, frame = vs.read()
                    value = cam.detection(marker_points2,marker_points10,arucoDetector,cam_param,frame)
                    for id_mark in value.keys():
                        if (id_mark == Balise1_id):
                            Balise1_found = True
        if not Balise1_found:
            print("Balise non atteinte")
        else:
            print("Balise trouvée !")
            emote(Balise1_id)
        cherche_balise_222()
        print("Balise détectée !")
    process.terminate()
    # Arrêter une course
    requests.post(url, "/api/stop")

def strategie_ep_finale():
    # Demander au serveur quoi faire -> Reçoit position et orientation
    pass

if __name__ == "__main__":
    strategy_4()