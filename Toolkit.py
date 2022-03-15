import platform
import tkinter as tk
from PIL import ImageTk,Image

def informacje():
    my_system = platform.uname()
    listbox.insert('end', f"System: {my_system.system}")
    listbox.insert('end', f"Node Name: {my_system.node}")
    listbox.insert('end', f"Release: {my_system.release}")
    listbox.insert('end', f"Version: {my_system.version}")
    listbox.insert('end', f"Machine: {my_system.machine}")
    listbox.insert('end', f"Processor: {my_system.processor}")

root = tk.Tk()
root.geometry("300x300")
root.title("System")

bg = ImageTk.PhotoImage(file = "computer.jpg")
label1 = tk.Label( root, image = bg)
label1.place(x = 0, y = 0)

listbox = tk.Listbox(root, width=30)
listbox.grid(sticky="news")
listbox.place(relx = 0.5, rely = 0.5, anchor="center")
b=tk.Button(root, text="Wyswietl informacje", width= 20, bg = "dark green", fg="white", command = informacje)
b.grid(padx=77, pady=240)

root.mainloop()