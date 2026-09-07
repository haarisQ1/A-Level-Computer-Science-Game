import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib
import re

class LoginSystemV3:
    def __init__(self):
        self.users_file = "users_v3.json"
        self.load_users()
    
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_username(self, username):
        """Validates username requirements"""
        # Presence check
        if not username:
            return False, "Username is required"
        
        # Length check (min 6 characters)
        if len(username) < 6:
            return False, "Username must be at least 6 characters"
        
        # Space check
        if ' ' in username:
            return False, "Username cannot contain spaces"
        
        # Check if username already exists
        if username in self.users:
            return False, "Username already taken"
        
        return True, "Valid"
    
    def validate_password(self, password):
        """Validates password requirements"""
        # Presence check
        if not password:
            return False, "Password is required"
        
        # Length check (min 8 characters)
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Check for at least one number
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain a special character (!@#$%^&*...)"
        
        return True, "Valid"
    
    def register(self, username, password):
        # Validate username
        valid, message = self.validate_username(username)
        if not valid:
            return False, message
        
        # Validate password
        valid, message = self.validate_password(password)
        if not valid:
            return False, message
        
        # Store hashed password
        self.users[username] = self.hash_password(password)
        self.save_users()
        return True, "Success"
    
    def login(self, username, password):
        stored_hash = self.users.get(username)
        if stored_hash is None:
            return False
        return stored_hash == self.hash_password(password)

class LoginWindowV3:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tuff Trace")
        self.root.geometry("400x380")
        self.root.resizable(False, False)
        self.login_system = LoginSystemV3()
        self.authenticated = False
        
        title = tk.Label(self.root, text="🎯 Tuff Trace - Login", 
                        font=("Arial", 16, "bold"), fg="#2196F3")
        title.pack(pady=15)
        
        # Requirements info
        req_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=5)
        req_frame.pack(padx=20, fill="x")
        
        req_title = tk.Label(req_frame, text="Requirements:", 
                            font=("Arial", 9, "bold"), bg="#f0f0f0")
        req_title.pack(anchor="w")
        
        req_text = tk.Label(req_frame, 
                           text="• Username: 6+ chars, no spaces\n• Password: 8+ chars, 1 number, 1 special char",
                           font=("Arial", 8), bg="#f0f0f0", justify="left")
        req_text.pack(anchor="w")
        
        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack()
        
        tk.Label(frame, text="Username:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        self.username_entry.focus()
        
        tk.Label(frame, text="Password:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, show="●", width=25, font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        login_btn = tk.Button(btn_frame, text="Login", command=self.login, 
                             width=12, bg="#4CAF50", fg="white", 
                             font=("Arial", 10, "bold"))
        login_btn.grid(row=0, column=0, padx=5)
        
        register_btn = tk.Button(btn_frame, text="Register", command=self.register, 
                                width=12, bg="#2196F3", fg="white",
                                font=("Arial", 10, "bold"))
        register_btn.grid(row=0, column=1, padx=5)
        
        self.status_label = tk.Label(self.root, text="", fg="gray", font=("Arial", 9))
        self.status_label.pack()
        
        self.root.bind('<Return>', lambda e: self.login())
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="Please fill all fields", fg="red")
            return
        
        if self.login_system.login(username, password):
            self.status_label.config(text="✓ Login successful!", fg="green")
            self.root.after(500, self.root.destroy)
            self.authenticated = True
        else:
            self.status_label.config(text="✗ Invalid credentials", fg="red")
            self.password_entry.delete(0, tk.END)
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        success, message = self.login_system.register(username, password)
        
        if success:
            self.status_label.config(text="✓ Registration successful! Please login.", fg="green")
            self.password_entry.delete(0, tk.END)
        else:
            self.status_label.config(text=f"✗ {message}", fg="red")
    
    def run(self):
        self.root.mainloop()
        return self.authenticated


if __name__ == "__main__":
    window = LoginWindowV3()
    window.run()