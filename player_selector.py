import time
from turtle import Turtle
from languages import STRINGS

def run_setup_menu(screen):
    screen.bgcolor("black")
    screen.tracer(0)

    drawer = Turtle()
    drawer.hideturtle()
    drawer.color("white")
    drawer.penup()

    menu_state = {
        "step": "LANGUAGE",  
        "lang": "en",
        "lang_page": 0,
        "num_players": 0,
        "current_player": 1,
        "config": {"left": False, "right": False, "top": False},
        "order": [],
        "available": ["left", "right", "top"]
    }
    
    lang_keys = list(STRINGS.keys())

    def draw_menu():
        drawer.clear()
        drawer.goto(0, 300)
        drawer.color("cyan")
        
        title_text = STRINGS[menu_state["lang"]]["setup_title"] if menu_state["step"] != "LANGUAGE" else "TROCKEY 4K SETUP"
        drawer.write(title_text, align="center", font=("Courier", 48, "bold"))
        drawer.color("white")
        
        if menu_state["step"] == "LANGUAGE":
            drawer.goto(0, 200)
            drawer.write("Select Language / भाषा चुनें:", align="center", font=("Courier", 30, "normal"))
            
            # Pagination logic
            start_idx = menu_state["lang_page"] * 9
            end_idx = min(start_idx + 9, len(lang_keys))
            displayed_keys = lang_keys[start_idx:end_idx]

            y = 120
            for i, l_code in enumerate(displayed_keys):
                drawer.goto(0, y)
                drawer.write(f"Press {i+1} for {STRINGS[l_code]['name']}", align="center", font=("Courier", 22, "normal"))
                y -= 35

            drawer.goto(0, y - 20)
            drawer.color("yellow")
            drawer.write("Press 0 for Next Page", align="center", font=("Courier", 22, "italic"))

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
            if key == "0":
                # Toggle between page 0 and 1
                menu_state["lang_page"] = (menu_state["lang_page"] + 1) % 2
                draw_menu()
            else:
                try:
                    idx_offset = int(key) - 1
                    if 0 <= idx_offset <= 8:
                        actual_idx = (menu_state["lang_page"] * 9) + idx_offset
                        if actual_idx < len(lang_keys):
                            menu_state["lang"] = lang_keys[actual_idx]
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

    for k in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        screen.onkeypress(lambda k=k: handle_key(k), k)
    
    screen.listen()
    draw_menu()
    
    while menu_state["step"] != "DONE":
        screen.update()
        time.sleep(0.05)
        
    for _ in range(20):
        time.sleep(0.05)
        screen.update()
        
    for k in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]: 
        screen.onkeypress(None, k)
        
    drawer.clear()
    screen.update()
    
    return menu_state["config"], menu_state["order"], menu_state["lang"]