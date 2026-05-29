import subprocess
import time

class RobotControl:
    def __init__(self):
        self.process = None

    def avancer(self, distance: int, vitesse: int, bloquante: bool):
        if distance < 0:
            self.process = subprocess.Popen(['python3', '/home/go4t/team5/Motors/Motors_func/backward_motors.py', str(distance), str(-vitesse)])
        else:
            self.process = subprocess.Popen(['python3', '/home/go4t/team5/Motors/Motors_func/forward_motors.py', str(distance), str(vitesse)])
        if bloquante:
            self.process.wait()
            time.sleep(0.1)

    def tourner(self, angle: float, vitesse: int, bloquante: bool):
        if angle < 0:
            self.process = subprocess.Popen(['python3', '/home/go4t/team5/Motors/Motors_func/rotate_left_motors.py', str(angle), str(vitesse)])
        else:
            self.process = subprocess.Popen(['python3', '/home/go4t/team5/Motors/Motors_func/rotate_right_motors.py', str(angle), str(vitesse)])
        if bloquante:
            self.process.wait()
            time.sleep(0.1)

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            return 0
        else:
            return 1
        time.sleep(0.1)
