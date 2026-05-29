import cv2
import numpy as np
import requests
import subprocess
import json
import Detection_and_Pos_estimation as cam
import sys
import time
import motors as moteur
import signal

session = requests.Session()

mot = moteur.RobotControl()

def avancer(d):
    mot.avancer(d, 50, True)

def tourner(theta) :
    mot.tourner(theta, 50, True)

marker_points2 = np.array([[-2 / 2, 2 / 2, 0],[2 / 2, 2 / 2, 0],[2 / 2, -2 / 2, 0],[-2 / 2, -2 / 2, 0]], dtype=np.float32)
marker_points10 = np.array([[-10 / 2, 10 / 2, 0],[10 / 2, 10 / 2, 0],[10 / 2, -10 / 2, 0],[-10 / 2, -10 / 2, 0]],dtype=np.float32)
cam_param = np.load('/home/go4t/team5/Calibration/Cam_calib.npz')
ARUCO_DICT = {"DICT_6X6_50": cv2.aruco.DICT_6X6_50}
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT['DICT_6X6_50'])
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_AUTOFOCUS, 0)
vs.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def signal_handler(sig, frame):
    print("Signal reçu, fermeture du processus enfant...")
    if process.poll() is None:  # Si le processus enfant est encore en cours d'exécution
        process.terminate()  # Envoyer un signal SIGTERM pour fermer le processus enfant
        process.wait()  # Attendre que le processus se termine proprement
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def demander_serveur():
    reponse = None
    try:
        reponse = session.get(url, json = "")
        print(reponse)
    except requests.exceptions.RequestException as e:
        print(f"Erreur à la requête :", e)
    if reponse != None and reponse.status_code == 200:
        serveur_reponse = reponse.json()
        print("Réponse : " + str(serveur_reponse) )
        dicT = serveur_reponse
        for key in dicT.keys():
            if key == "avancer" and dicT[key] == True:
                avancer(50)
            if key == "tourner" and dicT[key] != 0:
                tourner(dicT[key])
            if key == "capture" and dicT[key] != 0:
                x = dicT["positionX"] + 1
                y = chr(65 + dicT["positionY"])
                id_balise = dicT["capture"]
                for i in range(10):
                    try:
                        capture = requests.post('http://proj103.r2.enst.fr:80/api/marker?id='+str(id_balise)+'&col='+str(x)+'&row='+y)
                        print(capture)
                    except requests.exceptions.RequestException as e:
                        print(f"Erreur à la requête {i+1} pour la balise {id_balise} dans la case ({x},{y}) :", e)
                    if capture.status_code == 200 or capture.status_code == 503:
                        break
                tourner(360)

def demander_depart():
    response = None
    try:
        response = session.get("http://137.194.173.80:5000/start/5", json = "")
    except requests.exceptions.RequestException as e:
        print(f"Erreur à la requête :", e)
    if response !=None and response.status_code == 400:
        return True
    return False

process = subprocess.Popen(['python3', '/home/go4t/team5/Main_file/pos_update.py'])

if __name__ == "__main__":
    with open('/home/go4t/team5/Main_file/update_position.txt', 'w') as file:
        file.write("225;325;180")
    requests.post("http://proj103.r2.enst.fr:80/api/stop")
    requests.post("http://proj103.r2.enst.fr:80/api/start")
    try:
        url_base = "http://137.194.173.80:5000/robot/5" #url serveur sur campus-telecom
        #url_base = "http://192.168.19.207:5000/robot/5" #url serveur sur mon partage
        id_balise = 0
        url = url_base + "/" + str(id_balise)
        start = False
        while start == False:
            start = demander_depart()
            time.sleep(0.5)
        while True:
            id_balise = 0
            vs.grab()
            _, frame = vs.read()
            #cv2.imwrite('./image_'+str(i)+'.png', frame)
            value = cam.detection(marker_points2,marker_points10,arucoDetector,cam_param,frame)
            closest_id = None
            closest_distance = float('inf')
            max_distance = 50
            for id_mark in value.keys():
                distance = value[id_mark]["Dist"]
                if distance < closest_distance and distance <= max_distance:
                    closest_distance = distance
                    closest_id = id_mark
            if closest_id is not None and closest_id < 40:
                id_balise = closest_id
            else:
                id_balise = 0
            url = url_base + "/" + str(id_balise)
            demander_serveur()
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Si un CTRL+C est reçu pendant une tâche, appeler le gestionnaire de signal
        signal_handler(signal.SIGINT, None)
