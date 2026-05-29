from flask import Flask, send_from_directory, render_template, request, jsonify
import time
import subprocess
import sys
import signal

port_nb=sys.argv[1]  # Numero de port donné en argument

process_manual_driving = None
process_main_prog = None

vitesse_consigne_gauche = 70
vitesse_consigne_droite = 70

def signal_handler(sig, frame):
    if process_main_prog is not None:  # Vérifier si le processus a été lancé
        process_main_prog.terminate()  # Terminer le sous-processus
        process_main_prog.wait()  # Attendre que le sous-processus se termine proprement
        print("Prog main fermé")
    if process_manual_driving is not None:  # Vérifier si le processus a été lancé
        print("Prog manual_driving fermé")
        process_manual_driving.terminate()  # Terminer le sous-processus
        process_manual_driving.wait()  # Attendre que le sous-processus se termine proprement
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)  # Permet de fermer les process en fond si ont stop (Ctrl+C) ce serveur

process_manual_driving = subprocess.Popen(['python', '/home/go4t/team5/Main_file/manual_driving.py'])

app = Flask(__name__)

# Route pour servir la page HTML
@app.route('/')
def home():
    return send_from_directory('.', '/home/go4t/team5/website/home.html')
@app.route('/home.html')
def home2():
    return send_from_directory('.', '/home/go4t/team5/website/home.html')

# Routes pour servir les fichiers CSS et JavaScript
@app.route('/website/style.css')
def css():
    return send_from_directory('.', '/home/go4t/team5/website/style.css')

@app.route('/website/script.js')
def js():
    return send_from_directory('.', '/home/go4t/team5/website/script.js')

# Routes pour update ce que font les moteurs
@app.route('/control_motor', methods=['POST'])
def control_motor():
    # T'embête pas à tout lire, ça update le fichier commande avec '{vitesse_gauche}\n{vitesse_droite}'
    # Le prog 'manual_driving' qui tourne en fond récupère ces infos en continue
    with open("/home/go4t/team5/Main_file/commande.txt", 'w') as file:
        file.write(f"{vitesse_consigne_gauche*request.json.get('forward') + vitesse_consigne_gauche*request.json.get('right') - vitesse_consigne_gauche*request.json.get('backward') - vitesse_consigne_gauche*request.json.get('left')}\n{vitesse_consigne_droite*request.json.get('forward') + vitesse_consigne_droite*request.json.get('left') - vitesse_consigne_droite*request.json.get('backward') - vitesse_consigne_droite*request.json.get('right')}\n")
    return jsonify('', 200)

# ...
@app.route('/image', methods=['GET'])
def image():
    return send_from_directory('.', './website/image.png')

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=port_nb)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)