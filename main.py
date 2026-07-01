import tkinter as tk
import random
import asyncio

# ==========================================
# --- CONSTANTS & CONFIGURATION ------------
# ==========================================
WIDTH = 1300
HEIGHT = 600
GRAVITY = 1.5
FLAP_STRENGTH = -15
PIPE_SPEED_START = 8
PIPE_GAP = 160
PIPE_SPAWN_RATE = 90  # Frames between pipe spawns (~1.5 seconds)

class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Classy Flappy Bird")
        
        # Default Background Color
        self.bg_color = "skyblue"
        
        # Create Canvas Window
        self.window = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=self.bg_color)
        self.window.pack()
        
        # Game State Variables
        self.game_started = False
        self.game_running = False
        self.score = 0
        self.high_score = 0
        self.bird_velocity = 0
        self.pipe_speed = PIPE_SPEED_START
        self.spawn_timer = 0
        
        # Tracks unique pipe IDs that have awarded points
        self.passed_pipes = set()
        
        # Initialize the GUI Menu Screen
        self.show_start_screen()
        
        # Bind Controls (Space to flap/start, P to pause, R to reset)
        self.root.bind("<space>", self.flap)
        self.root.bind("<r>", self.restart_game)
        self.root.bind("<p>", self.toggle_pause)

    # ==========================================
    # --- VISUALS: MENU & INTERFACE ------------
    # ==========================================
    def show_start_screen(self):
        self.window.delete("all")
        
        # Title and Keybind Instructions on Canvas
        self.window.create_text(WIDTH/2, HEIGHT/3, text="FLAPPY BIRD", font=("Helvetica", 64, "bold"), fill="white", tag="menu")
        self.window.create_text(WIDTH/2, HEIGHT/2 - 20, text="Press SPACE to Flap & Start", font=("Helvetica", 24), fill="white", tag="menu")
        self.window.create_text(WIDTH/2, HEIGHT/2 + 20, text="Press P to Pause | Press R to Reset", font=("Helvetica", 16), fill="lightgray", tag="menu")
        
        # Color Menu Label
        self.window.create_text(WIDTH/2, HEIGHT - 120, text="Select Background Color:", font=("Helvetica", 16, "bold"), fill="white", tag="menu")
        
        # Interactive Color Buttons
        colors = ["skyblue", "pink", "lightblue", "black", "darkblue"]
        self.btn_frame = tk.Frame(self.root, bg=self.bg_color)
        self.window.create_window(WIDTH/2, HEIGHT - 70, window=self.btn_frame)
        
        for c in colors:
            btn = tk.Button(self.btn_frame, text=c.capitalize(), bg=c, fg="white" if c in ["black", "darkblue"] else "black",
                            command=lambda col=c: self.change_background(col))
            btn.pack(side=tk.LEFT, padx=5)

    def change_background(self, color):
        self.bg_color = color
        self.window.config(bg=color)
        if self.btn_frame.winfo_exists():
            self.btn_frame.config(bg=color)

    # ==========================================
    # --- GAME ENGINE ROOT & START LOGIC -------
    # ==========================================
    def start_game(self):
        if self.btn_frame.winfo_exists():
            self.btn_frame.destroy()  # Clean up menu button frame
            
        self.window.delete("menu")
        self.game_started = True
        self.game_running = True
        self.score = 0
        self.pipe_speed = PIPE_SPEED_START
        self.passed_pipes.clear()
        
        # Give the bird an instant upward boost right on launch so it doesn't drop immediately!
        self.bird_velocity = FLAP_STRENGTH  
        
        self.create_bird()
        self.text()
        self.game_loop()

    def create_bird(self):
        self.window.delete("bird")
        
        # 1. 3D Drop Shadow underneath the bird
        self.window.create_oval(198, 305, 258, 365, fill="#404040", outline="", tag="bird")
        
        # 2. Main Spherical 3D Body (Uses an orange-to-yellow nested overlay trick for a 3D gradient illusion)
        self.window.create_oval(200, 300, 260, 360, fill="#de9600", outline="black", width=2, tag="bird")
        self.window.create_oval(203, 303, 255, 355, fill="#ffb703", outline="", tag="bird")
        self.window.create_oval(208, 305, 245, 340, fill="#ffd166", outline="", tag="bird") # Light Highlight
        
        # 3. 3D Highlight Belly Patch
        self.window.create_oval(205, 335, 245, 358, fill="#fff3b0", outline="", tag="bird")
        
        # 4. Deep 3D Eye & Pupil with Glossy reflection
        self.window.create_oval(230, 308, 254, 332, fill="white", outline="black", width=2, tag="bird") 
        self.window.create_oval(242, 314, 252, 326, fill="black", outline="", tag="bird")
        self.window.create_oval(244, 316, 248, 320, fill="white", outline="", tag="bird") # Eye Specular Highlight
        
        # 5. Extruded Beak
        self.window.create_polygon(252, 324, 278, 331, 252, 338, fill="#e65c00", outline="black", width=2, tag="bird")
        self.window.create_polygon(252, 330, 272, 331, 252, 336, fill="#ff751a", outline="", tag="bird") # Beak highlight
        
        # 6. Layered 3D Wing
        self.window.create_oval(210, 325, 238, 350, fill="#d48800", outline="black", tag="bird")
        self.window.create_oval(213, 327, 235, 346, fill="#ffb703", outline="", tag="bird")

    # Master Game Loop running seamlessly at 60 updates/sec (~16ms)
    def game_loop(self):
        if not self.game_running:
            return

        # Handle Pipe Spawning Clocks
        self.spawn_timer += 1
        if self.spawn_timer >= PIPE_SPAWN_RATE:
            self.spawn_pipe()
            self.spawn_timer = 0

        # Core Game Stages
        self.move_pipes()
        self.apply_gravity()
        self.check_collision()
        self.check_score()

        self.window.after(16, self.game_loop)

    # ==========================================
    # --- MECHANICS & MOVEMENT -----------------
    # ==========================================
    def flap(self, event):
        if not self.game_started:
            self.start_game()
            return
        if self.game_running:
            self.bird_velocity = FLAP_STRENGTH

    def apply_gravity(self):
        self.bird_velocity += GRAVITY
        self.window.move("bird", 0, self.bird_velocity)

    def spawn_pipe(self):
        space = random.randint(100, HEIGHT - PIPE_GAP - 100)
        pipe_id = f"pipe_{random.randint(0, 100000)}"  # Unique structural tag name
        pipe_width = 70
        cap_height = 25
        cap_outset = 6 # How much wider the lip/cap is than the pipe shaft
        
        # --- TOP PIPE ---
        # Main Top Shaft
        self.window.create_rectangle(WIDTH, 0, WIDTH + pipe_width, space - cap_height, fill="#00a825", outline="black", width=2, tag=("pipe", pipe_id))
        # Top Shaft 3D Highlight Layer
        self.window.create_rectangle(WIDTH + 8, 0, WIDTH + 22, space - cap_height, fill="#00db34", outline="", tag=("pipe", pipe_id))
        # Top Rim/Cap Lip
        self.window.create_rectangle(WIDTH - cap_outset, space - cap_height, WIDTH + pipe_width + cap_outset, space, fill="#00a825", outline="black", width=2, tag=("pipe", pipe_id))
        # Top Rim 3D Highlight Layer
        self.window.create_rectangle(WIDTH - cap_outset + 8, space - cap_height + 2, WIDTH + 22, space - 2, fill="#00db34", outline="", tag=("pipe", pipe_id))
        
        # --- BOTTOM PIPE ---
        # Bottom Rim/Cap Lip
        self.window.create_rectangle(WIDTH - cap_outset, space + PIPE_GAP, WIDTH + pipe_width + cap_outset, space + PIPE_GAP + cap_height, fill="#00a825", outline="black", width=2, tag=("pipe", pipe_id))
        # Bottom Rim 3D Highlight Layer
        self.window.create_rectangle(WIDTH - cap_outset + 8, space + PIPE_GAP + 2, WIDTH + 22, space + PIPE_GAP + cap_height - 2, fill="#00db34", outline="", tag=("pipe", pipe_id))
        # Main Bottom Shaft
        self.window.create_rectangle(WIDTH, space + PIPE_GAP + cap_height, WIDTH + pipe_width, HEIGHT, fill="#00a825", outline="black", width=2, tag=("pipe", pipe_id))
        # Bottom Shaft 3D Highlight Layer
        self.window.create_rectangle(WIDTH + 8, space + PIPE_GAP + cap_height, WIDTH + 22, HEIGHT, fill="#00db34", outline="", tag=("pipe", pipe_id))

    def move_pipes(self):
        self.window.move("pipe", -self.pipe_speed, 0)
        
        # Cleanup routine for stray offscreen nodes
        for pipe in self.window.find_withtag("pipe"):
            coords = self.window.coords(pipe)
            if coords and coords[2] < -20: # Slightly expanded boundary to handle wider pipe caps safely
                self.window.delete(pipe)

    # ==========================================
    # --- COLLISION, PAUSE, & RESET LOGIC -----
    # ==========================================
    def check_collision(self):
        bird_coords = self.window.coords("bird")
        if not bird_coords:
            self.game_over()
            return
            
        # Standardize collision box against the main body layer coordinates
        b_x1, b_y1, b_x2, b_y2 = bird_coords[0], bird_coords[1], bird_coords[2], bird_coords[3]
        
        # Ground (Floor) AND Ceiling Boundaries Checked Directly
        if b_y2 >= HEIGHT or b_y1 <= 0:
            self.game_over()
            return
            
        # Geometric Overlapping Pipe Boundary Checking
        overlapping_objects = self.window.find_overlapping(b_x1, b_y1, b_x2, b_y2)      
        for obj_id in overlapping_objects:
            if "pipe" in self.window.gettags(obj_id):
                self.game_over()
                return

    def check_score(self):
        bird_coords = self.window.coords("bird")
        if not bird_coords: return
        bird_right = bird_coords[2]
        
        for pipe in self.window.find_withtag("pipe"):
            tags = self.window.gettags(pipe)
            pipe_id = [t for t in tags if t.startswith("pipe_")]
            
            if pipe_id:
                p_id = pipe_id[0]
                pipe_coords = self.window.coords(pipe)
                
                # Check if bird horizontal coordinate completely crossed past the pipe's trailing edge
                if pipe_coords and pipe_coords[2] < bird_right and p_id not in self.passed_pipes:
                    self.passed_pipes.add(p_id)
                    self.score += 1
                    
                    # Difficulty scaling increment every 3 points
                    if self.score % 3 == 0:
                        self.pipe_speed += 1.5
                        
                    self.text()

    def text(self):
        self.window.delete("scoreboard")
        self.window.create_text(100, 50, text=f"Score: {self.score}", font=("Helvetica", 24, "bold"), fill="white", tag="scoreboard")
        self.window.create_text(WIDTH - 150, 50, text=f"High Score: {self.high_score}", font=("Helvetica", 24, "bold"), fill="white", tag="scoreboard")

    def toggle_pause(self, event):
        if not self.game_started: return
        if self.game_running:
            self.game_running = False
            self.window.create_text(WIDTH/2, HEIGHT/2, text="PAUSED", font=("Helvetica", 48, "bold"), fill="yellow", tag="pause_text")
        else:
            self.game_running = True
            self.window.delete("pause_text")
            self.game_loop()

    def game_over(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            
        self.window.create_text(WIDTH/2, HEIGHT/2 - 30, text="GAME OVER", font=("Helvetica", 72, "bold"), fill="red")
        self.window.create_text(WIDTH/2, HEIGHT/2 + 50, text="Press R to Return to Menu", font=("Helvetica", 24), fill="white")

    def restart_game(self, event):
        if not self.game_running:
            self.game_started = False
            self.show_start_screen()

# ==========================================
# --- INITIALIZATION ENGINE RUN ------------
# ==========================================
root = tk.Tk()
game = FlappyBirdGame(root)
root.mainloop()