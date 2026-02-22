import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
from pomodoro_logic import run_pomodoro, stop_pomodoro
from database import save_log, mark_todo_done_by_title
from tkinter import messagebox

timer_aktif = False  # Flag global untuk cek status timer

def open_timer_window(parent=None, on_close=lambda: None, task_title=None):
    top = tb.Toplevel() if parent is None else tb.Toplevel(parent)
    top.title("⏱️ Pomodoro Timer")

    def close_window():
        if timer_aktif:
            jawab = messagebox.askyesno("Konfirmasi", "Timer masih berjalan. Yakin ingin kembali?")
            if not jawab:
                return
        on_close()
        top.destroy()
    
    window_width = 400
    window_height = 500
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    top.geometry(f"{window_width}x{window_height}+{x}+{y}")
    top.protocol("WM_DELETE_WINDOW", close_window)

    def toggle_buttons_state(state):
        btn_fokus.config(state=state)
        btn_istirahat.config(state=state)
        btn_stop.config(state=NORMAL if state == DISABLED else DISABLED)

    def toggle_entry_state(state):
        entry.config(state=state)

    def start_session(tipe):
        try:
            durasi = int(entry.get())
            if durasi <= 0:
                update_label("Masukkan angka lebih dari 0")
                return
            thread = threading.Thread(
                target=run_pomodoro,
                args=(durasi * 60, update_label, tipe, on_timer_start, on_timer_finish)
            )
            thread.daemon = True
            thread.start()
            save_log(f"Mulai {tipe} selama {durasi} menit")
        except ValueError:
            update_label("Masukkan angka yang valid")

    def on_timer_start():
        global timer_aktif
        timer_aktif = True
        toggle_buttons_state(DISABLED)
        toggle_entry_state(DISABLED)

    def on_timer_finish():
        global timer_aktif
        timer_aktif = False
        toggle_buttons_state(NORMAL)
        toggle_entry_state(NORMAL)
        if task_title:
            mark_todo_done_by_title(task_title)
            save_log(f"Tugas '{task_title}' selesai (otomatis ditandai).")

    def stop_timer():
        global timer_aktif
        stop_pomodoro()
        update_label("⏹️ Timer dihentikan.")
        save_log("Timer dihentikan manual")
        timer_aktif = False
        toggle_buttons_state(NORMAL)
        toggle_entry_state(NORMAL)

    def update_label(text):
        try:
            if label.winfo_exists():
                label.config(text=text)
        except:
            pass

    def cek_input(event=None):
        try:
            val = int(entry.get())
            btn_stop.config(state=NORMAL if val > 0 else DISABLED)
        except:
            btn_stop.config(state=DISABLED)

    # UI
    tb.Label(top, text="⏳", font=("Helvetica", 48)).pack(pady=20)
    tb.Label(top, text="Masukkan waktu (menit):").pack()

    entry = tb.Entry(top)
    entry.pack()
    entry.bind("<KeyRelease>", cek_input)

    frame = tb.Frame(top)
    frame.pack(pady=20)

    btn_fokus = tb.Button(frame, text="Mulai", bootstyle="success-outline", command=lambda: start_session("Fokus"))
    btn_fokus.pack(side=LEFT, padx=6.5)

    btn_istirahat = tb.Button(frame, text="Istirahat", bootstyle="info-outline", command=lambda: start_session("Istirahat"))
    btn_istirahat.pack(side=LEFT, padx=6.5)

    btn_stop = tb.Button(frame, text="Stop", bootstyle="danger-outline", command=stop_timer, state=DISABLED)
    btn_stop.pack(side=LEFT, padx=6.5)

    tb.Button(top, text="⬅️ Kembali", bootstyle="secondary", command=close_window).pack(pady=5)

    label = tb.Label(top, text="⏱️ Belum dimulai", font=("Helvetica", 14))
    label.pack(pady=20)

    cek_input()
