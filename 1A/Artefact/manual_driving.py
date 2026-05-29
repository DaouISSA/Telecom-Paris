import controller
import time
import matplotlib.pyplot as plt
import sys

mesure = False
# Définition des variables PID
kp = 2  # Coefficient proportionnel
ki = 15  # Coefficient intégral (désactivé pour l'instant)
kd = 0.0  # Coefficient dérivé (désactivé pour l'instant)
convert = 0.00553
# Variables pour le PID
erreur_gauche = 0
erreur_droite = 0
somme_erreurs_gauche = 0
somme_erreurs_droite = 0
erreur_precedente_gauche = 0
erreur_precedente_droite = 0
commande_gauche = 0
commande_droite = 0
c = controller.Controller()
vitesses_gauche = []
vitesses_droite = []
vitesses_consigne_gauche = []
vitesses_consigne_droite = []
commandes_gauche = []
commandes_droite = []
temps = []
# Constantes
vitesse_consigne_gauche = 1
vitesse_consigne_droite = 1
wait_time = 0.01  # en secondes, pour la boucle PID
commande_max = 70  # Valeur maximale pour la commande moteur
starttime = time.time()
# Fonction de saturation
def limiter_commande(valeur):
    return max(-commande_max, min(commande_max, valeur))
c.set_motor_shutdown_timeout(0.1)
c.get_encoder_ticks()
xl = 0
xd = 0
# Boucle principale PID
#for i in range(2000):
while True:
    time.sleep(wait_time)
    old_vitesse_gauche, old_vitesse_droite = vitesse_consigne_gauche, vitesse_consigne_droite
    with open("/home/go4t/team5/Motors/commande.txt", "r") as file:
        new_vitesse_consigne = file.read().split('\n')
        if (new_vitesse_consigne != [""]):
            vitesse_consigne_gauche = int(new_vitesse_consigne[0])
            vitesse_consigne_droite = int(new_vitesse_consigne[1])

    if (old_vitesse_gauche != 0):
        somme_erreurs_gauche *= vitesse_consigne_gauche/old_vitesse_gauche
    if (old_vitesse_droite != 0):
        somme_erreurs_droite *= vitesse_consigne_droite/old_vitesse_droite
    # Lecture des ticks des encodeurs
    ticks_gauche, ticks_droite = c.get_encoder_ticks()
    if (mesure):
        vitesses_consigne_gauche.append(old_vitesse_gauche)
        vitesses_consigne_droite.append(old_vitesse_droite)
        vitesses_gauche.append((ticks_gauche/wait_time)/80)
        vitesses_droite.append((ticks_droite/wait_time)/80)
        #commandes_gauche.append(limiter_commande(commande_gauche))
        #commandes_droite.append(limiter_commande(commande_droite))
        temps.append(time.time() - starttime)
     # Calcul des erreurs
    erreur_gauche = vitesse_consigne_gauche - ((ticks_gauche/wait_time)/80)
    erreur_droite = vitesse_consigne_droite - ((ticks_droite/wait_time)/80)
    # Calcul de la somme des erreurs pour la partie intégrale
    somme_erreurs_gauche += erreur_gauche * wait_time
    somme_erreurs_droite += erreur_droite * wait_time
    # Calcul de la dérivée de l'erreur
    derivee_erreur_gauche = erreur_gauche - erreur_precedente_gauche
    derivee_erreur_droite = erreur_droite - erreur_precedente_droite

    # PID pour chaque moteur
    commande_gauche = kp * erreur_gauche + ki * somme_erreurs_gauche + kd * derivee_erreur_gauche/wait_time
    commande_droite = kp * erreur_droite + ki * somme_erreurs_droite + kd * derivee_erreur_droite/wait_time

    # Limiter les commandes pour éviter des valeurs trop élevées

    # Appliquer les commandes aux moteurs
    xl += ticks_gauche * convert
    xd += ticks_droite * convert
    #print(round(xl), round(xd), round(xl-xd))
    #c.set_raw_motor_speed(limiter_commande(commande_gauche/4.9), limiter_commande(commande_droite/3.85))
    c.set_raw_motor_speed(limiter_commande(commande_gauche), limiter_commande(commande_droite))
    #c.set_raw_motor_speed(100, 100)
    # Stocker les erreurs précédentes pour la prochaine itération
    erreur_precedente_gauche = erreur_gauche
    erreur_precedente_droite = erreur_droite

if mesure:
    plt.rcParams["figure.figsize"] = (20,6)
    plt.plot(temps, vitesses_gauche, label='Vitesse gauche')
    plt.plot(temps, vitesses_droite, label='Vitesse droite')
    plt.plot(temps, vitesses_consigne_gauche)
    plt.plot(temps, vitesses_consigne_droite)
    #plt.plot(temps, commandes_gauche, label='Commande gauche')
    #plt.plot(temps, commandes_droite, label='Commande droite')
    plt.xlabel('Temps')
    plt.ylabel('Vitesse')
    plt.legend()
    print("try")
    plt.savefig('vitesse_moteurs.png', dpi=400)
    print("done")
