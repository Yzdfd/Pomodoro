import ttkbootstrap as tb
from ttkbootstrap.constants import *
from timer_view import open_timer_window
from todo_view import open_todo_window
from log_view import open_log_window
from PIL import Image, ImageTk
from tkinter import messagebox, PhotoImage
# from config import APP_TITLE, WINDOW_SIZE
from task_preview import open_pending_tasks_window

# Flag status window
is_timer_open = False
is_todo_open = False
is_log_open = False

def set_timer_open(state):
    global is_timer_open
    is_timer_open = state

def set_todo_open(state):
    global is_todo_open
    is_todo_open = state

def set_log_open(state):
    global is_log_open
    is_log_open = state

def handle_timer_window():
    if is_timer_open:
        return

    popup = tb.Toplevel(app)
    popup.title("Konfirmasi")
    
    # Ukuran jendela
    window_width = 250
    window_height = 130

    # Dapatkan ukuran layar
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Hitung posisi tengah
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Atur ukuran dan posisi jendela
    popup.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    popup.resizable(False, False)
    popup.transient(app)
    popup.grab_set()

    tb.Label(popup, text="Mau mulai pomdoro nya?", font=("Helvetica", 11)).pack(pady=(20, 10))

    frame_btn = tb.Frame(popup)
    frame_btn.pack(pady=10)
    
    def lanjut_ke_timer():
        popup.destroy()
        from task_preview import open_pending_tasks_window  # import di sini agar tidak circular
        open_pending_tasks_window(app)  # tampilkan jendela daftar tugas belum selesai

    def batal():
        popup.destroy()

    tb.Button(frame_btn, text="Pilih Tugas", bootstyle="success", width=10, command=lanjut_ke_timer).pack(side="left", padx=10)
    tb.Button(frame_btn, text="Nanti saja", bootstyle="secondary", width=10, command=batal).pack(side="right", padx=10)

def handle_todo_window():
    if not is_todo_open:
        set_todo_open(True)
        app.withdraw()
        open_todo_window(app, lambda: [set_todo_open(False), app.deiconify()])

def handle_log_window():
    if not is_log_open:
        set_log_open(True)
        app.withdraw()
        open_log_window(app, lambda: [set_log_open(False), app.deiconify()])

app = tb.Window(themename="darkly")
app.title("Dashboard")

# Ukuran jendela
window_width = 400
window_height = 500

# Dapatkan ukuran layar
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Hitung posisi tengah
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Atur ukuran dan posisi jendela
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Frame horizontal untuk logo + judul
top_frame = tb.Frame(app)
top_frame.pack(pady=5)

# Tambahkan gambar/logo di kiri
try:
    img = Image.open("assets/png/target.png")
    img = img.resize((50, 35))  # Ukuran gambar
    logo = ImageTk.PhotoImage(img)

    logo_label = tb.Label(top_frame, image=logo)
    logo_label.image = logo  # Penting agar tidak dikoleksi
    logo_label.pack(side="left", padx=0)
except Exception as e:
    print("Gagal memuat gambar:", e)

# Tambahkan teks judul di kanan gambar
tb.Label(top_frame, text="Pomodoro App", font=("Helvet1ca", 16, "bold")).pack(side="left", padx=5)

tb.Label(app, text="Teknik Fokus Waktu", font=("Helvetica", 10)).pack(pady=5)
# Judul & Menu
# Frame konten tengah
content_wrapper = tb.Frame(app)
content_wrapper.pack(expand=True, fill="both")

middle_frame = tb.Frame(app)
middle_frame = tb.Frame(content_wrapper)
middle_frame.place(relx=0.5, rely=0.4, anchor="center")  # Letakkan di tengah tapi masih bisa bergerak

tb.Label(middle_frame, text="Silakan Pilih Menu:", font=("Helvetica", 14)).pack(pady=5)

button_width = 20
tb.Button(middle_frame, text="⏱️ Pomodoro Timer", bootstyle="success-outline", command=handle_timer_window, width=button_width).pack(pady=10)
tb.Button(middle_frame, text="✅ To-Do List", bootstyle="info-outline", command=handle_todo_window, width=button_width).pack(pady=10)
tb.Button(middle_frame, text="📜 Lihat Log", bootstyle="warning-outline", command=handle_log_window, width=button_width).pack(pady=10)

# Tombol keluar di bawah layar
bottom_frame = tb.Frame(app)
bottom_frame.pack(pady=10)

def keluar_program():
    if messagebox.askyesno("Konfirmasi", "Yakin ingin keluar dari program?"):
        app.destroy()

tb.Button(bottom_frame, text="🚪 Keluar Program", bootstyle="danger-outline", command=keluar_program, width=button_width).pack()

app.mainloop()
