import threading
import time
import datetime
from pynput import keyboard, mouse

PROFILES = [
    ("1 click/sec", 1.0),
    ("2 clicks/sec", 0.5),
    ("5 clicks/sec", 0.2),
    ("10 clicks/sec", 0.1),
    ("20 clicks/sec", 0.05),
]

current_profile_index = 0
clicking = False
click_lock = threading.Lock()
mouse_controller = mouse.Controller()
log_time = datetime.datetime.now().strftime("%H:%M:%S")

def get_current_interval() -> float:
    return PROFILES[current_profile_index][1]


def get_current_profile_name() -> str:
    return PROFILES[current_profile_index][0]


def cycle_profile(step: int = 1) -> None:
    global current_profile_index
    current_profile_index = (current_profile_index + step) % len(PROFILES)
    print(
        f"[{log_time}] Profile: {get_current_profile_name()} "
        f"({get_current_interval():.3f}s per click)"
    )


def click_loop() -> None:
    global clicking
    while clicking:
        mouse_controller.click(mouse.Button.left, 1)
        time.sleep(get_current_interval())


def toggle_clicking() -> None:
    global clicking

    with click_lock:
        if clicking:
            clicking = False
            print(f"[{log_time}] Auto-clicker stopped.")
            return

        clicking = True
        print(
            f"[{log_time}] Auto-clicker started: {get_current_profile_name()} "
            f"({get_current_interval():.3f}s per click)"
        )
        thread = threading.Thread(target=click_loop, daemon=True)
        thread.start()


def on_key_press(key) -> None:
    if hasattr(key, "char") and key.char is not None:
        char = key.char.lower()

        if char == "*":
            toggle_clicking()
            return

        if char == "[":
            cycle_profile(-1)
            return

        if char == "]":
            cycle_profile(1)
            return

    if key == keyboard.Key.esc:
        print(f"[{log_time}] Exiting auto-clicker.")
        raise SystemExit


if __name__ == "__main__":
    print(f"[{log_time}] Auto-clicker ready.")
    print(f"[{log_time}] Press * to start/stop.")
    print(f"[{log_time}] Press [ or ] to change the speed profile.")
    print(f"[{log_time}] Press Esc to quit.")
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()
