import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import hashlib
import re
from ursina import *
import math
import random
import winsound
import threading


class LoginSystemV3:
    def __init__(self):
        self.users_file = "users_v3.json" # File to store user accounts
        self.load_users()
    
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {} # Empty dict if file doesn't exist
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_username(self, username):
        if not username:
            return False, "Username is required"
        if len(username) < 6:
            return False, "Username must be at least 6 characters"
        if ' ' in username:
            return False, "Username cannot contain spaces"
        if username in self.users:
            return False, "Username already taken"
        return True, "Valid"
    
    def validate_password(self, password):
        if not password:
            return False, "Password is required"
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        special_chars = "!@#$%^&*(),.?\":{}|<>"
        if not any(c in special_chars for c in password):
            return False, "Password must contain a special character (!@#$%^&*...)"
        
        return True, "Valid"
    
    def register(self, username, password):
        valid, msg = self.validate_username(username)
        if not valid:
            return False, msg
        
        valid, msg = self.validate_password(password)
        if not valid:
            return False, msg
        
        self.users[username] = self.hash_password(password)
        self.save_users()
        return True, "Success"
    
    def login(self, username, password):
        stored = self.users.get(username)
        if stored is None:
            return False # Username doesn't exist
        return stored == self.hash_password(password)  # Compare hashed passwords


class LeaderboardSystem:
    def __init__(self):
        self.leaderboard_file = "leaderboard.json" # File to store scores
        self.load_leaderboard()
    
    def load_leaderboard(self):
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'r') as f:
                self.leaderboard = json.load(f) # Empty list if file doesn't exist
        else:
            self.leaderboard = []
    
    def save_leaderboard(self):
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.leaderboard, f, indent=2)
    
    def add_score(self, username, level, score, accuracy):
        entry = {
            "username": username,
            "level": level,
            "score": score,
            "accuracy": round(accuracy, 1) # Round to 1 decimal place
        }
        self.leaderboard.append(entry)
        self.save_leaderboard()
    
    def get_top_scores(self, level_filter=None, limit=10):
        # Filter by level if specified
        if level_filter is not None:
            scores = [e for e in self.leaderboard if e['level'] == level_filter]
        else:
            scores = self.leaderboard.copy() 
        
        # Sort by score (then accuracy if tied), highest first
        scores.sort(key=lambda x: (x['score'], x['accuracy']), reverse=True)
        return scores[:limit] # Return top N scores
    
    def get_user_best_scores(self, username):
        user_scores = [e for e in self.leaderboard if e['username'] == username]
        
         # Find best score per level
        best = {}
        for e in user_scores:
            lvl = e['level']
            if lvl not in best or e['score'] > best[lvl]['score']:
                best[lvl] = e
        
        # Convert to sorted list
        result = list(best.values())
        result.sort(key=lambda x: x['level'])
        return result


class LoginWindow:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Tuff Trace - Login")
        self.root.geometry("400x380")
        self.root.resizable(False, False)

        # Initialize login system

        self.login_system = LoginSystemV3()
        self.authenticated = False
        self.username = ""
        
        # Title label
        title = tk.Label(self.root, text="🎯 Tuff Trace", 
                        font=("Arial", 16, "bold"), fg="#2196F3")
        title.pack(pady=15)
        # Requirements display frame
        req_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=5)
        req_frame.pack(padx=20, fill="x")
        
        tk.Label(req_frame, text="Requirements:", 
                 font=("Arial", 9, "bold"), bg="#f0f0f0").pack(anchor="w")
        tk.Label(req_frame, 
                 text="• Username: 6+ chars, no spaces\n• Password: 8+ chars, 1 number, 1 special char",
                 font=("Arial", 8), bg="#f0f0f0", justify="left").pack(anchor="w")
        
        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack()
         # Username input
        tk.Label(frame, text="Username:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        self.username_entry.focus()
         # Password input
        tk.Label(frame, text="Password:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, show="●", width=25, font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        # Login button
        tk.Button(btn_frame, text="Login", command=self.login, 
                  width=12, bg="#4CAF50", fg="white", 
                  font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        # Register button
        tk.Button(btn_frame, text="Register", command=self.register, 
                  width=12, bg="#2196F3", fg="white",
                  font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        # Status message label
        self.status_label = tk.Label(self.root, text="", fg="gray", font=("Arial", 9))
        self.status_label.pack()
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Check if fields are filled
        if not username or not password:
            self.status_label.config(text="Please fill all fields", fg="red")
            return
         # Verify credentials
        if self.login_system.login(username, password):
            self.status_label.config(text="✓ Login successful!", fg="green")
            self.authenticated = True
            self.username = username
            self.root.after(500, self.root.destroy) # Close window after 0.5 seconds
        else:
            self.status_label.config(text="✗ Invalid credentials", fg="red")
            self.password_entry.delete(0, tk.END)  # Clear password field
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        success, msg = self.login_system.register(username, password)
        
        if success:
            self.status_label.config(text="✓ Registration successful! Please login.", fg="green")
            self.password_entry.delete(0, tk.END) # Clear password field
        else:
            self.status_label.config(text=f"✗ {msg}", fg="red")
    
    def run(self):
        self.root.mainloop()
        return self.authenticated


class MenuWindow:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("3D Aim Trainer - Menu")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        # Store username and initialize variables
        self.username = username
        self.selected_level = 1
        self.action = None
        self.leaderboard_system = LeaderboardSystem()
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Welcome message
        tk.Label(main_frame, text=f"Welcome, {username}!", 
                 font=("Arial", 18, "bold"), fg="#2196F3").pack(pady=10)
         # Level selection frame
        level_frame = tk.LabelFrame(main_frame, text="Select Level", 
                                    font=("Arial", 12, "bold"), 
                                    bg="#f0f0f0", padx=15, pady=10)
        level_frame.pack(fill="x", pady=10)
        
        self.level_var = tk.IntVar(value=1)
        # Create buttons for levels 1-10
        level_buttons_frame = tk.Frame(level_frame, bg="#f0f0f0")
        level_buttons_frame.pack(pady=10)
        
        for i in range(1, 11):
            btn = tk.Radiobutton(level_buttons_frame, text=f"Level {i}", 
                                variable=self.level_var, value=i,
                                font=("Arial", 10), bg="#f0f0f0",
                                selectcolor="#c0e0ff", padx=10, pady=5)
            btn.grid(row=(i-1)//5, column=(i-1)%5, padx=5, pady=5, sticky="w")
        
        tk.Button(main_frame, text="Start Game", command=self.start_game,
                  width=20, height=2, bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=15)
        
        lb_frame = tk.LabelFrame(main_frame, text="🏆 Leaderboard", 
                                 font=("Arial", 14, "bold"), fg="#FF9800",
                                 bg="#f0f0f0", padx=15, pady=10)
        lb_frame.pack(fill="both", expand=True, pady=10)
        # Filter controls
        filter_frame = tk.Frame(lb_frame, bg="#f0f0f0")
        filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter by Level:", 
                 font=("Arial", 10), bg="#f0f0f0").pack(side="left", padx=(0, 10))
        # Dropdown for level filter
        self.level_filter_var = tk.StringVar(value="All")
        level_filter_combo = ttk.Combobox(filter_frame, textvariable=self.level_filter_var,
                                          values=["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                          state="readonly", width=10)
        level_filter_combo.pack(side="left")
        level_filter_combo.bind("<<ComboboxSelected>>", self.refresh_leaderboard)
         # Scrollable text area for leaderboard
        lb_container = tk.Frame(lb_frame, bg="#f0f0f0")
        lb_container.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(lb_container)
        scrollbar.pack(side="right", fill="y")
        
        self.lb_text = tk.Text(lb_container, height=12, width=70, 
                               font=("Courier", 10), bg="white",
                               yscrollcommand=scrollbar.set, state="disabled")
        self.lb_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.lb_text.yview)
        # Load initial leaderboard

        self.refresh_leaderboard()
        
    def refresh_leaderboard(self, event=None):
        self.lb_text.config(state="normal")
        self.lb_text.delete("1.0", tk.END)
         # Get filter value
        filter_val = self.level_filter_var.get()
        level_filter = None if filter_val == "All" else int(filter_val)
         # Get top scores
        top_scores = self.leaderboard_system.get_top_scores(level_filter, limit=20)
        
        if top_scores:
            self.lb_text.insert("1.0", f"{'Rank':<6}{'Username':<15}{'Level':<8}{'Score':<10}{'Accuracy':<10}\n")
            self.lb_text.insert("2.0", "-" * 55 + "\n")
            
            for i, e in enumerate(top_scores, 1):
                self.lb_text.insert(tk.END, f"{i:<6}{e['username']:<15}{e['level']:<8}{e['score']:<10}{e['accuracy']}%\n")
        else:
            self.lb_text.insert("1.0", "No scores yet! Be the first to play!")
        
        self.lb_text.config(state="disabled")
        
    def start_game(self):
        self.selected_level = self.level_var.get()
        self.action = "start"
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()
        return self.action, self.selected_level


class TargetBall(Entity):
    def __init__(self, level):
        self.level = level
        # Size decreases with level 
        self.size = max(0.5, 1.2 - (level * 0.05))
        super().__init__(
            model='sphere',
            color=color.red,
            scale=self.size,
            collider='sphere'
        )
        # Speed increases with level
        self.speed = 2.5 + (level * 0.5)
        self.direction = Vec3(random.choice([-1, 1]), 0, random.choice([-1, 1]))
        self.position = Vec3(random.uniform(-6, 6), 1, random.uniform(8, 14))
        
        self.vertical_speed = 0.2 + (level * 0.15)
        self.vertical_direction = random.choice([-1, 1])
        self.base_height = 1
        self.vertical_range = 0.5 + (level * 0.2)
        # Random direction change timer
        self.change_timer = 0
        self.change_interval = random.uniform(1.0, max(0.5, 2.5 - (level * 0.1)))
        
    def update(self):
        """Update target position and handle boundary collisions"""
        dt = time.dt
        
        self.x += self.direction.x * self.speed * dt
        self.z += self.direction.z * self.speed * dt
        self.y += self.vertical_direction * self.vertical_speed * dt
        
        if abs(self.x) > 10:
            self.x = 10 if self.x > 0 else -10
            self.direction.x *= -1
        
        if self.z > 16 or self.z < 6:
            self.z = clamp(self.z, 6, 16)
            self.direction.z *= -1
        
        if self.y > self.base_height + self.vertical_range:
            self.y = self.base_height + self.vertical_range
            self.vertical_direction = -1
        elif self.y < self.base_height - self.vertical_range:
            self.y = self.base_height - self.vertical_range
            self.vertical_direction = 1
        
        self.change_timer += dt
        if self.change_timer >= self.change_interval:
            self.change_timer = 0
            self.change_interval = random.uniform(1.0, max(0.5, 2.5 - (self.level * 0.1)))
            
            if random.random() > 0.3:
                self.direction.x = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
                self.direction.z = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
                
                length = (self.direction.x**2 + self.direction.z**2)**0.5
                if length > 0:
                    self.direction.x = (self.direction.x / length) * random.uniform(0.8, 1.2)
                    self.direction.z = (self.direction.z / length) * random.uniform(0.8, 1.2)
            
            if random.random() > 0.5:
                self.vertical_direction *= -1
            
            if self.level > 3 and random.random() > 0.6:
                self.speed = (2.5 + (self.level * 0.5)) * random.uniform(0.7, 1.3)


class GameController(Entity):
    def __init__(self, starting_level=1, username="Player"):
        super().__init__()
        
        self.game_started = False
        self.username = username
        self.level = starting_level
        self.score = 0
        # Required scores for each level (Level 1-10)
        self.required_scores = [40000, 40000, 35000, 30000, 30000, 25000, 22500, 20000, 19500, 16000]
        self.tracking = False
        # Timer (25 seconds per level)
        self.level_time = 25
        self.time_remaining = self.level_time
        
        self.total_tracking_time = 0 # Time spent hitting target
        self.possible_tracking_time = 0 # Time spent shooting
        self.accuracy = 0.0
        
        self.hit_sound_timer = 0
        self.hit_sound_interval = 0.05 # Play beep every 0.05 seconds
        self.last_hit_state = False
        # Leaderboard system
        self.leaderboard_system = LeaderboardSystem()
        # Camera setup
        self.camera_pivot = Entity()
        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 90
        # Create target
        self.target = TargetBall(self.level)
        # Weapon model (3 parts)
        self.laser_pointer = Entity(
            model='cube',
            color=color.black,
            scale=(0.15, 0.15, 0.5),
            position=(0.3, -0.2, 0.5),
            rotation=(0, 0, 0),
            parent=camera
        )
        self.laser_barrel = Entity(model='cube', color=color.black, scale=(0.08, 0.08, 0.3),
                                   position=(0, 0, 0.4), parent=self.laser_pointer)
        self.laser_tip = Entity(model='cube', color=color.black, scale=(0.1, 0.1, 0.05),
                                position=(0, 0, 0.55), parent=self.laser_pointer)
        # Laser beam

        self.laser = Entity(model='cube', color=color.rgba(255, 255, 0, 200),
                            scale=(0.02, 0.02, 200), visible=False, unlit=True)
        self.laser_dot = Entity(model='sphere', color=color.yellow,
                                scale=0.2, visible=False, unlit=True)
        # HUD text (top of screen)
        self.info_text = Text(
            text=f'Level: {self.level} | Score: {self.score}/{self.required_scores[self.level-1]} | Accuracy: {self.accuracy:.1f}% | Time: {int(self.time_remaining)}s',
            position=(-0.85, 0.45),
            scale=1.8,
            color=color.white
        )
        self.message_text = Text(text='', position=(0, 0), scale=3,
                                 color=color.yellow, origin=(0, 0))
        self.crosshair = Entity(model='quad', scale=0.01, color=color.white,
                                parent=camera.ui, z=-1)
        
    def play_beep(self, freq=800, dur=50): # Creates the beep sound, the parameterts freq and dur change the frequency and duration of the sound
        def beep():
            try:
                winsound.Beep(freq, dur) # Winsound only works on windows 
            except:
                pass
        threading.Thread(target=beep, daemon=True).start()
        
    def input(self, key):
        if key == 'escape':
            mouse.locked = False
            application.quit()
    
    def update(self):
        # Start game on first mouse click
        if not self.game_started and held_keys['left mouse']:
            self.game_started = True
        
        if self.time_remaining > 0 and self.game_started:
             # Countdown timer
            self.time_remaining -= time.dt
            # Laser shooting
            if held_keys['left mouse']:
                self.possible_tracking_time += time.dt
            
            self.camera_pivot.rotation_y += mouse.velocity[0] * 40
            self.camera_pivot.rotation_x -= mouse.velocity[1] * 40
            self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -80, 80)
            
            if held_keys['left mouse']:
                ray = raycast(camera.world_position, camera.forward, distance=200,
                              ignore=[self.laser_pointer, self.laser_barrel, self.laser_tip])
                
                if ray.hit:
                    laser_origin = self.laser_tip.world_position
                    hit_point = ray.world_point
                    beam_vec = hit_point - laser_origin
                    beam_len = beam_vec.length()
                    
                    self.laser.visible = True
                    self.laser.position = laser_origin + beam_vec * 0.5
                    self.laser.look_at(hit_point)
                    self.laser.scale = (0.02, 0.02, beam_len)
                    
                    self.laser_dot.visible = True
                    self.laser_dot.position = hit_point
                    # Check if hitting target
                    if ray.entity == self.target:
                        if not self.tracking:
                            self.tracking = True
                            self.last_hit_state = True
                            self.play_beep(1000, 50)
                        # Track time and add score
                        self.total_tracking_time += time.dt
                        self.score += 3 # 3 points per frame
                        self.laser.color = color.rgba(0, 255, 0, 200)
                        
                        self.hit_sound_timer += time.dt
                        if self.hit_sound_timer >= self.hit_sound_interval:
                            self.play_beep(random.randint(900, 1100), 30)
                            self.hit_sound_timer = 0
                    else:
                        # Missing target
                        self.tracking = False
                        self.last_hit_state = False
                        self.hit_sound_timer = 0
                        self.laser.color = color.rgba(255, 255, 0, 200)
                else:
                    # No hit - extend laser into distance
                    laser_origin = self.laser_tip.world_position
                    far_point = camera.world_position + camera.forward * 200
                    beam_vec = far_point - laser_origin
                    
                    self.laser.visible = True
                    self.laser.position = laser_origin + beam_vec * 0.5
                    self.laser.look_at(far_point)
                    self.laser.scale = (0.02, 0.02, 200)
                    self.laser.color = color.rgba(255, 255, 0, 200)
                    self.laser_dot.visible = False
                    self.tracking = False
            else:
                # Not shooting - hide laser
                self.laser.visible = False
                self.laser_dot.visible = False
                self.tracking = False
                self.hit_sound_timer = 0
            # Calculate accuracy
            if self.possible_tracking_time > 0:
                self.accuracy = (self.total_tracking_time / self.possible_tracking_time) * 100
            
            self.info_text.text = f'Level: {self.level} | Score: {self.score}/{self.required_scores[self.level-1]} | Accuracy: {self.accuracy:.1f}% | Time: {int(self.time_remaining)}s'
        # LEVEL END (time ran out)
        elif self.game_started:
            self.laser.visible = False
            self.laser_dot.visible = False
            # Check if level passed
            if self.score >= self.required_scores[self.level - 1]:
                self.leaderboard_system.add_score(self.username, self.level, self.score, self.accuracy)
                # Check if final level
                if self.level < 10:
                    # Show level complete message
                    self.message_text.text = f"LEVEL {self.level} COMPLETE!\nScore: {self.score} | Accuracy: {self.accuracy:.1f}%\nPress SPACE for next level"
                    # Advance to next level on SPACE
                    if held_keys['space']:
                        self.level += 1
                        self.score = 0
                        self.total_tracking_time = 0
                        self.possible_tracking_time = 0
                        self.accuracy = 0.0
                        self.time_remaining = self.level_time
                        self.game_started = False
                        self.message_text.text = ''
                        destroy(self.target)
                        self.target = TargetBall(self.level)
                else:
                    self.message_text.text = f"GAME COMPLETED!\nFinal Score: {self.score} | Accuracy: {self.accuracy:.1f}%\nPress ESC to exit"
            else:
                self.message_text.text = f"LEVEL {self.level} FAILED!\nScore: {self.score}/{self.required_scores[self.level-1]} | Accuracy: {self.accuracy:.1f}%\nPress SPACE to retry"
                if held_keys['space']:
                    self.score = 0
                    self.total_tracking_time = 0
                    self.possible_tracking_time = 0
                    self.accuracy = 0.0
                    self.time_remaining = self.level_time
                    self.game_started = False
                    self.message_text.text = ''
                    destroy(self.target)
                    self.target = TargetBall(self.level)


def start_game(starting_level=1, username="Player"):
    """Initialize and run the game"""
    app = Ursina()
    # Window settings
    window.title = "3D Aim Trainer"
    window.borderless = False
    window.fullscreen = False
    window.exit_button.visible = False
    
    Sky()
    
    ground = Entity(
        model='plane',
        color=color.rgb(139, 90, 60),
        scale=200,
        position=(0, -5, 0)
    )
    
    DirectionalLight(y=10, z=10, rotation=(45, -45, 0), shadows=True)
    AmbientLight(color=color.rgba(200, 200, 200, 255))
    
    mouse.locked = True
    game_controller = GameController(starting_level, username)
    app.run()


if __name__ == "__main__":
    login_window = LoginWindow()
    authenticated = login_window.run()
    # Step 1: Login
    if authenticated:
        # Get username from login
        username = login_window.username
        # Step 2: Menu and level selection
        menu_window = MenuWindow(username)
        action, selected_level = menu_window.run()
         # Step 3: Start game if user clicked start
        if action == "start":
            start_game(selected_level, username)
    else:
        print("Login failed or cancelled")