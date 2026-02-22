import ttkbootstrap as tb
from tkinter import ttk, messagebox
from database import load_timer_logs, save_timer_logs
import os

def open_log_window(parent, on_close):
    top = tb.Toplevel(parent)
    top.title("📜 Log Aktivitas")

    def close_window():
        on_close()
        top.destroy()

    window_width = 700
    window_height = 500

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    top.geometry(f"{window_width}x{window_height}+{x}+{y}")

    top.protocol("WM_DELETE_WINDOW", close_window)

    # Frame utama
    frame = tb.Frame(top, padding=10)
    frame.pack(fill="both", expand=True)

    # Treeview log
    tree = ttk.Treeview(frame, columns=("timestamp", "message"), show="headings", height=15)
    tree.heading("timestamp", text="Waktu")
    tree.heading("message", text="Aktivitas")
    tree.column("timestamp", width=160, anchor="w")
    tree.column("message", anchor="w")
    tree.pack(fill="both", expand=True)

    def load_logs():
        tree.delete(*tree.get_children())  # hapus semua baris
        logs = load_timer_logs()
        logs = sorted(logs, key=lambda log: log['timestamp'], reverse=True)
        if logs:
            for log in logs:
                tree.insert("", "end", values=(log['timestamp'], log['message']))
        else:
            tree.insert("", "end", values=("—", "       Belum ada aktivitas."))

    def clear_logs():
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus semua log?"):
            save_timer_logs([])  # simpan list kosong
            load_logs()

    load_logs()

    # Tombol aksi
    btn_frame = tb.Frame(top)
    btn_frame.pack(pady=10)

    tb.Button(btn_frame, text="⬅️ Kembali", bootstyle="secondary", command=close_window).pack(side="left", padx=5)
    tb.Button(btn_frame, text="🗑️ Hapus Log", bootstyle="danger", command=clear_logs).pack(side="left", padx=5)