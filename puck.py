import random
from turtle import Turtle


class Puck(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.shapesize(stretch_wid=5, stretch_len=5)
        self.penup()

        self.last_hitter = None
        self.reset_position()
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1
        self.move_speed *= 0.9

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 0.9

    def reset_position(self):
        self.move_speed = 0.1
        self.goto(0, 0)
        self.last_hitter = None

        # Randomize the serve speed and angle so it doesn't shoot perfectly into the corners
        # Keeping Y speeds slightly lower than X favors hitting the side paddles first
        self.x_move = random.choice([30, 35, 40]) * random.choice([1, -1])
        self.y_move = random.choice([15, 20, 25]) * random.choice([1, -1])