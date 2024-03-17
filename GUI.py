import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import joblib

def predict_values():
    try:
        # Get input variable values
        values1 = [float(entry.get()) for entry in entries1]
        values2 = [float(entry.get()) for entry in entries2]
        values = values1 + values2

        # Predict optimal excitation wavelength using Model 1
        prediction1 = model1.predict([values])
        oem = prediction1[0]

        # Predict optimal emission wavelength using Model 2
        prediction2 = model2.predict([values + [oem]])
        oex = prediction2[0]

        # Predict afterglow lifetime using Model 3
        prediction3 = model3.predict([values + [oex]])

        # Create a custom message box
        custom_messagebox = tk.Toplevel(root)
        custom_messagebox.title("Prediction Results")
        custom_messagebox.geometry("600x150")

        # Set font for the message
        message_label = tk.Label(custom_messagebox, text=f"Optimal excitation wavelength: {oem}\nOptimal emission wavelength: {oex}\nAfterglow lifetime: {prediction3[0]}", font=("Arial", 16))
        message_label.pack(padx=20, pady=10)

        # Button to close the window
        close_button = ttk.Button(custom_messagebox, text="Close", command=custom_messagebox.destroy)
        close_button.pack(pady=10)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values")

# Load models
model1 = joblib.load("Oem.pkl")
model2 = joblib.load("Oex.pkl")
model3 = joblib.load("life.pkl")

# Create GUI window
root = tk.Tk()
root.title("CDs afterglow property prediction GUI")
root.geometry("700x400")
root.iconbitmap("favicon.ico")  # Set icon, replace "icon.ico" with your icon file path
root.configure(bg="white")  # Set background color to white

# Create input fields and labels
variables = ["C", "H", "N", "O", "HOMO", "LUMO", "GAP", "Energy", "Mr", "St", "Pol", "TPSA", "NHA", "Mc", "Qm", "Mt"]
entries1 = []
entries2 = []

for i, var in enumerate(variables[:8]):
    tk.Label(root, text=var, font=("Arial", 14), bg="white").grid(row=i, column=0, pady=5, padx=10, sticky="w")
    entry = tk.Entry(root, font=("Arial", 14))
    entry.grid(row=i, column=1, pady=5, padx=10, sticky="e")
    entries1.append(entry)

for i, var in enumerate(variables[8:]):
    tk.Label(root, text=var, font=("Arial", 14), bg="white").grid(row=i, column=2, pady=5, padx=10, sticky="w")
    entry = tk.Entry(root, font=("Arial", 14))
    entry.grid(row=i, column=3, pady=5, padx=10, sticky="e")
    entries2.append(entry)

# Create predict button
predict_button = tk.Button(root, text="Predict", command=predict_values, bg="#4CAF50", fg="white", font=("Arial", 14))
predict_button.grid(row=9, columnspan=4, pady=10, padx=10)

root.mainloop()
