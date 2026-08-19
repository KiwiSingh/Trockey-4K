import time
from turtle import Screen, Turtle
from controller import Controller
from paddle import Paddle
from puck import Puck
from player_selector import run_setup_menu
from scoreboard import Scoreboard
from sound_manager import SoundManager

screen = Screen()
screen.setup(width=3840, height=2160)
screen.bgcolor("black")
screen.title("Trockey 4K")
screen.tracer(0)

# 1. Run the visual menu before spawning the objects
human_config = run_setup_menu(screen)

# 2. Start the Audio Engine and loop the BGM!
sound_manager = SoundManager()
sound_manager.start_bgm()

# 3. Set positions, stretch factors, and territorial boundaries
l_paddle = Paddle((-1000, 0), (24, 4), x_bounds=(-1880, 0), y_bounds=(-1040, 1040))
r_paddle = Paddle((1000, 0), (24, 4), x_bounds=(0, 1880), y_bounds=(-1040, 1040))
t_paddle = Paddle((0, 1000), (4, 24), x_bounds=(-1880, 1880), y_bounds=(0, 1040))
puck = Puck()

# 4. Assign AI flags based on the menu configuration
l_paddle.is_ai = not human_config["left"]
r_paddle.is_ai = not human_config["right"]
t_paddle.is_ai = not human_config["top"]

# 5. Initialize three separate controllers
l_controller = Controller(joystick_id=0)
r_controller = Controller(joystick_id=1)
t_controller = Controller(joystick_id=2)

# --- Ephemeral Text Setup ---
messenger = Turtle()
messenger.hideturtle()
messenger.penup()
messenger.color("yellow")
messenger.goto(0, 300)

current_message = ""
message_clear_time = 0


def show_message(text, duration=2.0):
    global current_message, message_clear_time
    if current_message != text:
        messenger.clear()
        messenger.write(text, align="center", font=("Courier", 64, "bold"))
        current_message = text
    message_clear_time = time.time() + duration


# --- Collision Math ---
def is_touching(x1, y1, w1, h1, x2, y2, w2, h2):
    return abs(x1 - x2) < (w1 + w2) and abs(y1 - y2) < (h1 + h2)


# Pass the sound_manager in so it can trigger the SFX
def handle_puck_collision(puck, paddle, pad_w, pad_h, player_name, snd_mgr):
    pad_x = paddle.xcor()
    pad_y = paddle.ycor()
    dx = puck.xcor() - pad_x
    dy = puck.ycor() - pad_y

    intersect_x = (50 + pad_w) - abs(dx)
    intersect_y = (50 + pad_h) - abs(dy)

    if intersect_x > 0 and intersect_y > 0:

        # Trigger the paddle bounce sound!
        snd_mgr.play_paddle_bounce()

        if paddle.is_active:
            puck.last_hitter = player_name
        else:
            puck.last_hitter = None

        if intersect_x < intersect_y:
            if dx > 0:
                puck.x_move = abs(puck.x_move)
                puck.setx(pad_x + pad_w + 50)
            else:
                puck.x_move = -abs(puck.x_move)
                puck.setx(pad_x - pad_w - 50)
        else:
            if dy > 0:
                puck.y_move = abs(puck.y_move)
                puck.sety(pad_y + pad_h + 50)
            else:
                puck.y_move = -abs(puck.y_move)
                puck.sety(pad_y - pad_h - 50)

        puck.move_speed *= 0.9
        puck.move_speed = max(0.005, puck.move_speed)

        return True
    return False


screen.listen()

# Map the Left paddle to WASD
screen.onkeypress(l_paddle.go_up, "w")
screen.onkeypress(l_paddle.go_down, "s")
screen.onkeypress(l_paddle.go_left, "a")
screen.onkeypress(l_paddle.go_right, "d")

# Map the Right paddle to Arrow Keys
screen.onkeypress(r_paddle.go_up, "Up")
screen.onkeypress(r_paddle.go_down, "Down")
screen.onkeypress(r_paddle.go_left, "Left")
screen.onkeypress(r_paddle.go_right, "Right")

# Map the Top paddle to IJKL
screen.onkeypress(t_paddle.go_up, "i")
screen.onkeypress(t_paddle.go_down, "k")
screen.onkeypress(t_paddle.go_left, "j")
screen.onkeypress(t_paddle.go_right, "l")

# Score Tracker & Foul Timers
scores = {"left": 0, "right": 0, "top": 0}
scoreboard = Scoreboard()

unfreeze_time = {"left": 0, "right": 0, "top": 0}

# Main Game Loop
game_is_on = True
while game_is_on:
    time.sleep(puck.move_speed)
    screen.update()

    # Check if frozen paddles are ready to thaw out
    current_time = time.time()
    if not l_paddle.is_active and current_time > unfreeze_time["left"]:
        l_paddle.unfreeze()
    if not r_paddle.is_active and current_time > unfreeze_time["right"]:
        r_paddle.unfreeze()
    if not t_paddle.is_active and current_time > unfreeze_time["top"]:
        t_paddle.unfreeze()

    puck.move()

    # --- INPUT / AI LOGIC ---
    if not l_paddle.is_ai:
        l_controller.update(l_paddle)
    else:
        l_paddle.ai_track(puck, "y")

    if not r_paddle.is_ai:
        r_controller.update(r_paddle)
    else:
        r_paddle.ai_track(puck, "y")

    if not t_paddle.is_ai:
        t_controller.update(t_paddle)
    else:
        t_paddle.ai_track(puck, "x")

    # Clear ephemeral text if time has expired
    if current_time > message_clear_time and current_message != "":
        messenger.clear()
        current_message = ""

    px, py = puck.xcor(), puck.ycor()
    lx, ly = l_paddle.xcor(), l_paddle.ycor()
    rx, ry = r_paddle.xcor(), r_paddle.ycor()
    tx, ty = t_paddle.xcor(), t_paddle.ycor()

    # ----------------------------------------------------
    # FOUL SYSTEM FRAMEWORK
    # ----------------------------------------------------
    l_r_foul = is_touching(lx, ly, 40, 240, rx, ry, 40, 240)
    l_t_foul = is_touching(lx, ly, 40, 240, tx, ty, 240, 40)
    r_t_foul = is_touching(rx, ry, 40, 240, tx, ty, 240, 40)

    foul_occurred = False

    if l_r_foul and r_t_foul and l_t_foul:
        show_message("MEGA FOUL! -1 Point All Around", 2.0)
        scores["left"] -= 1
        scores["right"] -= 1
        scores["top"] -= 1
        scoreboard.update_scores(scores)

        l_paddle.freeze()
        r_paddle.freeze()
        t_paddle.freeze()
        unfreeze_time["left"] = current_time + 5.0
        unfreeze_time["right"] = current_time + 5.0
        unfreeze_time["top"] = current_time + 5.0
        foul_occurred = True

    elif l_r_foul:
        show_message("FOUL: Left & Right. Top gets free shot!", 2.0)
        l_paddle.freeze()
        r_paddle.freeze()
        unfreeze_time["left"] = current_time + 5.0
        unfreeze_time["right"] = current_time + 5.0
        foul_occurred = True

    elif l_t_foul:
        show_message("FOUL: Left & Top. Right gets free shot!", 2.0)
        l_paddle.freeze()
        t_paddle.freeze()
        unfreeze_time["left"] = current_time + 5.0
        unfreeze_time["top"] = current_time + 5.0
        foul_occurred = True

    elif r_t_foul:
        show_message("FOUL: Right & Top. Left gets free shot!", 2.0)
        r_paddle.freeze()
        t_paddle.freeze()
        unfreeze_time["right"] = current_time + 5.0
        unfreeze_time["top"] = current_time + 5.0
        foul_occurred = True

    if foul_occurred:
        sound_manager.play_paddle_bounce()
        sound_manager.play_freeze()  # Trigger the ice freeze sound!
        l_paddle.goto(-1000, 0)
        r_paddle.goto(1000, 0)
        t_paddle.goto(0, 1000)
        puck.reset_position()
        screen.update()
        time.sleep(1.5)
        continue

        # ----------------------------------------------------
    # PUCK TO PADDLE COLLISIONS
    # ----------------------------------------------------
    if not handle_puck_collision(puck, l_paddle, 40, 240, "left", sound_manager):
        if not handle_puck_collision(puck, r_paddle, 40, 240, "right", sound_manager):
            handle_puck_collision(puck, t_paddle, 240, 40, "top", sound_manager)

    # ----------------------------------------------------
    # SCORING & WALL BOUNDARIES
    # ----------------------------------------------------
    goal_side = None

    if puck.xcor() < -1060:
        goal_side = "left"
    elif puck.xcor() > 1060:
        goal_side = "right"
    elif puck.ycor() > 1060:
        goal_side = "top"
    elif puck.ycor() < -1060:
        puck.bounce_y()
        sound_manager.play_wall_bounce()  # Trigger the wall bounce sound!

    if goal_side:
        if puck.last_hitter is None:
            show_message("Dead Puck! No points.", 2.0)
        else:
            if goal_side == "left":
                if puck.last_hitter == "top":
                    scores["top"] += 1
                    show_message("Top scored!", 2.0)
                elif puck.last_hitter == "right":
                    scores["right"] += 1
                    show_message("Right scored!", 2.0)
                elif puck.last_hitter == "left":
                    scores["top"] += 1
                    scores["right"] += 1
                    show_message("Own Goal! Top & Right score.", 2.0)

            elif goal_side == "right":
                if puck.last_hitter == "top":
                    scores["top"] += 1
                    show_message("Top scored!", 2.0)
                elif puck.last_hitter == "left":
                    scores["left"] += 1
                    show_message("Left scored!", 2.0)
                elif puck.last_hitter == "right":
                    scores["top"] += 1
                    scores["left"] += 1
                    show_message("Own Goal! Top & Left score.", 2.0)

            elif goal_side == "top":
                if puck.last_hitter == "left":
                    scores["left"] += 1
                    show_message("Left scored!", 2.0)
                elif puck.last_hitter == "right":
                    scores["right"] += 1
                    show_message("Right scored!", 2.0)
                elif puck.last_hitter == "top":
                    scores["left"] += 1
                    scores["right"] += 1
                    show_message("Own Goal! Left & Right score.", 2.0)

        scoreboard.update_scores(scores)

        # --- WIN CONDITION CHECK ---
        winners = [side.upper() for side, score in scores.items() if score >= 10]

        if winners:
            sound_manager.stop_bgm()  # Kill the background music!
            if len(winners) > 1:
                show_message(f"TIE BREAK! {' & '.join(winners)} WIN!", 5.0)
            else:
                show_message(f"MATCH OVER! {winners[0]} WINS!", 5.0)

            screen.update()
            game_is_on = False
            continue

        puck.reset_position()
        screen.update()
        time.sleep(1.5)

screen.exitonclick()