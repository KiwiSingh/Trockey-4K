import time
from turtle import Turtle

def run_setup_menu(screen):
    screen.clear()
    screen.bgcolor("black")
    screen.tracer(0)

    drawer = Turtle()
    drawer.hideturtle()
    drawer.color("white")
    drawer.penup()

    # Shared state dictionary to safely track the menu progress
    menu_state = {
        "step": "COUNT",  
        "num_players": 0,
        "current_player": 1,
        "config": {"left": False, "right": False, "top": False},
        "order": [],
        "available": ["left", "right", "top"]
    }
    
    # Keyboard mappings for the UI
    keyboard_map = {
        "left": "WASD",
        "right": "Arrow Keys",
        "top": "IJKL"
    }

    def draw_menu():
        drawer.clear()
        drawer.goto(0, 200)
        drawer.color("cyan")
        drawer.write("TROCKEY 4K SETUP", align="center", font=("Courier", 48, "bold"))
        drawer.color("white")
        
        if menu_state["step"] == "COUNT":
            drawer.goto(0, 0)
            drawer.write("How many humans? (Press 0, 1, 2, or 3)", align="center", font=("Courier", 36, "normal"))
            
        elif menu_state["step"] == "POSITION":
            drawer.goto(0, 50)
            drawer.color("yellow")
            drawer.write(f"Player {menu_state['current_player']} (Controller {menu_state['current_player']}), choose your side:", align="center", font=("Courier", 36, "bold"))
            
            drawer.color("white")
            y = -50
            if "left" in menu_state["available"]:
                drawer.goto(0, y)
                drawer.write("Press 1 for LEFT (WASD)", align="center", font=("Courier", 24, "normal"))
            y -= 50
            if "right" in menu_state["available"]:
                drawer.goto(0, y)
                drawer.write("Press 2 for RIGHT (Arrow Keys)", align="center", font=("Courier", 24, "normal"))
            y -= 50
            if "top" in menu_state["available"]:
                drawer.goto(0, y)
                drawer.write("Press 3 for TOP (IJKL)", align="center", font=("Courier", 24, "normal"))

        elif menu_state["step"] == "DONE":
            if menu_state["num_players"] == 0:
                drawer.goto(0, 100)
                drawer.color("green")
                drawer.write("SPECTATOR MODE INITIATED", align="center", font=("Courier", 48, "bold"))
                
                drawer.goto(0, 0)
                drawer.color("white")
                drawer.write("All paddles set to AI.", align="center", font=("Courier", 24, "normal"))
                
                drawer.goto(0, -100)
                drawer.color("yellow")
                drawer.write("Dropping puck in 4 seconds...", align="center", font=("Courier", 24, "italic"))
                
            else:
                drawer.goto(0, 100)
                drawer.color("green")
                drawer.write("ALL PLAYERS READY!", align="center", font=("Courier", 48, "bold"))
                
                drawer.goto(0, 20)
                drawer.color("cyan")
                drawer.write("--- PLAYER DIBS ---", align="center", font=("Courier", 36, "bold"))
                
                y = -50
                drawer.color("white")
                for i, pos in enumerate(menu_state["order"]):
                    drawer.goto(0, y)
                    # --- EXPLICITLY MAP BOTH CONTROLLERS AND KEYBOARDS ON THE FINAL SCREEN ---
                    drawer.write(f"Player {i+1} (Ctrl {i+1} / {keyboard_map[pos]}) -> {pos.upper()} PADDLE", align="center", font=("Courier", 24, "normal"))
                    y -= 50
                    
                drawer.goto(0, y - 40)
                drawer.color("yellow")
                drawer.write("Dropping puck in 4 seconds...", align="center", font=("Courier", 24, "italic"))

        screen.update()

    def handle_key(key):
        if menu_state["step"] == "COUNT":
            if key in ["0", "1", "2", "3"]:
                menu_state["num_players"] = int(key)
                if menu_state["num_players"] == 0:
                    menu_state["step"] = "DONE"
                else:
                    menu_state["step"] = "POSITION"
                draw_menu()
        
        elif menu_state["step"] == "POSITION":
            choice = None
            if key == "1" and "left" in menu_state["available"]:
                choice = "left"
            elif key == "2" and "right" in menu_state["available"]:
                choice = "right"
            elif key == "3" and "top" in menu_state["available"]:
                choice = "top"
            
            if choice:
                menu_state["config"][choice] = True
                menu_state["order"].append(choice)
                menu_state["available"].remove(choice)
                
                if menu_state["current_player"] < menu_state["num_players"]:
                    menu_state["current_player"] += 1
                else:
                    menu_state["step"] = "DONE"
                draw_menu()

    def press_0(): handle_key("0")
    def press_1(): handle_key("1")
    def press_2(): handle_key("2")
    def press_3(): handle_key("3")

    screen.listen()
    screen.onkeypress(press_0, "0")
    screen.onkeypress(press_1, "1")
    screen.onkeypress(press_2, "2")
    screen.onkeypress(press_3, "3")
    
    draw_menu()
    
    while menu_state["step"] != "DONE":
        screen.update()
        time.sleep(0.05)
        
    time.sleep(4.0) 
    
    screen.onkeypress(None, "0")
    screen.onkeypress(None, "1")
    screen.onkeypress(None, "2")
    screen.onkeypress(None, "3")
    
    return menu_state["config"], menu_state["order"]