import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Load existing data or create new data
        self.data = self.load_data()
        self.current_month = None

        # GUI Elements
        self.label = tk.Label(root, text="Expense Tracker", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.select_month_button = tk.Button(root, text="Select Month", command=self.select_month)
        self.select_month_button.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=10)

        self.view_button = tk.Button(root, text="View Summary", command=self.view_summary)
        self.view_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.destroy)
        self.exit_button.pack(pady=10)

    def load_data(self):
        try:
            with open("expense_data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"expenses": []}

    def save_data(self):
        with open("expense_data.json", "w") as file:
            json.dump(self.data, file, indent=2)

    def select_month(self):
        year = self.get_user_input("Enter the year (YYYY):")
        if not year:
            return

        month = self.get_user_input("Enter the month (MM):")
        if not month:
            return

        self.current_month = f"{year}-{month}-01"

    def add_expense(self):
        if not self.current_month:
            messagebox.showinfo("Expense Tracker", "Please select a month first.")
            return

        amount = self.get_user_input("Enter the amount spent:")
        description = self.get_user_input("Enter a brief description:")
        category = self.get_user_input("Enter the category (food, transportation, entertainment, etc.):")
        date = self.current_month

        expense_details = {"amount": amount, "description": description, "category": category, "date": date}
        self.data["expenses"].append(expense_details)
        self.save_data()
        messagebox.showinfo("Expense Tracker", "Expense added successfully!")

    def view_summary(self):
        if not self.current_month:
            messagebox.showinfo("Expense Tracker", "Please select a month first.")
            return

        monthly_expenses = [expense for expense in self.data["expenses"] if expense["date"].startswith(self.current_month)]

        if not monthly_expenses:
            messagebox.showinfo("Expense Tracker", f"No expenses for {self.current_month}.")
            return

        total_spent = sum(float(expense["amount"]) for expense in monthly_expenses)

        summary_text = f"Total amount spent in {self.current_month}: ${total_spent:.2f}\n\nCategory-wise Expenditure:\n"

        categories = set(expense["category"] for expense in monthly_expenses)
        for category in categories:
            category_total = sum(float(expense["amount"]) for expense in monthly_expenses if expense["category"] == category)
            summary_text += f"{category}: ${category_total:.2f}\n"

        messagebox.showinfo("Expense Tracker - Summary", summary_text)

    def get_user_input(self, prompt):
        return simpledialog.askstring("Expense Tracker", prompt)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
