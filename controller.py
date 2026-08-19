import pygame  # type: ignore

class Controller:
    DEADZONE = 0.5
    PADDLE_SPEED = 20  # Adjust this number to change controller paddle speed

    def __init__(self, joystick_id=0):
        pygame.init()
        pygame.joystick.init()

        self.joystick_id = joystick_id
        self.controller = None
        self.button_states = {}

        if self.connect_controller():
            print(f"Controller {self.joystick_id} connected: {self.controller.get_name()}")
        else:
            # We don't need to print failure here anymore since the menu handles it smoothly
            pass

    def connect_controller(self):
        if pygame.joystick.get_count() <= self.joystick_id:
            return False

        self.controller = pygame.joystick.Joystick(self.joystick_id)
        self.controller.init()
        return True

    def update(self, paddle):
        pygame.event.pump()

        if self.controller is None:
            self.connect_controller()
            return []

        new_presses = []

        try:
            for button in range(self.controller.get_numbuttons()):
                is_pressed = self.controller.get_button(button)
                if is_pressed and not self.button_states.get(button, False):
                    new_presses.append(button)
                self.button_states[button] = is_pressed

            x = self.controller.get_axis(0)
            y = self.controller.get_axis(1)

        except pygame.error:
            self.controller = None
            self.button_states.clear()
            print(f"Controller {self.joystick_id} disconnected.")
            return []

        # Joystick Deadzone
        if abs(x) < self.DEADZONE and abs(y) < self.DEADZONE:
            return new_presses

        # Apply continuous movement using the NEW movement methods!
        if abs(x) > abs(y):
            if x < -self.DEADZONE:
                paddle.move_x(-self.PADDLE_SPEED)
            elif x > self.DEADZONE:
                paddle.move_x(self.PADDLE_SPEED)
        else:
            if y < -self.DEADZONE:
                paddle.move_y(self.PADDLE_SPEED)
            elif y > self.DEADZONE:
                paddle.move_y(-self.PADDLE_SPEED)

        return new_presses