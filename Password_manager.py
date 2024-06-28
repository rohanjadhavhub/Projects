import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import string

class PasswordManager:
    def __init__(self, filename="passwords.json"):
        self.filename = filename
        self.passwords = self.load_passwords()

    def load_passwords(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_passwords(self):
        with open(self.filename, "w") as file:
            json.dump(self.passwords, file, indent=2)

    def add_password(self, account, password):
        self.passwords[account] = password
        self.save_passwords()

    def get_password(self, account):
        return self.passwords.get(account, "Account not found.")

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def list_accounts(self):
        return list(self.passwords.keys())

class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("400x300")
        self.pm = PasswordManager()

        self.create_widgets()

    def create_widgets(self):

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="Add Password")

        ttk.Label(self.add_frame, text="Account:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.account_entry = ttk.Entry(self.add_frame)
        self.account_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.add_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.add_frame, text="Add", command=self.add_password).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.add_frame, text="Generate Password", command=self.generate_password).grid(row=3, column=0, columnspan=2)

        self.get_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.get_frame, text="Get Password")

        ttk.Label(self.get_frame, text="Account:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.get_account_entry = ttk.Entry(self.get_frame)
        self.get_account_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.get_frame, text="Get Password", command=self.get_password).grid(row=1, column=0, columnspan=2, pady=10)

        self.password_var = tk.StringVar()
        ttk.Label(self.get_frame, textvariable=self.password_var).grid(row=2, column=0, columnspan=2, pady=5)

        self.list_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.list_frame, text="List Accounts")

        self.accounts_listbox = tk.Listbox(self.list_frame, width=40, height=10)
        self.accounts_listbox.pack(padx=5, pady=5, expand=True, fill="both")

        ttk.Button(self.list_frame, text="Refresh", command=self.list_accounts).pack(pady=5)

        self.list_accounts()

    def add_password(self):
        account = self.account_entry.get()
        password = self.password_entry.get()
        if account and password:
            self.pm.add_password(account, password)
            messagebox.showinfo("Success", f"Password for {account} has been added.")
            self.account_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.list_accounts()
        else:
            messagebox.showerror("Error", "Please enter both account and password.")

    def get_password(self):
        account = self.get_account_entry.get()
        if account:
            password = self.pm.get_password(account)
            self.password_var.set(f"Password: {password}")
        else:
            messagebox.showerror("Error", "Please enter an account name.")

    def generate_password(self):
        password = self.pm.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def list_accounts(self):
        self.accounts_listbox.delete(0, tk.END)
        for account in self.pm.list_accounts():
            self.accounts_listbox.insert(tk.END, account)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()