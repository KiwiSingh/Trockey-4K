import time
import pyglet #type: ignore
from turtle import Screen, Turtle
from controller import Controller
from paddle import Paddle
from puck import Puck
from player_selector import run_setup_menu
from scoreboard import Scoreboard
from sound_manager import SoundManager, resource_path
from languages import STRINGS #type: ignore

# --- FONT LOADING ---
try:
    pyglet.font.add_file(resource_path('NotoSansJP-Regular.ttf'))
    pyglet.font.add_file(resource_path('NotoSansDevanagari-Regular.ttf'))
except Exception as e:
    print(f"Custom fonts not loaded, using system defaults: {e}")

# --- SCREEN SETUP & AUTO-SCALING ---
screen = Screen()
screen.setup(width=1.0, height=1.0)
screen.setworldcoordinates(-1920, -1080, 1920, 1080)

current_message = ""
message_clear_time = 0
messenger = None

# We pass the active language to this function now
def show_message(text, active_lang, duration=2.0):
    global current_message, message_clear_time, messenger
    if current_message != text:
        messenger.clear()
        
        # Use appropriate font fallback based on language
        font_name = "Courier"
        if active_lang == "ja": font_name = "Noto Sans JP"
        elif active_lang == "hi": font_name = "Noto Sans Devanagari"
            
        messenger.write(text, align="center", font=(font_name, 64, "bold"))
        current_message = text
    message_clear_time = time.time() + duration

def is_touching(x1, y1, w1, h1, x2, y2, w2, h2):
    return abs(x1 - x2) < (w1 + w2) and abs(y1 - y2) < (h1 + h2)

def handle_puck_collision(puck, paddle, pad_w, pad_h, player_name, snd_mgr):
    pad_x = paddle.xcor()
    pad_y = paddle.ycor()
    dx = puck.xcor() - pad_x
    dy = puck.ycor() - pad_y

    intersect_x = (50 + pad_w) - abs(dx)
    intersect_y = (50 + pad_h) - abs(dy)

    if intersect_x > 0 and intersect_y > 0:
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

# ==========================================
# MAIN ARCADE LOOP
# ==========================================
while True:
    screen.clear()
    screen.bgcolor("black")
    screen.title("Trockey 4K (Auto-Scaled)")
    screen.tracer(0)

    current_message = ""
    message_clear_time = 0

    human_config, human_order, LANG = run_setup_menu(screen)

    sound_manager = SoundManager()
    sound_manager.start_bgm()

    l_paddle = Paddle((-1000, 0), (24, 4), x_bounds=(-1880, 0), y_bounds=(-1040, 1040))
    r_paddle = Paddle((1000, 0), (24, 4), x_bounds=(0, 1880), y_bounds=(-1040, 1040))
    t_paddle = Paddle((0, 1000), (4, 24), x_bounds=(-1880, 1880), y_bounds=(0, 1040))
    puck = Puck()

    l_paddle.is_ai = not human_config["left"]
    r_paddle.is_ai = not human_config["right"]
    t_paddle.is_ai = not human_config["top"]

    active_controllers = {}
    for index, position in enumerate(human_order):
        try:
            active_controllers[position] = Controller(joystick_id=index)
        except Exception:
            pass

    messenger = Turtle()
    messenger.hideturtle()
    messenger.penup()
    messenger.color("yellow")
    messenger.goto(0, 300)

    screen.listen()

    screen.onkeypress(l_paddle.go_up, "w")
    screen.onkeypress(l_paddle.go_down, "s")
    screen.onkeypress(l_paddle.go_left, "a")
    screen.onkeypress(l_paddle.go_right, "d")

    screen.onkeypress(r_paddle.go_up, "Up")
    screen.onkeypress(r_paddle.go_down, "Down")
    screen.onkeypress(r_paddle.go_left, "Left")
    screen.onkeypress(r_paddle.go_right, "Right")

    screen.onkeypress(t_paddle.go_up, "i")
    screen.onkeypress(t_paddle.go_down, "k")
    screen.onkeypress(t_paddle.go_left, "j")
    screen.onkeypress(t_paddle.go_right, "l")

    scores = {"left": 0, "right": 0, "top": 0}
    scoreboard = Scoreboard()
    winning_score = 10 

    game_is_on = True
    while game_is_on:
        time.sleep(puck.move_speed)
        screen.update()
        current_time = time.time()
        puck.move()

        if not l_paddle.is_ai:
            if "left" in active_controllers: active_controllers["left"].update(l_paddle)
        elif l_paddle.is_active:
            l_paddle.ai_track_unhinged(puck)

        if not r_paddle.is_ai:
            if "right" in active_controllers: active_controllers["right"].update(r_paddle)
        elif r_paddle.is_active:
            r_paddle.ai_track_unhinged(puck)

        if not t_paddle.is_ai:
            if "top" in active_controllers: active_controllers["top"].update(t_paddle)
        elif t_paddle.is_active:
            t_paddle.ai_track_unhinged(puck)

        if current_time > message_clear_time and current_message != "":
            messenger.clear()
            current_message = ""

        px, py = puck.xcor(), puck.ycor()
        lx, ly = l_paddle.xcor(), l_paddle.ycor()
        rx, ry = r_paddle.xcor(), r_paddle.ycor()
        tx, ty = t_paddle.xcor(), t_paddle.ycor()

        # --- FOULS (PERMA-FREEZE) ---
        l_r_foul = is_touching(lx, ly, 40, 240, rx, ry, 40, 240)
        l_t_foul = is_touching(lx, ly, 40, 240, tx, ty, 240, 40)
        r_t_foul = is_touching(rx, ry, 40, 240, tx, ty, 240, 40)
        foul_occurred = False

        if l_r_foul and r_t_foul and l_t_foul:
            show_message(STRINGS[LANG]["grand_bash"], LANG, 2.0)
            scores["left"] = max(0, scores["left"] - 1)
            scores["right"] = max(0, scores["right"] - 1)
            scores["top"] = max(0, scores["top"] - 1)
            scoreboard.update_scores(scores)
            
            l_paddle.freeze()
            r_paddle.freeze()
            t_paddle.freeze()
            foul_occurred = True

        elif l_r_foul:
            show_message(STRINGS[LANG]["foul_lr"], LANG, 2.0)
            l_paddle.freeze()
            r_paddle.freeze()
            foul_occurred = True

        elif l_t_foul:
            show_message(STRINGS[LANG]["foul_lt"], LANG, 2.0)
            l_paddle.freeze()
            t_paddle.freeze()
            foul_occurred = True

        elif r_t_foul:
            show_message(STRINGS[LANG]["foul_rt"], LANG, 2.0)
            r_paddle.freeze()
            t_paddle.freeze()
            foul_occurred = True

        if foul_occurred:
            sound_manager.play_paddle_bounce() 
            sound_manager.play_freeze()        
            
            l_paddle.goto(-1000, 0)
            r_paddle.goto(1000, 0)
            t_paddle.goto(0, 1000)
            puck.reset_position()
            screen.update()
            time.sleep(1.5)
            continue 

        # --- COLLISIONS ---
        if not handle_puck_collision(puck, l_paddle, 40, 240, "left", sound_manager):
            if not handle_puck_collision(puck, r_paddle, 40, 240, "right", sound_manager):
                handle_puck_collision(puck, t_paddle, 240, 40, "top", sound_manager)

        # --- SCORING & GHOST PUCK ---
        goal_side = None

        if puck.xcor() < -1060:
            goal_side = "left"
        elif puck.xcor() > 1060:
            goal_side = "right"
        elif puck.ycor() > 1060:
            goal_side = "top"
        elif puck.ycor() < -1060:
            puck.bounce_y()
            sound_manager.play_wall_bounce()

        if goal_side:
            if puck.last_hitter is None:
                if goal_side == "left":
                    scores["top"] += 1
                    scores["right"] += 1
                    show_message(STRINGS[LANG]["ghost_tr"], LANG, 2.0)
                elif goal_side == "right":
                    scores["top"] += 1
                    scores["left"] += 1
                    show_message(STRINGS[LANG]["ghost_tl"], LANG, 2.0)
                elif goal_side == "top":
                    scores["left"] += 1
                    scores["right"] += 1
                    show_message(STRINGS[LANG]["ghost_lr"], LANG, 2.0)
            else:
                if goal_side == "left":
                    if puck.last_hitter == "top":
                        scores["top"] += 1
                        show_message(STRINGS[LANG]["score_t"], LANG, 2.0)
                    elif puck.last_hitter == "right":
                        scores["right"] += 1
                        show_message(STRINGS[LANG]["score_r"], LANG, 2.0)
                    elif puck.last_hitter == "left":
                        scores["top"] += 1
                        scores["right"] += 1
                        show_message(STRINGS[LANG]["own_tr"], LANG, 2.0)

                elif goal_side == "right":
                    if puck.last_hitter == "top":
                        scores["top"] += 1
                        show_message(STRINGS[LANG]["score_t"], LANG, 2.0)
                    elif puck.last_hitter == "left":
                        scores["left"] += 1
                        show_message(STRINGS[LANG]["score_l"], LANG, 2.0)
                    elif puck.last_hitter == "right":
                        scores["top"] += 1
                        scores["left"] += 1
                        show_message(STRINGS[LANG]["own_tl"], LANG, 2.0)

                elif goal_side == "top":
                    if puck.last_hitter == "left":
                        scores["left"] += 1
                        show_message(STRINGS[LANG]["score_l"], LANG, 2.0)
                    elif puck.last_hitter == "right":
                        scores["right"] += 1
                        show_message(STRINGS[LANG]["score_r"], LANG, 2.0)
                    elif puck.last_hitter == "top":
                        scores["left"] += 1
                        scores["right"] += 1
                        show_message(STRINGS[LANG]["own_lr"], LANG, 2.0)

            scoreboard.update_scores(scores)
            
            # UNFREEZE EVERYONE AFTER A GOAL
            l_paddle.unfreeze()
            r_paddle.unfreeze()
            t_paddle.unfreeze()
            
            winners = [side.upper() for side, score in scores.items() if score >= winning_score]
            
            if winners:
                if len(winners) > 1:
                    show_message(STRINGS[LANG]["tie_break"].format(winning_score + 1), LANG, 3.0)
                    winning_score += 1
                    puck.reset_position()
                    screen.update()
                    time.sleep(1.5)
                    continue
                else:
                    sound_manager.stop_bgm() 
                    show_message(STRINGS[LANG]["match_over"].format(winners[0]), LANG, 5.0)
                    screen.update()
                    time.sleep(4.0) 
                    game_is_on = False
                    continue

            puck.reset_position()
            screen.update()
            time.sleep(1.5)