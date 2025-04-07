import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

# Set up the database if it doesn't already exist
def setup_database():
    conn = sqlite3.connect("customers.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birthday TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            preferred_contact TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to handle what happens when you click the Submit button
def submit_info():
    name = name_entry.get()
    birthday = birthday_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()
    contact_method = contact_method_box.get()

    # Make sure everything is filled out
    if not name or not birthday or not email or not phone or not address or contact_method == "Select":
        messagebox.showwarning("Missing Info", "Please fill out all fields.")
        return

    # Check if the email looks valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    # Check if the birthday is in the right format
    if not re.match(r"\d{4}-\d{2}-\d{2}", birthday):
        messagebox.showerror("Invalid Birthday", "Use this format: YYYY-MM-DD")
        return

    # Save the data to the database
    conn = sqlite3.connect("customers.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customers (name, birthday, email, phone, address, preferred_contact)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, birthday, email, phone, address, contact_method))
    conn.commit()
    conn.close()

    # Let the user know it worked
    messagebox.showinfo("Success", "Thanks! Your info was submitted.")

    # Clear the form for the next entry
    name_entry.delete(0, tk.END)
    birthday_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    contact_method_box.set("Select")

# Set up the database when the program starts
setup_database()

# Build the GUI
root = tk.Tk()
root.title("Customer Info Form")
root.geometry("400x450")

# Name
tk.Label(root, text="Full Name").pack()
name_entry = tk.Entry(root, width=40)
name_entry.pack()

# Birthday
tk.Label(root, text="Birthday (YYYY-MM-DD)").pack()
birthday_entry = tk.Entry(root, width=40)
birthday_entry.pack()

# Email
tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack()

# Phone
tk.Label(root, text="Phone Number").pack()
phone_entry = tk.Entry(root, width=40)
phone_entry.pack()

# Address
tk.Label(root, text="Address").pack()
address_entry = tk.Entry(root, width=40)
address_entry.pack()

# Preferred Contact Method
tk.Label(root, text="Preferred Contact Method").pack()
contact_method_box = ttk.Combobox(root, values=["Email", "Phone", "Mail"])
contact_method_box.set("Select")
contact_method_box.pack()

# Submit Button
tk.Button(root, text="Submit", command=submit_info, bg="lightgreen").pack(pady=15)

# Run the app
root.mainloop()