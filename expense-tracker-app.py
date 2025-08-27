import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

CSV_FILE = "expenses.csv"

# --- Data Handling ---
def load_expenses():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_expenses(df):
    df.to_csv(CSV_FILE, index=False)

# --- GUI Functions ---
def add_expense():
    date = date_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    desc = desc_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all required fields")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    new_entry = {"Date": date, "Category": category, "Amount": amount, "Description": desc}
    df = load_expenses()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_expenses(df)
    update_table()
    messagebox.showinfo("Success", "Expense added successfully!")

def update_table():
    for row in tree.get_children():
        tree.delete(row)
    df = load_expenses()
    for _, row in df.iterrows():
        tree.insert("", "end", values=(row["Date"], row["Category"], row["Amount"], row["Description"]))

def show_summary():
    df = load_expenses()
    if df.empty:
        messagebox.showinfo("Summary", "No expenses recorded yet.")
        return
    total = df["Amount"].sum()
    per_category = df.groupby("Category")["Amount"].sum()
    summary = f"Total Expenses: {total}\n\n" + per_category.to_string()
    messagebox.showinfo("Summary", summary)

def show_chart():
    df = load_expenses()
    if df.empty:
        messagebox.showinfo("Chart", "No expenses recorded yet.")
        return
    per_category = df.groupby("Category")["Amount"].sum()
    per_category.plot(kind="bar", figsize=(6,4))
    plt.title("Expenses by Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()

# --- GUI Setup ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("750x500")

# Input Frame
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

tk.Label(frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, sticky="w")
date_entry = tk.Entry(frame)
date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Category").grid(row=1, column=0, sticky="w")
category_var = tk.StringVar(value="Food")
category_menu = ttk.Combobox(frame, textvariable=category_var,
                             values=["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"])
category_menu.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Amount").grid(row=2, column=0, sticky="w")
amount_entry = tk.Entry(frame)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Description").grid(row=3, column=0, sticky="w")
desc_entry = tk.Entry(frame)
desc_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(frame, text="Add Expense", command=add_expense, bg="green", fg="white")
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Table Frame
columns = ("Date", "Category", "Amount", "Description")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(expand=True, fill="both", padx=10, pady=10)

# Action Buttons
btn_frame = tk.Frame(root, pady=10)
btn_frame.pack()

summary_btn = tk.Button(btn_frame, text="Show Summary", command=show_summary, bg="#007ACC", fg="white")
summary_btn.grid(row=0, column=0, padx=10)

chart_btn = tk.Button(btn_frame, text="Show Chart", command=show_chart, bg="#007ACC", fg="white")
chart_btn.grid(row=0, column=1, padx=10)

update_table()
root.mainloop()
