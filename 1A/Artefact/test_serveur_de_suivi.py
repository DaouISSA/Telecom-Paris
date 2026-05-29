import requests
import sys
url = sys.argv[1]
XVAL = sys.argv[2]
YVAL = sys.argv[3]
MID = sys.argv[4]
MCOL = str(int(XVAL)//50 + 1)
MROW = chr(int(YVAL)//50 + 65)
nb_requetes = 0
# Mise  à jour de position
pos = requests.post(url+"/api/pos?x="+str(XVAL)+"&y="+str(YVAL))
while (pos.status_code != 200 or pos.status_code != 503) and nb_requetes < 20:
    pos = requests.post(url+"/api/pos?x="+str(XVAL)+"&y="+str(YVAL))
    nb_requetes += 1
nb_requetes = 0
# Capture de drapeaux
cap = requests.post(url+"/api/marker?id="+MID+"&col="+MCOL+"&row="+MROW)
while (cap.status_code != 200 or cap.status_code != 503) and nb_requetes < 20:
    cap = requests.post(url+"/api/marker?id="+MID+"&col="+MCOL+"&row="+MROW)
    nb_requetes +=1
    
print(f"Requête envoyé avec les codes {pos} et {cap} !")