import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from urllib.parse import urlparse
import pygame
import random
from PIL import Image, ImageTk
from datetime import datetime

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("Welcome to AeroPull")
        self.splash.configure(bg='#1e1e1e')
        self.splash.overrideredirect(True)
        
        # Set icon
        try:
            icon_path = os.path.join("resources", "sourceclown.ico")
            if os.path.exists(icon_path):
                self.splash.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Make splash stay on top
        try:
            self.splash.attributes('-topmost', True)
        except Exception:
            pass
        
        # Play random sound
        self.play_random_sound()
        
        # Display images
        self.setup_images()
        
        # Add text labels
        self.setup_labels()
        
        # Center and show window
        self.center_window(500, 375)
        
        # Start loading animation
        self.loading_var = tk.StringVar(value="Loading")
        self.loading_label = tk.Label(
            self.splash, 
            textvariable=self.loading_var, 
            font=("Arial", 12), 
            bg='#1e1e1e', 
            fg='#ffffff'
        )
        self.loading_label.pack(pady=10)
        
        # Start animation
        self.animate_loading()
        
        # Close after delay
        self.splash.after(3000, self.close)
        
    def play_random_sound(self):
        try:
            pygame.mixer.init()
            preopen_files = [
                f"preopen{i}.mp3" for i in range(1, 3) 
                if os.path.exists(os.path.join("resources", f"preopen{i}.mp3"))
            ]
            if preopen_files:
                chosen = random.choice(preopen_files)
                sound_path = os.path.join("resources", chosen)
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(0.5)
                sound.play()
        except Exception:
            pass
    
    def setup_images(self):
        try:
            img_frame = tk.Frame(self.splash, bg='#1e1e1e')
            img_frame.pack(side=tk.TOP, pady=(10, 0))
            
            # Load and display gaq9.png
            gaq9_path = os.path.join("resources", "gaq9.png")
            if os.path.exists(gaq9_path):
                try:
                    gaq9_img = Image.open(gaq9_path)
                    self.gaq9_img = ImageTk.PhotoImage(gaq9_img)
                    gaq9_label = tk.Label(img_frame, image=self.gaq9_img, bg='#1e1e1e')
                    gaq9_label.pack(side=tk.LEFT, padx=(0, 10))
                    
                    # Load and display sourceclown.png (resized to match)
                    sourceclown_path = os.path.join("resources", "sourceclown.png")
                    if os.path.exists(sourceclown_path):
                        sourceclown_img = Image.open(sourceclown_path)
                        sourceclown_img = sourceclown_img.resize(gaq9_img.size, Image.LANCZOS)
                        self.sourceclown_img = ImageTk.PhotoImage(sourceclown_img)
                        sourceclown_label = tk.Label(img_frame, image=self.sourceclown_img, bg='#1e1e1e')
                        sourceclown_label.pack(side=tk.LEFT)
                except Exception:
                    pass
        except Exception:
            pass
    
    def setup_labels(self):
        label = tk.Label(
            self.splash, 
            text="Thank you for using AeroPull!", 
            font=("Arial", 16, "bold"), 
            bg='#1e1e1e', 
            fg='#4fc3f7'
        )
        label.pack(pady=(5, 0))
        
        version_label = tk.Label(
            self.splash, 
            text="AeroPull Version 0.19 - Made by Kiverix (the clown)", 
            font=("Arial", 10), 
            bg='#1e1e1e', 
            fg='#ffffff'
        )
        version_label.pack(pady=(5, 0))
    
    def center_window(self, width, height):
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.splash.geometry(f'{width}x{height}+{x}+{y}')
    
    def animate_loading(self, count=0):
        if not hasattr(self, 'splash') or not self.splash.winfo_exists():
            return
            
        dots = '.' * ((count % 4) + 1)
        self.loading_var.set(f"Loading{dots}")
        self.splash.after(200, self.animate_loading, count + 1)
    
    def close(self):
        if hasattr(self, 'splash') and self.splash.winfo_exists():
            self.splash.destroy()
    
    def show(self):
        self.splash.mainloop()

class FastDLDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("AeroPull v0.19")
        
        pygame.mixer.init()
        
        self.center_window(550, 250)
        
        self.set_dark_theme()
        
        self.setup_ui()
        
        self.play_sound("open.wav")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def set_dark_theme(self):
        self.root.configure(bg='#1e1e1e')
        
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.entry_bg = '#252525'
        self.entry_fg = '#ffffff'
        self.button_bg = '#3c3c3c'
        self.button_fg = '#ffffff'
        self.button_active = '#4a4a4a'
        self.progress_color = '#007acc'
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('.', background=self.bg_color, foreground=self.fg_color)
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('TEntry', fieldbackground=self.entry_bg, foreground=self.entry_fg, 
                       insertcolor=self.fg_color)
        style.configure('TButton', background=self.button_bg, foreground=self.button_fg, 
                        bordercolor=self.button_bg, lightcolor=self.button_bg, darkcolor=self.button_bg)
        style.map('TButton', 
                 background=[('active', self.button_active), ('disabled', self.button_bg)],
                 foreground=[('active', self.button_fg), ('disabled', self.fg_color)])
        style.configure('TProgressbar', background=self.progress_color, troughcolor=self.entry_bg)
        
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.main_frame, text="Enter Download URL:").pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(self.main_frame, width=60)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        self.url_entry.insert(0, "https://dl.game-relay.cloud/6953190d-c02b-4536-8dfd-7658840ef9eb/maps/gsh_inferno.bsp.bz2")
        
        self.url_display = ttk.Label(self.main_frame, text="", wraplength=400)
        self.url_display.pack(fill=tk.X, pady=(0, 10))
        
        self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        self.status = ttk.Label(self.main_frame, text="Ready to download")
        self.status.pack(fill=tk.X)
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        self.download_btn = ttk.Button(btn_frame, text="Download", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        self.downloading = False
        self.cancel_requested = False
    
    def validate_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def start_download(self):
        url = self.url_entry.get().strip()
        
        if not self.validate_url(url):
            messagebox.showerror("Invalid URL", "Please enter a valid URL starting with http:// or https://")
            return
        
        # Create timestamped folder for scraping
        now = datetime.now()
        folder_name = f"SCRAPE_{now.strftime('%d/%m_%H:%M')}"
        # Replace invalid characters for Windows folder names
        folder_name = folder_name.replace('/', '-').replace(':', '-')
        self.scrape_folder = os.path.join(os.getcwd(), folder_name)
        
        try:
            os.makedirs(self.scrape_folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create scrape folder: {str(e)}")
            return
        
        self.play_sound("join.wav")
            
        self.fastdl_url = url
        self.url_display.config(text=f"Downloading: {url}")
        
        self.downloading = True
        self.cancel_requested = False
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        
        download_thread = Thread(target=self.download_file)
        download_thread.start()
        
        self.root.after(100, self.check_progress)
    
    def cancel_download(self):
        self.cancel_requested = True
        self.status.config(text="Cancelling download...")
    
    def download_file(self):
        try:
            parsed_url = urlparse(self.fastdl_url)
            filename = os.path.basename(parsed_url.path)
            
            if not filename:
                filename = "downloaded_file"
                
            # Save file to the timestamped scrape folder
            save_path = os.path.join(self.scrape_folder, filename)
            
            self.update_status(f"Downloading {filename}...")
            
            with requests.get(self.fastdl_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                
                with open(save_path, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        if self.cancel_requested:
                            self.update_status("Download cancelled")
                            f.close()
                            if os.path.exists(save_path):
                                os.remove(save_path)
                            return
                            
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = int((downloaded / total_size) * 100) if total_size > 0 else 0
                            self.update_progress(progress)
                
            if not self.cancel_requested:
                self.update_status(f"Download complete! Saved to {save_path}")
                self.play_sound("information.wav")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to download file:\n{str(e)}")
        finally:
            self.downloading = False
            self.root.after(100, self.reset_ui)
    
    def update_status(self, text):
        self.root.after(0, lambda: self.status.config(text=text))
    
    def update_progress(self, value):
        self.root.after(0, lambda: self.progress.config(value=value))
    
    def check_progress(self):
        if self.downloading:
            self.root.after(100, self.check_progress)
    
    def reset_ui(self):
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress.config(value=0)
    
    def play_sound(self, filename):
        try:
            sound_path = os.path.join("resources", filename)
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.play()
        except Exception as e:
            pass
    
    def on_closing(self):
        self.play_sound("close.wav")
        self.root.after(200, self.root.destroy)

if __name__ == "__main__":
    # Show splash screen first
    splash = SplashScreen()
    splash.show()
    
    # Then start main application
    root = tk.Tk()
    app = FastDLDownloader(root)
    root.mainloop()