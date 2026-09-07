import tkinter as tk

class LoginSystemV1:
    def __init__(self):
        self.users = {}
    
    def register(self, username, password):
        self.users[username] = password
        return True
    
    def login(self, username, password):
        return self.users[username] == password

class LoginWindowV1:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("300x200")
        self.login_system = LoginSystemV1()
        self.authenticated = False
        
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=10)
        
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady=10)
        
        tk.Button(self.root, text="Login", 
                 command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.login_system.login(username, password):
            self.authenticated = True
            self.root.destroy()
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_system.register(username, password)
    
    def run(self):
        self.root.mainloop()
        return self.authenticated


if __name__ == "__main__":
    window = LoginWindowV1()
    window.run()