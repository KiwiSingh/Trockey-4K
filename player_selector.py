import time
from turtle import Turtle


def run_setup_menu(screen):
    menu_pen = Turtle()
    menu_pen.hideturtle()
    menu_pen.penup()
    menu_pen.color("white")

    # By default, assume all paddles are AI. We will flip them to True based on choices.
    config = {"left": False, "right": False, "top": False, "done": False}

    # We use a list for state so we can modify it inside our helper functions
    state = ["count"]

    def draw_text(text):
        menu_pen.clear()
        menu_pen.goto(0, 0)
        menu_pen.write(text, align="center", font=("Courier", 48, "bold"))
        screen.update()

    def set_count(n):
        if state[0] != "count": return

        if n == 0:
            config["done"] = True
        elif n == 3:
            config["left"] = True
            config["right"] = True
            config["top"] = True
            config["done"] = True
        elif n == 1:
            state[0] = "pos1"
            draw_text("1 PLAYER MODE\n\nSelect your position:\nPress (L)eft, (R)ight, or (T)op")
        elif n == 2:
            state[0] = "pos2"
            draw_text(
                "2 PLAYER MODE\n\nSelect human positions:\nPress (1) Left & Right\nPress (2) Left & Top\nPress (3) Right & Top")

    def handle_pos1(pos):
        if state[0] != "pos1": return
        config[pos] = True
        config["done"] = True

    def handle_pos2(choice):
        if state[0] != "pos2": return
        if choice == 1:
            config["left"] = True
            config["right"] = True
        elif choice == 2:
            config["left"] = True
            config["top"] = True
        elif choice == 3:
            config["right"] = True
            config["top"] = True
        config["done"] = True

    screen.listen()

    # Number selection keys
    screen.onkeypress(lambda: set_count(0), "0")
    screen.onkeypress(lambda: set_count(1), "1")
    screen.onkeypress(lambda: set_count(2), "2")
    screen.onkeypress(lambda: set_count(3), "3")

    # Position selection keys (for 1 Player mode)
    screen.onkeypress(lambda: handle_pos1("left"), "l")
    screen.onkeypress(lambda: handle_pos1("right"), "r")
    screen.onkeypress(lambda: handle_pos1("top"), "t")

    # Initial Menu Draw
    draw_text("TROCKEY 4K\n\nHow many human players?\nPress 0, 1, 2, or 3")

    # Halt the rest of the game from loading until a choice is finalized
    while not config["done"]:
        screen.update()
        time.sleep(0.05)

    # --- Cleanup ---
    # Unbind menu keys so they don't interfere with the game controls later
    for key in ["0", "1", "2", "3", "l", "r", "t"]:
        screen.onkeypress(None, key)

    menu_pen.clear()

    return config