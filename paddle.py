from turtle import Turtle
import random

class Paddle(Turtle):
    def __init__(self, position, stretch_len, x_bounds, y_bounds):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=stretch_len[1], stretch_len=stretch_len[0])
        self.penup()
        self.goto(position)
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.is_active = True
        self.is_ai = False
        self.move_speed = 20

    def go_up(self):
        if self.is_active and self.ycor() + self.move_speed <= self.y_bounds[1]:
            new_y = self.ycor() + self.move_speed
            self.goto(self.xcor(), new_y)

    def go_down(self):
        if self.is_active and self.ycor() - self.move_speed >= self.y_bounds[0]:
            new_y = self.ycor() - self.move_speed
            self.goto(self.xcor(), new_y)

    def go_left(self):
        if self.is_active and self.xcor() - self.move_speed >= self.x_bounds[0]:
            new_x = self.xcor() - self.move_speed
            self.goto(new_x, self.ycor())

    def go_right(self):
        if self.is_active and self.xcor() + self.move_speed <= self.x_bounds[1]:
            new_x = self.xcor() + self.move_speed
            self.goto(new_x, self.ycor())

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