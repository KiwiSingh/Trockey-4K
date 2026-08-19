from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position, stretch_factor, x_bounds, y_bounds):
        super().__init__()
        self.shape("square")
        self.shapesize(*stretch_factor)
        self.color("white")
        self.penup()
        self.goto(position)

        self.is_active = True
        self.is_ai = False

        # Store the specific screen boundaries for this paddle
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds

    def freeze(self):
        self.is_active = False
        self.color("cyan")  # Turns blue so you visually KNOW you are frozen!

    def unfreeze(self):
        self.is_active = True
        self.color("white")

    def move_x(self, amount):
        if not self.is_active:
            return
        new_x = self.xcor() + amount
        new_x = max(self.x_bounds[0], min(new_x, self.x_bounds[1]))
        self.setx(new_x)

    def move_y(self, amount):
        if not self.is_active:
            return
        new_y = self.ycor() + amount
        new_y = max(self.y_bounds[0], min(new_y, self.y_bounds[1]))
        self.sety(new_y)

    def ai_track(self, puck, axis):
        if not self.is_active or not self.is_ai:
            return

        ai_speed = 15

        if axis == "y":
            if self.ycor() < puck.ycor() - 10:
                self.move_y(ai_speed)
            elif self.ycor() > puck.ycor() + 10:
                self.move_y(-ai_speed)

        elif axis == "x":
            if self.xcor() < puck.xcor() - 10:
                self.move_x(ai_speed)
            elif self.xcor() > puck.xcor() + 10:
                self.move_x(-ai_speed)

    # --- KEYBOARD LOCKS ---
    def go_up(self):
        if self.is_active:
            self.move_y(72)

    def go_down(self):
        if self.is_active:
            self.move_y(-72)

    def go_right(self):
        if self.is_active:
            self.move_x(72)

    def go_left(self):
        if self.is_active:
            self.move_x(-72)