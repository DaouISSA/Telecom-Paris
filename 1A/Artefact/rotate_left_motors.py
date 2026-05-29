import controller
import sys
import time
import motors as moteur

max_time = (-int(float(sys.argv[1]))) / 10
angle = (int(float(sys.argv[1]))*47.3)+50
vitesse_consigne = int(float(sys.argv[2]))
c = controller.Controller()
c.set_motor_shutdown_timeout(0.1)
c.standby()
c.set_pid_coefficients(0.4,0.2,0)
c.get_encoder_ticks()
x = 0
y = 0
vitesse = 3
diff = 0
pos = ['']
while pos == ['']:
    with open('/home/go4t/team5/Main_file/update_position.txt', 'r') as file:
        pos = file.read().split(';')
xbegin = float(pos[0])
ybegin = float(pos[1])
orientation = float(pos[2])
def updatePos():
    with open('/home/go4t/team5/Main_file/update_position.txt', 'w') as file:
        file.write(f'{xbegin};{ybegin};{(orientation+(-diff/47.3))%360}')
angle_decer = angle + 1000
timestart = time.time()
lasttime = timestart
while (diff > angle_decer and time.time()-timestart < max_time):
    c.set_motor_speed(round(max(-vitesse, -vitesse_consigne)), round(min(vitesse, vitesse_consigne)))
    vitesse += 0.2
    if (time.time() - lasttime > 1):
        updatePos()
        lasttime = time.time()
    time.sleep(0.01)
    x, y = c.get_encoder_ticks()
    diff += (x-y)
if vitesse > vitesse_consigne:
    vitesse = vitesse_consigne
while (diff > angle and time.time()-timestart < max_time):
    c.set_motor_speed(round(min(-vitesse,-3)), round(max(vitesse, 3)))
    vitesse -= 0.2
    if (time.time() - lasttime > 1):
        updatePos()
        lasttime = time.time()
    time.sleep(0.01)
    x, y = c.get_encoder_ticks()
    diff += (x-y)
c.set_motor_speed(0, 0)
time.sleep(0.4)
x, y = c.get_encoder_ticks()
diff += (x-y)
updatePos()
if abs(diff-angle+50) > 1:
    mot = moteur.RobotControl()
    mot.tourner((angle-diff)/47.166666, 30, True)
#print(diff)
#print(str(angle-50) + " -> " + str(diff) + " -> " + str(diff-angle+50))

