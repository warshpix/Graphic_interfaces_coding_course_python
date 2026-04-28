import tkinter as tk

window = tk.Tk()
window.title("Task Manager")
window.geometry("400x400")

entry = tk.Entry(window, width=30)
entry.pack(pady=10)

listbox = tk.Listbox(window, width=40, height=10)
listbox.pack(pady=10)

def add_task():
    task = entry.get()
    if task != "":
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)

def delete_task():
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected)

add_button = tk.Button(window, text="Add task", command=add_task)
add_button.pack(pady=5)


add_button = tk.Button(window, text="Delete task", command=delete_task)
add_button.pack(pady=5)

window.mainloop()