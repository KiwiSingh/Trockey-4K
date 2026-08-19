import time
from turtle import Turtle
from languages import STRINGS #type: ignore

def run_setup_menu(screen):
    screen.clear()
    screen.bgcolor("black")
    screen.tracer(0)

    drawer = Turtle()
    drawer.hideturtle()
    drawer.color("white")
    drawer.penup()

    menu_state = {
        "step": "LANGUAGE",  
        "lang": "en",
        "num_players": 0,
        "current_player": 1,
        "config": {"left": False, "right": False, "top": False},
        "order": [],
        "available": ["left", "right", "top"]
    }
    
    lang_keys = list(STRINGS.keys())

    def draw_menu():
        drawer.clear()
        drawer.goto(0, 250)
        drawer.color("cyan")
        
        # Default to English title if language isn't picked yet
        title_text = STRINGS[menu_state["lang"]]["setup_title"] if menu_state["step"] != "LANGUAGE" else "TROCKEY 4K SETUP"
        drawer.write(title_text, align="center", font=("Courier", 48, "bold"))
        drawer.color("white")
        
        if menu_state["step"] == "LANGUAGE":
            drawer.goto(0, 150)
            drawer.write("Select Language:", align="center", font=("Courier", 30, "normal"))
            y = 80
            for i, l_code in enumerate(lang_keys):
                drawer.goto(0, y)
                drawer.write(f"Press {i+1} for {STRINGS[l_code]['name']}", align="center", font=("Courier", 24, "normal"))
                y -= 40

        elif menu_state["step"] == "COUNT":
            drawer.goto(0, 0)
            drawer.write(STRINGS[menu_state["lang"]]["how_many"], align="center", font=("Courier", 36, "normal"))
            
        elif menu_state["step"] == "POSITION":
            drawer.goto(0, 50)
            drawer.color("yellow")
            prompt = STRINGS[menu_state["lang"]]["choose_side"].format(menu_state["current_player"])
            drawer.write(prompt, align="center", font=("Courier", 36, "bold"))
            
            drawer.color("white")
            y = -50
            if "left" in menu_state["available"]:
                drawer.goto(0, y)
                drawer.write(STRINGS[menu_state["lang"]]["press_left"], align="center", font=("Courier", 24, "normal"))
            y -= 50
            if "right" in menu_state["available"]:
                drawer.goto(0, y)
                drawer.write(STRINGS[menu_state["lang"]]["press_right"], align="center", font=("Courier", 24, "normal"))
            y -= 50
            if "top" in menu_state["available"]:
                drawer.goto(0, y)
                drawer.write(STRINGS[menu_state["lang"]]["press_top"], align="center", font=("Courier", 24, "normal"))

        elif menu_state["step"] == "DONE":
            drawer.goto(0, 100)
            drawer.color("green")
            drawer.write(STRINGS[menu_state["lang"]]["all_set"], align="center", font=("Courier", 48, "bold"))
            drawer.goto(0, -100)
            drawer.color("yellow")
            drawer.write(STRINGS[menu_state["lang"]]["dropping_puck"], align="center", font=("Courier", 24, "italic"))

        screen.update()

    def handle_key(key):
        if menu_state["step"] == "LANGUAGE":
            try:
                idx = int(key) - 1
                if 0 <= idx < len(lang_keys):
                    menu_state["lang"] = lang_keys[idx]
                    menu_state["step"] = "COUNT"
                    draw_menu()
            except ValueError:
                pass
                
        elif menu_state["step"] == "COUNT":
            if key in ["0", "1", "2", "3"]:
                menu_state["num_players"] = int(key)
                menu_state["step"] = "DONE" if menu_state["num_players"] == 0 else "POSITION"
                draw_menu()
        
        elif menu_state["step"] == "POSITION":
            choice = None
            if key == "1" and "left" in menu_state["available"]: choice = "left"
            elif key == "2" and "right" in menu_state["available"]: choice = "right"
            elif key == "3" and "top" in menu_state["available"]: choice = "top"
            
            if choice:
                menu_state["config"][choice] = True
                menu_state["order"].append(choice)
                menu_state["available"].remove(choice)
                
                if menu_state["current_player"] < menu_state["num_players"]:
                    menu_state["current_player"] += 1
                else:
                    menu_state["step"] = "DONE"
                draw_menu()

    for k in ["0", "1", "2", "3", "4", "5", "6", "7"]:
        screen.onkeypress(lambda k=k: handle_key(k), k)
    
    screen.listen()
    draw_menu()
    
    while menu_state["step"] != "DONE":
        screen.update()
        time.sleep(0.05)
        
    time.sleep(4.0) 
    for k in ["0", "1", "2", "3", "4", "5", "6", "7"]: screen.onkeypress(None, k)
    drawer.clear()
    screen.update()
    
    return menu_state["config"], menu_state["order"], menu_state["lang"]