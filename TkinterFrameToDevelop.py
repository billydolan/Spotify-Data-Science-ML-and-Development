import tkinter as tk

def calculate_t0():
    try:
        teeAy = float(entry_ta.get())
        em = float(entry_m.get())
        whyC = 1.4
        teeOh = teeAy * (1 + ((whyC - 1)/2) * (em*em))
        result_label.config(text="T0 = {:.2f}".format(teeOh))
    except ValueError: result_label.config(text="Invalid input")

root = tk.Tk()
root.resizable(False,False)
root.title("Calculate T0")
root.geometry("250x220")

root.bind("<Escape>", lambda event: root.destroy())

label_ta = tk.Label(root, text="Enter Ta:")
label_ta.grid(row=0, column=0, padx=10, pady=10)

entry_ta = tk.Entry(root)
entry_ta.grid(row=0, column=1, padx=10, pady=10)

label_m = tk.Label(root, text="Enter M:")
label_m.grid(row=1, column=0, padx=10, pady=10)

entry_m = tk.Entry(root)
entry_m.grid(row=1, column=1, padx=10, pady=10)

calculate_button = tk.Button(root, text="Calculate T0", command=calculate_t0)
calculate_button.grid(row=2, column=0, columnspan=2, pady=20)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2)

root.mainloop()