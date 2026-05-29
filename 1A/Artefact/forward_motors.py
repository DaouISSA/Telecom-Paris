import controller
import sys
import time
import numpy as np

distance = int(float(sys.argv[1]))
vitesse_consigne = int(float(sys.argv[2]))

c = controller.Controller()
c.set_motor_shutdown_timeout(0.1)
c.standby()
c.set_pid_coefficients(0.4,0.2,0)
c.get_encoder_ticks()
x = 0
y = 0
vitesse = 10
xtot = 0
ytot = 0
x_begin = 0
y_begin = 0
pos = ['']
while pos == ['']:
    with open('/home/go4t/team5/Main_file/update_position.txt', 'r') as file:
        pos = file.read().split(';')
x_begin = float(pos[0])
y_begin = float(pos[1])
orientation = float(pos[2])

def updatePos():
    with open('/home/go4t/team5/Main_file/update_position.txt', 'w') as file:
        file.write(f'{x_begin + xtot*np.sin(orientation*np.pi/180)};{y_begin + ytot*np.cos(-orientation*np.pi/180)};{orientation}')
distance_decer = distance - 20
timestart = time.time()
lasttime = timestart
while (xtot < distance_decer and ytot < distance_decer) and (time.time()-timestart < 20):
    c.set_motor_speed(round(min(vitesse, vitesse_consigne)), round(min(vitesse, vitesse_consigne)))
    x, y = c.get_encoder_ticks()
    xtot += x*0.00553
    ytot += y*0.00553
    vitesse += 0.2
    if (time.time() - lasttime > 1):
        updatePos()
        lasttime = time.time()
    time.sleep(0.01)
if vitesse > vitesse_consigne:
    vitesse = vitesse_consigne
while (xtot < distance and ytot < distance) and (time.time()-timestart < 20):
    c.set_motor_speed(round(max(vitesse, 10)), round(max(vitesse, 10)))
    x, y = c.get_encoder_ticks()
    xtot += x*0.00553
    ytot += y*0.00553
    vitesse -= 0.4
    if (time.time() - lasttime > 1):
        updatePos()
        lasttime = time.time()
    time.sleep(0.01)
c.set_motor_speed(0, 0)
updatePos()
