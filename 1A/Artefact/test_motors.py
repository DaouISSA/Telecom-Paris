import motors
import time
import sys

commandes = sys.argv[1].split(',')
print(commandes)
robot = motors.RobotControl()
for commande in commandes:
    if commande.startswith('r'):
        print(f'Le robot va avancer de {commande[1:]} !')
        robot.avancer(int(commande[1:]), 50, True)
    elif commande.startswith('a'):
        print(f'Le robot va tourner de {commande[1:]} !')
        robot.tourner(int(commande[1:]), 50, True)
    else:
        print(f'Erreur dans la commande {commande}')
    time.sleep(0.5)

print("Fin des test moteurs")