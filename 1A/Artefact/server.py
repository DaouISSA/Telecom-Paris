from flask import Flask, send_from_directory, render_template, request, jsonify
import time
import subprocess
import sys
import signal
import controller

c = controller.Controller()
c.set_motor_shutdown_timeout(0.5)
c.set_pid_coefficients(0.4,0.2,0)
c.standby()
mode_auto = False  # Va permettre de ne rien faire (pas d'envoie de contrôle de robot)

port_nb=sys.argv[1]  # Numero de port donné en argument

process_manual_driving = None
process_main_prog = None
process_go_to_case = None

vitesse_consigne_gauche = 50
vitesse_consigne_droite = 50

def signal_handler(sig, frame):
    if process_main_prog is not None:  # Vérifier si le processus a été lancé
        process_main_prog.terminate()  # Terminer le sous-processus
        process_main_prog.wait()  # Attendre que le sous-processus se termine proprement
        print("Prog main fermé")
    if process_manual_driving is not None:  # Vérifier si le processus a été lancé
        process_manual_driving.terminate()  # Terminer le sous-processus
        process_manual_driving.wait()  # Attendre que le sous-processus se termine proprement
        print("Prog manual_driving fermé")
    if process_go_to_case is not None:
        process_go_to_case.terminate()
        process_go_to_case.wait()
        print("Prog go_to_case fermé")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)  # Permet de fermer les process en fond si ont stop (Ctrl+C) ce serveur

process_manual_driving = None #subprocess.Popen(['python3', '/home/go4t/team5/Motors/manual_driving.py'])

app = Flask(__name__)

# Routes pour servir les pages HTML
@app.route('/')
def home():
    return send_from_directory('/home/go4t/team5/website/', 'home.html')
@app.route('/home.html')
def home2():
    return send_from_directory('/home/go4t/team5/website/', 'home.html')
@app.route('/website/home.html')
def home3():
    return send_from_directory('/home/go4t/team5/website/', 'home.html')
@app.route('/website/go_to_case.html')
def go_to_case_html():
    return send_from_directory('/home/go4t/team5/website/', 'go_to_case.html')

# Routes pour servir les fichiers CSS et JavaScript
@app.route('/website/style.css')
def css():
    return send_from_directory('/home/go4t/team5/website/', 'style.css')

@app.route('/website/script.js')
def js():
    return send_from_directory('/home/go4t/team5/website/', 'script.js')

# Route pour update ce que font les moteurs
@app.route('/control_motor', methods=['POST'])
def control_motor():
    if mode_auto:
        return jsonify('', 300)
    # T'embête pas à tout lire, ça update le fichier commande avec '{vitesse_gauche}\n{vitesse_droite}'
    # Le prog 'manual_driving' qui tourne en fond récupère ces infos en continue
    with open("/home/go4t/team5/Motors/commande.txt", 'w') as file:
        file.write(f"{vitesse_consigne_gauche*request.json.get('forward') + vitesse_consigne_gauche*request.json.get('right') - vitesse_consigne_gauche*request.json.get('backward') - vitesse_consigne_gauche*request.json.get('left')}\n{vitesse_consigne_droite*request.json.get('forward') + vitesse_consigne_droite*request.json.get('left') - vitesse_consigne_droite*request.json.get('backward') - vitesse_consigne_droite*request.json.get('right')}\n")
    return jsonify('', 200)

# Route pour le deuxième mode de contrôle (avec barre)
@app.route('/control_motor_wheel', methods=['POST'])
def control_motor_wheel():
    if mode_auto:
        return jsonify('', 300)
    c.set_motor_speed(request.json.get('left'), request.json.get('right'))
    #with open("/home/go4t/team5/Motors/commande.txt", 'w') as file:
    #    file.write(f"{request.json.get('left')}\n{request.json.get('right')}\n")
    return jsonify('', 200)

# Route pour aller à une case
@app.route('/go_to_case', methods=['POST'])
def go_to_case():
    if mode_auto:
        return jsonify('', 300)
    process_go_to_case = subprocess.Popen(['python3','/home/go4t/team5/Go_to_case.py', f'{request.json.get("case_x")}', f'{request.json.get("case_y")}'])
    process_go_to_case.wait()
    return jsonify('', 200)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=port_nb)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
