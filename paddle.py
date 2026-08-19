from turtle import Turtle
import random

class Paddle(Turtle):
    def __init__(self, position, stretch_len, x_bounds, y_bounds):
        super().__init__()
        self.shape("square")
        self.color("white")
        # FIX: Mapped correctly so vertical/horizontal paddles render as intended!
        self.shapesize(stretch_wid=stretch_len[0], stretch_len=stretch_len[1])
        self.penup()
        self.goto(position)
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.is_active = True
        self.is_ai = False
        self.move_speed = 20

    # Analog movement methods for the DualSense controller
    def move_y(self, amount):
        if self.is_active:
            new_y = self.ycor() + amount
            new_y = max(self.y_bounds[0], min(self.y_bounds[1], new_y))
            self.goto(self.xcor(), new_y)

    def move_x(self, amount):
        if self.is_active:
            new_x = self.xcor() + amount
            new_x = max(self.x_bounds[0], min(self.x_bounds[1], new_x))
            self.goto(new_x, self.ycor())

    # Keyboard movement wrappers
    def go_up(self):
        self.move_y(self.move_speed)

    def go_down(self):
        self.move_y(-self.move_speed)

    def go_left(self):
        self.move_x(-self.move_speed)

    def go_right(self):
        self.move_x(self.move_speed)

    def freeze(self):
        self.is_active = False
        self.color("blue")

    def unfreeze(self):
        self.is_active = True
        self.color("white")

    def ai_track_unhinged(self, puck, primary_axis):
        if not self.is_active:
            return
            
        move_x = False
        move_y = False
        
        # 100% chance to track their main defensive line, 15% chance to aggressively drift
        if primary_axis == "y":
            move_y = True
            move_x = random.random() < 0.15
        else:
            move_x = True
            move_y = random.random() < 0.15
            
        if move_x:
            if self.xcor() < puck.xcor() - 10:
                self.go_right()
            elif self.xcor() > puck.xcor() + 10:
                self.go_left()
                
        if move_y:
            if self.ycor() < puck.ycor() - 10:
                self.go_up()
            elif self.ycor() > puck.ycor() + 10:
                self.go_down()