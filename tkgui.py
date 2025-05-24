import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    frame = ttk.Frame(root)
    frame.pack()

    entryvar = tk.StringVar()
    entry = ttk.Entry(frame, textvariable=entryvar)
    button = ttk.Button(frame, text="Click me!" ,command=lambda: print(entryvar.get()))

    entry.grid(row=0, column=0)
    button.grid(row=0, column=1)    

    root.geometry('300x400')    
    root.mainloop()    


if __name__ == "__main__":
    main()