class Robot:
    def __init__(self):
        self.position = 0

    def avancer(self):
        self.position += 1
        print(f"Le robot avance à la position {self.position}")

    def tourner_360(self):
        print("Le robot tourne de 360 degrés")

    def parcourir_colonne(self, cases):
        for _ in range(cases):
            self.avancer()
            self.tourner_360()

if __name__ == "__main__":
    robot = Robot()
    robot.parcourir_colonne(6)