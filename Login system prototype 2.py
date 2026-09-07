import tkinter as tk
from tkinter import messagebox
import json
import os

class LoginSystemV2:
    def __init__(self):
        self.users_file = "users_v2.json"
        self.load_users()
    
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
    
    def register(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True
    
    def login(self, username, password):
        return self.users.get(username) == password

class LoginWindowV2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("300x250")
        self.login_system = LoginSystemV2()
        self.authenticated = False
        
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.login_system.login(username, password):
            self.authenticated = True
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if self.login_system.register(username, password):
            messagebox.showinfo("Success", "Registered! Please login.")
        else:
            messagebox.showerror("Error", "Username exists")
    
    def run(self):
        self.root.mainloop()
        return self.authenticated


if __name__ == "__main__":
    window = LoginWindowV2()
    window.run()