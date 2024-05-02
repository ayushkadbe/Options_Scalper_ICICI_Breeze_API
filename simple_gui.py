import tkinter as tk
from datetime import datetime
import api_trade as apt


def create_widgets():
    tk.Label(root, text="Lots:", bg="#0B0F15", fg="white").grid(row=5, column=0, pady=5)
    tk.Label(root, text="$ Risk", bg="#0B0F15", fg="white").grid(row=5, column=1, pady=5)
    tk.Label(root, text="SL", bg="#0B0F15", fg="white").grid(row=5, column=2, pady=5)

    lots_var = tk.DoubleVar()
    lots_var.set(1)  # Default value
    lots_entry = tk.Entry(root, textvariable=lots_var)
    lots_entry.grid(row=6, column=0, pady=5)

    dollar_risk_var = tk.DoubleVar()
    dollar_risk_var.set(20)  # Default value
    dollar_risk_entry = tk.Entry(root, textvariable=dollar_risk_var)
    dollar_risk_entry.grid(row=6, column=1, pady=5)

    percent_risk_var = tk.DoubleVar()
    percent_risk_var.set(5)  # Default value
    percent_risk_entry = tk.Entry(root, textvariable=percent_risk_var)
    percent_risk_entry.grid(row=6, column=2, pady=5)

    # 4) ORDER BUY, SQUARE OFF, EXIT ALL BUTTON
    tk.Button(root, text="BUY CALL", command=apt.gui_place_call_order, bg="green", fg="white").grid(row=7, column=0, columnspan=2, pady=10)
    tk.Button(root, text="BUY PUT", command=apt.gui_place_put_order, bg="green", fg="white").grid(row=7, column=1, columnspan=2, pady=10)
    tk.Button(root, text="SELL CALL", command=apt.gui_square_off_call_order, bg="blue", fg="white").grid(row=8, column=0, columnspan=2, pady=10)
    tk.Button(root, text="SELL PUT", command=apt.gui_square_off_put_order, bg="red", fg="white").grid(row=8, column=1, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Options Scalper Terminal")
    root.configure(bg="#0B0F15")
    
    print("Starting Execution")
    apt.initialize_sdk()
    apt.connect_to_socket()
 
    create_widgets()

    root.mainloop()
