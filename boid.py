class Boid:
    def __init__(self, direction: int, position: tuple[int, int], speed: int):
        self.direction: int = direction
        self.position: tuple[int, int] = position
        self.speed: int = speed

    def rotate(self, direction: int):
        self.direction = direction

    def move(self):
        x, y = angle_move_thing(self.position, self.direction, self.speed)
        self.position = int(x), int(y)
