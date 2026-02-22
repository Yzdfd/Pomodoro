import ttkbootstrap as tb
from ttkbootstrap.constants import *
from timer_view import open_timer_window
import database
import tkinter as tk
from tkinter import messagebox

def open_todo_window(parent, on_close):
    top = tb.Toplevel(parent)
    top.title("✅ To-Do List")
    tb.Label(top, text="Mau Ngapain Hari Ini ?", font=("Helvetica", 12)).pack(pady=(20, 10))

    window_width = 500
    window_height = 520
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    top.geometry(f"{window_width}x{window_height}+{x}+{y}")
    top.protocol("WM_DELETE_WINDOW", lambda: [on_close(), top.destroy()])

    entry = tb.Entry(top, width=50)
    entry.pack(pady=(0, 15), padx=10)

    frame_buttons = tb.Frame(top)
    frame_buttons.pack(pady=(0, 15), padx=10)
    
    # Frame listbox ganda
    frame_lists = tb.Frame(top)
    frame_lists.pack(fill='both', expand=True, padx=10, pady=(0, 15))

    # Frame kiri: tugas belum selesai
    frame_left = tb.Frame(frame_lists)
    frame_left.pack(side='left', fill='both', expand=True, padx=5)

    tb.Label(frame_left, text="❌ Belum Selesai", font=("Segoe UI", 10, "bold")).pack(pady=(0, 3))
    listbox_not_done = tk.Listbox(frame_left, width=40, height=12)
    listbox_not_done.pack(fill='both', expand=True)

    # Frame kanan: tugas selesai
    frame_right = tb.Frame(frame_lists)
    frame_right.pack(side='left', fill='both', expand=True, padx=5)

    tb.Label(frame_right, text="✔ Selesai", font=("Segoe UI", 10, "bold")).pack(pady=(0, 3))
    listbox_done = tk.Listbox(frame_right, width=40, height=12)
    listbox_done.pack(fill='both', expand=True)

    def mulai_pomodoro():
        try:
            index = listbox_not_done.curselection()[0]
            task_text = listbox_not_done.get(index).strip()
            open_timer_window(parent, lambda: open_todo_window(parent, on_close), task_title=task_text)
            top.destroy()
        except IndexError:
            messagebox.showwarning("Pilih Tugas", "Pilih tugas dari daftar belum selesai.")

    def tandai_selesai():
        try:
            index = listbox_not_done.curselection()[0]
            task_text = listbox_not_done.get(index).strip()
            tasks = database.load_todo_list()
            for i, task in enumerate(tasks):
                if task['task'] == task_text and not task.get('done', False):
                    tasks[i]['done'] = True
                    database.save_todo_list(tasks)
                    database.save_log(f"Tugas ditandai selesai: '{task_text}'")
                    refresh_listbox()
                    break
        except:
            pass

    def hapus_task():
        try:
            index = listbox_not_done.curselection()[0]
            task_text = listbox_not_done.get(index).strip()
            confirm = messagebox.askyesno("Hapus", f"Yakin ingin menghapus:\n\n{task_text}?")
            if confirm:
                tasks = database.load_todo_list()
                for i, task in enumerate(tasks):
                    if task['task'] == task_text and not task.get('done', False):
                        tasks.pop(i)
                        database.save_todo_list(tasks)
                        refresh_listbox()
                        break
        except:
            pass

    def hapus_semua():
        confirm = messagebox.askyesno("Hapus Semua", "Yakin ingin menghapus SEMUA tugas?")
        if confirm:
            database.save_todo_list([])
            database.write_todo_log_json("Semua tugas dihapus.")
            refresh_listbox()

    def tambah_task():
        task_text = entry.get().strip()
        if task_text:
            database.add_todo_item(task_text)
            database.save_log(f"Tugas ditambahkan: '{task_text}'")
            entry.delete(0, 'end')
            refresh_listbox(select_last=True)

    def show_stats():
        tasks = database.load_todo_list()
        total = len(tasks)
        done = sum(1 for t in tasks if t.get('done', False))
        not_done = total - done

        popup = tb.Toplevel(top)
        popup.title("📊 Statistik")
        popup.geometry("220x150+{}+{}".format(
            top.winfo_screenwidth() // 2 - 110,
            top.winfo_screenheight() // 2 - 75
        ))

        tb.Label(popup, text=(
            f"Total tugas : {total}\n"
            f"Tugas Selesai : {done}\n"
            f"Tugas Yang Belum Selesai : {not_done}"
        ), font=("Segoe UI", 11)).pack(pady=20)

        tb.Button(popup, text="OK", command=popup.destroy, bootstyle="primary").pack()
        popup.transient(top)
        popup.grab_set()
        top.wait_window(popup)

    def update_button_state(event=None):
        try:
            index = listbox_not_done.curselection()[0]
            btn_mulai.config(state="normal")
            btn_selesai.config(state="normal")
            btn_hapus.config(state="normal")
        except:
            btn_mulai.config(state="disabled")
            btn_selesai.config(state="disabled")
            btn_hapus.config(state="disabled")

    def refresh_listbox(select_last=False):
        tasks = database.load_todo_list()
        not_done = [t['task'] for t in tasks if not t.get('done', False)]
        done = [t['task'] for t in tasks if t.get('done', False)]

        listbox_not_done.delete(0, 'end')
        listbox_done.delete(0, 'end')

        for t in not_done:
            listbox_not_done.insert('end', t)
        for t in done:
            listbox_done.insert('end', t)

        if select_last and listbox_not_done.size() > 0:
            listbox_not_done.select_set(listbox_not_done.size() - 1)
            listbox_not_done.event_generate("<<ListboxSelect>>")

        update_button_state()

    # Tombol-tombol utama
    tb.Button(frame_buttons, text="➕ Tambah", command=tambah_task, bootstyle="success-outline").pack(side='left', padx=5)

    btn_hapus = tb.Button(frame_buttons, text="❌ Hapus", command=hapus_task, bootstyle="danger-outline", state="disabled")
    btn_hapus.pack(side='left', padx=5)

    tb.Button(frame_buttons, text="📊 Stats", command=show_stats, bootstyle="info-outline").pack(side='left', padx=5)

    btn_selesai = tb.Button(frame_buttons, text="✔️ Done", command=tandai_selesai, bootstyle="success-outline", state="disabled")
    btn_selesai.pack(side='left', padx=5)
    
    btn_mulai = tb.Button(frame_buttons, text="Mulai Pomodoro", command=mulai_pomodoro, bootstyle="primary-outline", state="disabled")
    btn_mulai.pack(side='left', padx=5)


    btn_hapus_semua = tb.Button(top, text="🗑️ Hapus Semua", command=hapus_semua, bootstyle="danger")
    btn_hapus_semua.pack(pady=(0, 5))

    tb.Button(top, text="⬅️ Kembali", bootstyle="secondary", command=lambda: [on_close(), top.destroy()]).pack(pady=5)

    listbox_not_done.bind("<<ListboxSelect>>", update_button_state)

    refresh_listbox()
