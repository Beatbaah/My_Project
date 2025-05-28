import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import random

class RevenueCollectionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Revenue Collection System")
        self.root.geometry("800x600")

        # Initialize database
        self.init_database()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        # Create tabs
        self.taxpayer_tab = ttk.Frame(self.notebook)
        self.bills_tab = ttk.Frame(self.notebook)
        self.receipts_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.taxpayer_tab, text="Taxpayer Management")
        self.notebook.add(self.bills_tab, text="Tax Bills")
        self.notebook.add(self.receipts_tab, text="Receipts")
        
        self.setup_taxpayer_tab()
        self.setup_bills_tab()
        self.setup_receipts_tab()

    def init_database(self):
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        
        # Create taxpayers table
        c.execute('''CREATE TABLE IF NOT EXISTS taxpayers
                    (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     address TEXT,
                     phone TEXT,
                     type TEXT)''')
        
        # Create bills table
        c.execute('''CREATE TABLE IF NOT EXISTS bills
                    (id INTEGER PRIMARY KEY,
                     taxpayer_id INTEGER,
                     bill_type TEXT,
                     amount REAL,
                     date TEXT,
                     status TEXT,
                     FOREIGN KEY (taxpayer_id) REFERENCES taxpayers (id))''')
        
        # Create receipts table
        c.execute('''CREATE TABLE IF NOT EXISTS receipts
                    (id INTEGER PRIMARY KEY,
                     bill_id INTEGER,
                     amount_paid REAL,
                     payment_date TEXT,
                     receipt_number TEXT,
                     FOREIGN KEY (bill_id) REFERENCES bills (id))''')
        
        conn.commit()
        conn.close()

    def setup_taxpayer_tab(self):
        # Taxpayer input frame
        input_frame = ttk.LabelFrame(self.taxpayer_tab, text="Add Taxpayer")
        input_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, pady=5, padx=5)
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Address:").grid(row=1, column=0, pady=5, padx=5)
        self.address_entry = ttk.Entry(input_frame)
        self.address_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Phone:").grid(row=2, column=0, pady=5, padx=5)
        self.phone_entry = ttk.Entry(input_frame)
        self.phone_entry.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Type:").grid(row=3, column=0, pady=5, padx=5)
        self.type_combo = ttk.Combobox(input_frame, values=["Individual", "Business"])
        self.type_combo.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Button(input_frame, text="Add Taxpayer", command=self.add_taxpayer).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Taxpayer list
        list_frame = ttk.LabelFrame(self.taxpayer_tab, text="Taxpayer List")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.taxpayer_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Address", "Phone", "Type"), show="headings")
        self.taxpayer_tree.heading("ID", text="ID")
        self.taxpayer_tree.heading("Name", text="Name")
        self.taxpayer_tree.heading("Address", text="Address")
        self.taxpayer_tree.heading("Phone", text="Phone")
        self.taxpayer_tree.heading("Type", text="Type")
        
        self.taxpayer_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        ttk.Button(list_frame, text="Delete Selected", command=self.delete_taxpayer).pack(pady=5)
        
        self.load_taxpayers()

    def setup_bills_tab(self):
        # Bill creation frame
        input_frame = ttk.LabelFrame(self.bills_tab, text="Create Bill")
        input_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(input_frame, text="Taxpayer:").grid(row=0, column=0, pady=5, padx=5)
        self.bill_taxpayer_combo = ttk.Combobox(input_frame)
        self.bill_taxpayer_combo.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Bill Type:").grid(row=1, column=0, pady=5, padx=5)
        self.bill_type_combo = ttk.Combobox(input_frame, values=["Property Rate", "Business Tax", "Other"])
        self.bill_type_combo.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Amount:").grid(row=2, column=0, pady=5, padx=5)
        self.bill_amount_entry = ttk.Entry(input_frame)
        self.bill_amount_entry.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Button(input_frame, text="Generate Bill", command=self.generate_bill).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Bills list
        list_frame = ttk.LabelFrame(self.bills_tab, text="Bills List")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.bills_tree = ttk.Treeview(list_frame, columns=("ID", "Taxpayer", "Type", "Amount", "Date", "Status"), show="headings")
        self.bills_tree.heading("ID", text="ID")
        self.bills_tree.heading("Taxpayer", text="Taxpayer")
        self.bills_tree.heading("Type", text="Type")
        self.bills_tree.heading("Amount", text="Amount")
        self.bills_tree.heading("Date", text="Date")
        self.bills_tree.heading("Status", text="Status")
        
        self.bills_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.load_bills()
        self.update_taxpayer_combo()

    def setup_receipts_tab(self):
        # Receipt creation frame
        input_frame = ttk.LabelFrame(self.receipts_tab, text="Generate Receipt")
        input_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(input_frame, text="Bill ID:").grid(row=0, column=0, pady=5, padx=5)
        self.receipt_bill_entry = ttk.Entry(input_frame)
        self.receipt_bill_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Amount Paid:").grid(row=1, column=0, pady=5, padx=5)
        self.receipt_amount_entry = ttk.Entry(input_frame)
        self.receipt_amount_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Button(input_frame, text="Generate Receipt", command=self.generate_receipt).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Receipts list
        list_frame = ttk.LabelFrame(self.receipts_tab, text="Receipts List")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.receipts_tree = ttk.Treeview(list_frame, columns=("ID", "Bill ID", "Amount", "Date", "Receipt No."), show="headings")
        self.receipts_tree.heading("ID", text="ID")
        self.receipts_tree.heading("Bill ID", text="Bill ID")
        self.receipts_tree.heading("Amount", text="Amount")
        self.receipts_tree.heading("Date", text="Date")
        self.receipts_tree.heading("Receipt No.", text="Receipt No.")
        
        self.receipts_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.load_receipts()

    def add_taxpayer(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        type_ = self.type_combo.get()
        
        if not all([name, address, phone, type_]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        c.execute("INSERT INTO taxpayers (name, address, phone, type) VALUES (?, ?, ?, ?)",
                 (name, address, phone, type_))
        conn.commit()
        conn.close()
        
        self.load_taxpayers()
        self.update_taxpayer_combo()
        
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.type_combo.set('')

    def delete_taxpayer(self):
        selected_item = self.taxpayer_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a taxpayer to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this taxpayer?"):
            taxpayer_id = self.taxpayer_tree.item(selected_item)['values'][0]
            
            conn = sqlite3.connect('revenue.db')
            c = conn.cursor()
            c.execute("DELETE FROM taxpayers WHERE id=?", (taxpayer_id,))
            conn.commit()
            conn.close()
            
            self.load_taxpayers()
            self.update_taxpayer_combo()

    def generate_bill(self):
        taxpayer = self.bill_taxpayer_combo.get()
        bill_type = self.bill_type_combo.get()
        amount = self.bill_amount_entry.get()
        
        if not all([taxpayer, bill_type, amount]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return
        
        taxpayer_id = taxpayer.split('-')[0].strip()
        
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        c.execute("INSERT INTO bills (taxpayer_id, bill_type, amount, date, status) VALUES (?, ?, ?, ?, ?)",
                 (taxpayer_id, bill_type, amount, datetime.now().strftime("%Y-%m-%d"), "Unpaid"))
        conn.commit()
        conn.close()
        
        self.load_bills()
        
        # Clear entries
        self.bill_taxpayer_combo.set('')
        self.bill_type_combo.set('')
        self.bill_amount_entry.delete(0, tk.END)

    def generate_receipt(self):
        bill_id = self.receipt_bill_entry.get()
        amount_paid = self.receipt_amount_entry.get()
        
        if not all([bill_id, amount_paid]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            amount_paid = float(amount_paid)
            bill_id = int(bill_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
            return
        
        receipt_number = f"RCP-{random.randint(10000, 99999)}"
        
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        
        # Check if bill exists and get its amount
        c.execute("SELECT amount, status FROM bills WHERE id=?", (bill_id,))
        result = c.fetchone()
        
        if not result:
            messagebox.showerror("Error", "Bill not found!")
            conn.close()
            return
        
        bill_amount, status = result
        
        if status == "Paid":
            messagebox.showerror("Error", "This bill has already been paid!")
            conn.close()
            return
        
        if amount_paid < bill_amount:
            messagebox.showerror("Error", "Amount paid must be equal to or greater than the bill amount!")
            conn.close()
            return
        
        # Generate receipt
        c.execute("INSERT INTO receipts (bill_id, amount_paid, payment_date, receipt_number) VALUES (?, ?, ?, ?)",
                 (bill_id, amount_paid, datetime.now().strftime("%Y-%m-%d"), receipt_number))
        
        # Update bill status
        c.execute("UPDATE bills SET status='Paid' WHERE id=?", (bill_id,))
        
        conn.commit()
        conn.close()
        
        self.load_receipts()
        self.load_bills()
        
        # Clear entries
        self.receipt_bill_entry.delete(0, tk.END)
        self.receipt_amount_entry.delete(0, tk.END)

    def load_taxpayers(self):
        for item in self.taxpayer_tree.get_children():
            self.taxpayer_tree.delete(item)
        
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        c.execute("SELECT * FROM taxpayers")
        for row in c.fetchall():
            self.taxpayer_tree.insert('', 'end', values=row)
        conn.close()

    def load_bills(self):
        for item in self.bills_tree.get_children():
            self.bills_tree.delete(item)
        
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        c.execute("""
            SELECT bills.id, taxpayers.name, bills.bill_type, bills.amount, bills.date, bills.status
            FROM bills
            JOIN taxpayers ON bills.taxpayer_id = taxpayers.id
        """)
        for row in c.fetchall():
            self.bills_tree.insert('', 'end', values=row)
        conn.close()

    def load_receipts(self):
        for item in self.receipts_tree.get_children():
            self.receipts_tree.delete(item)
        
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        c.execute("SELECT * FROM receipts")
        for row in c.fetchall():
            self.receipts_tree.insert('', 'end', values=row)
        conn.close()

    def update_taxpayer_combo(self):
        conn = sqlite3.connect('revenue.db')
        c = conn.cursor()
        c.execute("SELECT id, name FROM taxpayers")
        taxpayers = [f"{row[0]} - {row[1]}" for row in c.fetchall()]
        conn.close()
        
        self.bill_taxpayer_combo['values'] = taxpayers

if __name__ == "__main__":
    root = tk.Tk()
    app = RevenueCollectionSystem(root)
    root.mainloop()