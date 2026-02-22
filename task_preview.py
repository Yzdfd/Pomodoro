import ttkbootstrap as tb
from ttkbootstrap.constants import *
import database
from timer_view import open_timer_window
from todo_view import open_todo_window

def open_pending_tasks_window(parent):
    window = tb.Toplevel(parent)
    window.title("Pilih Tugas")
    window.resizable(False, False)
    window.transient(parent)
    window.grab_set()

    window_width = 350
    window_height = 450
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tb.Label(window, text="Tugas Yang Belum Diselesaikan", font=("Helvetica", 13, "bold")).pack(pady=10)

    frame = tb.Frame(window)
    frame.pack(fill="both", expand=True, padx=10)

    canvas = tb.Canvas(frame)
    scrollbar = tb.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tb.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tasks = database.load_todo_list()
    unfinished_tasks = [task for task in tasks if not task.get("done", False)]

    selected_task = {"title": None}
    label_refs = []

    def select_task(title, label_widget):
        for ref in label_refs:
            ref.configure(font=("Helvetica", 10), bootstyle="default")
        label_widget.configure(font=("Helvetica", 10, "bold"), bootstyle="primary")
        selected_task["title"] = title
        start_button.configure(state=NORMAL)

    if not unfinished_tasks:
        tb.Label(scroll_frame, text="🎉 Tidak ada tugas tertunda!", font=("Helvetica", 11)).pack(pady=20)
    else:
        for task in unfinished_tasks:
            task_title = task.get("task", "Tanpa Judul")
            label = tb.Label(
                scroll_frame,
                text="🔸 " + task_title,
                font=("Helvetica", 10),
                anchor="w",
                cursor="hand2"
            )
            label.pack(fill="x", pady=4)
            label.bind("<Button-1>", lambda e, title=task_title, lbl=label: select_task(title, lbl))
            label_refs.append(label)

    # Tombol Mulai
    def start_timer():
        if selected_task["title"]:
            window.destroy()       # Tutup task_preview
            # Jangan destroy parent, cukup sembunyikan kalau perlu
            # parent.withdraw()
            open_timer_window(task_title=selected_task["title"])

    start_button = tb.Button(window, text="Mulai", bootstyle="success", command=start_timer, state=DISABLED)
    start_button.pack(pady=(10, 0))

    def buka_todo():
        window.destroy()
        parent.withdraw()
        open_todo_window(parent, on_close=lambda: parent.deiconify())

    todo_button = tb.Button(
        window,
        text="Buka To-Do List",
        bootstyle="info",
        command=buka_todo,
        state=NORMAL if not unfinished_tasks else DISABLED
    )
    todo_button.pack(pady=(5, 0))

    tb.Button(window, text="Tutup", bootstyle="secondary", command=window.destroy).pack(pady=(5, 10))
