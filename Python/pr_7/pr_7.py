import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json

tasks_data = []
PRIORITY_WEIGHT = {"High": 1, "Medium": 2, "Low": 3}


def update_ui():
    """Сортує дані та оновлює Listbox"""
    tasks_data.sort(key=lambda x: PRIORITY_WEIGHT.get(x["priority"], 3))

    listbox.delete(0, tk.END)
    for task in tasks_data:
        listbox.insert(tk.END, f"[{task['priority']}] {task['text']}")


def add_task():
    task_text = entry.get().strip()
    priority = priority_combobox.get()

    if task_text == "":
        messagebox.showwarning("Warning", "You cannot add an empty task")
    else:
        tasks_data.append({"text": task_text, "priority": priority})
        entry.delete(0, tk.END)
        update_ui()


def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        tasks_data.pop(index)
        update_ui()


def clear_all():
    tasks_data.clear()
    update_ui()


def save_tasks_as():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Save tasks as"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=4)


def open_tasks():
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Open tasks"
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                global tasks_data
                tasks_data = json.load(f)
                update_ui()
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Could not read the file")


def show_about():
    messagebox.showinfo("About", "Task Manager v2.0\n:з")


window = tk.Tk()
window.title("Task Manager Pro")
window.geometry("450x450")

window.columnconfigure(1, weight=1)

tk.Label(window, text="Task:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry = tk.Entry(window)
entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

tk.Label(window, text="Priority:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
priority_combobox = ttk.Combobox(window, values=["High", "Medium", "Low"], state="readonly")
priority_combobox.current(1)
priority_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="we")

add_button = tk.Button(window, text="Add task", command=add_task)
add_button.grid(row=2, column=0, columnspan=2, pady=5)

listbox = tk.Listbox(window, width=50, height=10)
listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

button_frame = tk.Frame(window)
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

del_button = tk.Button(button_frame, text="Delete task", command=delete_task)
del_button.pack(side="left", padx=50)

clear_button = tk.Button(button_frame, text="Clear all", command=clear_all)
clear_button.pack(side="left", padx=50)

menubar = tk.Menu(window)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open...", command=open_tasks)
file_menu.add_command(label="Save As...", command=save_tasks_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

window.config(menu=menubar)

window.mainloop()