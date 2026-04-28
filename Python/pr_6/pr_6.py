import tkinter as tk
from tkinter import messagebox
import json

window = tk.Tk()
window.title("Task Manager")
window.geometry("400x400")

entry = tk.Entry(window, width=30)
entry.pack(pady=10)

listbox = tk.Listbox(window, width=40, height=10)
listbox.pack(pady=10)

def add_task():
    task = entry.get().strip()
    if task == "":
        messagebox.showwarning("Warning", "You cannot add an empty task")
    else:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()

def delete_task():
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected)
        save_tasks()

def save_tasks():
    tasks = listbox.get(0, tk.END)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def load_tasks():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
            for task in tasks:
                listbox.insert(tk.END, task)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def clear_all():
    listbox.delete(0, tk.END)
    save_tasks()

add_button = tk.Button(window, text="Add task", command=add_task)
add_button.pack(pady=5)


add_button = tk.Button(window, text="Delete task", command=delete_task)
add_button.pack(pady=5)


clear_button = tk.Button(window, text="Clear all", command=clear_all)
clear_button.pack(pady=5)

load_tasks()
window.mainloop()