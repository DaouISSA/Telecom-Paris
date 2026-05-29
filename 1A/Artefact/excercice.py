class Robot:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y

    def move_up(self, distance):
        self.y += distance
        print(f"{self.name} moved up by {distance} units.")

    def move_down(self, distance):
        self.y -= distance
        print(f"{self.name} moved down by {distance} units.")

    def move_left(self, distance):
        self.x -= distance
        print(f"{self.name} moved left by {distance} units.")

    def move_right(self, distance):
        self.x += distance
        print(f"{self.name} moved right by {distance} units.")

    def get_position(self):
        return self.x, self.y

# Example usage
robot = Robot("Robo1")
robot.move_up(5)
robot.move_right(3)
print(f"Current position: {robot.get_position()}")