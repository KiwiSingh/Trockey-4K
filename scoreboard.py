from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        # Park it at the bottom of the screen
        self.goto(0, -1000)
        self.update_scores({"left": 0, "right": 0, "top": 0})

    def update_scores(self, scores):
        self.clear()
        # Format the text so it's neatly spaced out
        score_text = f"LEFT: {scores['left']}    TOP: {scores['top']}    RIGHT: {scores['right']}"
        self.write(score_text, align="center", font=("Courier", 54, "bold"))