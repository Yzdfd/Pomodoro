from database import add_pomodoro_session
import time
import pygame  # Import pygame

stop_flag = False

# Inisialisasi pygame mixer (sekali saja)
pygame.mixer.init()

def play_sound():
    try:
        pygame.mixer.music.load("finish.mp3") 
        pygame.mixer.music.play()
    except Exception as e:
        print("Gagal memutar suara:", e)

def stop_pomodoro():
    global stop_flag
    stop_flag = True

def run_pomodoro(duration_seconds, update_callback=None, session_type="Timer", on_start=None, on_finish=None):
    global stop_flag
    stop_flag = False

    if on_start:
        on_start()

    total = duration_seconds
    while duration_seconds > 0:
        if stop_flag:
            if update_callback:
                update_callback(f"{session_type} dihentikan.")
            if on_finish:
                on_finish()
            return
        minutes = duration_seconds // 60
        sec = duration_seconds % 60
        if update_callback:
            update_callback(f"{session_type} - {minutes}:{sec:02}")
        time.sleep(1)
        duration_seconds -= 1

    if update_callback:
        update_callback(f"{session_type} selesai!")

    play_sound()  

    if on_finish:
        on_finish()

    add_pomodoro_session(total // 60, session_type)
