import tkinter as tk
from tkinter import ttk
# from breeze_connect import BreezeConnect
from datetime import datetime
import login as l
# import api_trade as at

class TradingTerminal:
    def __init__(self, master):
        self.master = master
        self.master.title("Options Scalper Terminal")
        self.master.configure(bg="#0B0F15")  # Set the background color       


        # # Initialize SDK
        # self.breeze = BreezeConnect(api_key=l.api_key)

        # # Generate Session
        # self.breeze.generate_session(api_secret=l.secret_key,
        #                         session_token=l.session_key)

        # # Connect to websocket(it will connect to tick-by-tick data server)
        # self.breeze.ws_connect()

        # # Callback to receive ticks.
        # def on_ticks(ticks):
        #     print("Ticks: {}".format(ticks))

        # # Assign the callbacks.
        # breeze.on_ticks = on_ticks
        
        # UI Components
        self.create_widgets()

    def create_widgets(self):
        #1) Realtime Data
        tk.Label(self.master, text="Symbol Spot:", bg="#0B0F15", fg="white").grid(row=0, column=0, )
        tk.Label(self.master, text="Expiry:", bg="#0B0F15", fg="white").grid(row=0, column=1, pady=5)
        tk.Label(self.master, text="Strike:", bg="#0B0F15", fg="white").grid(row=0, column=2, pady=5)

        self.symbol_var = tk.StringVar()
        self.symbol_dropdown = ttk.Combobox(self.master, textvariable=self.symbol_var, values=["NIFTY", "BANKNIFTY", "SENSEX"])
        self.symbol_dropdown.grid(row=1, column=0, pady=5)
        self.symbol_dropdown.set("NIFTY")  # Set the default value

        atm_strike = at.get_atm_strike(self.symbol_var.get())  
        self.expiry_date_var = tk.StringVar()
        self.expiry_date_dropdown = ttk.Combobox(self.master, textvariable=self.expiry_date_var, values=["123", "456", "OTM"])
        self.expiry_date_dropdown.grid(row=1, column=1, pady=5)
        self.expiry_date_dropdown.set("123")  # Set the default value

        # Get ATM strike using the function
        atm_strike = at.get_atm_strike(self.symbol_var.get())        
        self.strike_var = tk.StringVar()
        self.strike_dropdown = ttk.Combobox(self.master, textvariable=self.strike_var, values=["ATM", "ITM", "OTM"])
        self.strike_dropdown.grid(row=1, column=2, pady=5)
        self.strike_dropdown.set(f"{atm_strike}")  # Set the default value as ATM strike

        
        #2) CALL PUT STRIKE, LTP        
        tk.Label(self.master, text="Call", bg="red", fg="white", font=("Helvetica", 16)).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Label(self.master, text="PUT", bg="green", fg="white", font=("Helvetica", 16)).grid(row=2, column=1, columnspan=2, pady=10)
        
        # CALL DATA
        self.lots_var = tk.DoubleVar()
        self.lots_var.set(1)  # Default value
        self.lots_entry = tk.Entry(self.master, textvariable=self.lots_var)
        self.lots_entry.grid(row=3, column=0, pady=5)

        self.dollar_risk_var = tk.DoubleVar()
        self.dollar_risk_var.set(20)  # Default value
        self.dollar_risk_entry = tk.Entry(self.master, textvariable=self.dollar_risk_var)
        self.dollar_risk_entry.grid(row=4, column=0, pady=5)
        
        #LABELS
        tk.Label(self.master, text="Strike Price:", bg="#0B0F15", fg="white").grid(row=3, column=1, pady=5)
        tk.Label(self.master, text="LTP", bg="#0B0F15", fg="white").grid(row=4, column=1, pady=5)       
        
        # PUT DATA
        self.lots_var = tk.DoubleVar()
        self.lots_var.set(1)  # Default value
        self.lots_entry = tk.Entry(self.master, textvariable=self.lots_var)
        self.lots_entry.grid(row=3, column=2, pady=5)

        self.dollar_risk_var = tk.DoubleVar()
        self.dollar_risk_var.set(20)  # Default value
        self.dollar_risk_entry = tk.Entry(self.master, textvariable=self.dollar_risk_var)
        self.dollar_risk_entry.grid(row=4, column=2, pady=5)
        
        #3) ORDER VALUES: LOTS, STOPLOSS PIPS
        tk.Label(self.master, text="Lots:", bg="#0B0F15", fg="white").grid(row=5, column=0, pady=5)
        tk.Label(self.master, text="$ Risk", bg="#0B0F15", fg="white").grid(row=5, column=1, pady=5)
        tk.Label(self.master, text="SL", bg="#0B0F15", fg="white").grid(row=5, column=2, pady=5)
        
        self.lots_var = tk.DoubleVar()
        self.lots_var.set(1)  # Default value
        self.lots_entry = tk.Entry(self.master, textvariable=self.lots_var)
        self.lots_entry.grid(row=6, column=0, pady=5)

        self.dollar_risk_var = tk.DoubleVar()
        self.dollar_risk_var.set(20)  # Default value
        self.dollar_risk_entry = tk.Entry(self.master, textvariable=self.dollar_risk_var)
        self.dollar_risk_entry.grid(row=6, column=1, pady=5)

        self.percent_risk_var = tk.DoubleVar()
        self.percent_risk_var.set(5)  # Default value
        self.percent_risk_entry = tk.Entry(self.master, textvariable=self.percent_risk_var)
        self.percent_risk_entry.grid(row=6, column=2, pady=5)
        
        #4) ORDER BUY,SQUARE OFF, EXIT ALL BUTTON
        tk.Button(self.master, text="BUY CALL", command=self.get_options_chain, bg="green", fg="white").grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="BUY PUT", command=self.place_order, bg="green", fg="white").grid(row=7, column=1, columnspan=2, pady=10) 
        tk.Button(self.master, text="Square Off", command=self.get_options_chain, bg="blue", fg="white").grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Exit All", command=self.place_order, bg="red", fg="white").grid(row=8, column=1, columnspan=2, pady=10)
        
        #5) OPTIONS CHAIN TABLE/TREE with Colums and rows like below
        # CALL                    PUT
        # CALL OI LTP  STRIKE IV  LTP PUT OI
        options_chain_tree = ttk.Treeview(self.master)
        options_chain_tree["columns"] = ("Call_OI", "Call_LTP", "PCR", "Strike", "IV", "Put_LTP", "Put_OI")
        options_chain_tree.heading("Call_OI", text="Call OI")
        options_chain_tree.heading("Call_LTP", text="Call LTP")
        options_chain_tree.heading("PCR", text="PCR")
        options_chain_tree.heading("Strike", text="Strike")
        options_chain_tree.heading("IV", text="IV")
        options_chain_tree.heading("Put_LTP", text="Put LTP")
        options_chain_tree.heading("Put_OI", text="Put OI")
        
        options_chain_tree.column("Call_OI", minwidth=0, width=70, stretch=tk.NO)
        options_chain_tree.column("Call_LTP", minwidth=0, width=70, stretch=tk.NO)       
        options_chain_tree.column("PCR", minwidth=0, width=70, stretch=tk.NO)
        options_chain_tree.column("Strike", minwidth=0, width=70, stretch=tk.NO)
        options_chain_tree.column("IV", minwidth=0, width=70, stretch=tk.NO)
        options_chain_tree.column("Put_LTP", minwidth=0, width=70, stretch=tk.NO)
        options_chain_tree.column("Put_OI", minwidth=0, width=70, stretch=tk.NO)
        
        options_chain_tree.grid(row=9, column=0, columnspan=3)

        # Get the current strike price (replace with actual logic to get the strike price)
        current_strike = 150

        # Inserting rows for two strikes above and below the current strike
        for i in range(2, -3, -1):  # Two above and two below
            strike = current_strike + i * 10  # You can adjust the step size as needed
            options_chain_tree.insert("", tk.END, values=(f"1234{i}", f"100{i}", f"{strike}", f"20{i}", f"200{i}", f"120{i}"))

       

    #icicidirect breeze api widgets
    def get_options_chain(self):
        # Implement this method to retrieve options chain data
        symbol = self.symbol_var.get()
        expiry_date = self.expiry_date_var.get()
        # Add code to fetch options chain data using self.breeze

    def place_order(self):
        # Implement this method to place an order
        symbol = self.symbol_var.get()
        lots = self.lots_var.get()
        dollar_risk = self.dollar_risk_var.get()
        percent_risk = self.percent_risk_var.get()
        # Add code to place an order using self.breeze

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("670x500")
    app = TradingTerminal(root)
    root.mainloop()
