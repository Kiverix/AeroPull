import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from urllib.parse import urlparse, urljoin
import pygame
import random
from PIL import Image, ImageTk
from datetime import datetime
import time
from bs4 import BeautifulSoup

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("Welcome to AeroPull")
        self.splash.configure(bg='#1e1e1e')
        self.splash.overrideredirect(True)
        
        try:
            icon_path = os.path.join("resources", "sourceclown.ico")
            if os.path.exists(icon_path):
                self.splash.iconbitmap(icon_path)
        except Exception:
            pass
        
        try:
            self.splash.attributes('-topmost', True)
        except Exception:
            pass
        
        self.play_random_sound()
        
        self.setup_images()
        
        self.setup_labels()
        
        self.center_window(500, 375)
        
        self.loading_var = tk.StringVar(value="Loading")
        self.loading_label = tk.Label(
            self.splash, 
            textvariable=self.loading_var, 
            font=("Arial", 12), 
            bg='#1e1e1e', 
            fg='#ffffff'
        )
        self.loading_label.pack(pady=10)
        
        self.animate_loading()
        
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
            
            gaq9_path = os.path.join("resources", "gaq9.png")
            if os.path.exists(gaq9_path):
                try:
                    gaq9_img = Image.open(gaq9_path)
                    self.gaq9_img = ImageTk.PhotoImage(gaq9_img)
                    gaq9_label = tk.Label(img_frame, image=self.gaq9_img, bg='#1e1e1e')
                    gaq9_label.pack(side=tk.LEFT, padx=(0, 10))
                    
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
            text="AeroPull Version 0.20 - Made by Kiverix (the clown)", 
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
        self.root.title("AeroPull v0.20")
        
        pygame.mixer.init()
        
        self.center_window(650, 350)
        
        self.set_dark_theme()
        
        self.setup_ui()
        
        self.play_sound("open.wav")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.total_files = 0
        self.downloaded_files = 0
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.start_time = None
        
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
        
        ttk.Label(self.main_frame, text="Enter FastDL Base URL:").pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(self.main_frame, width=80)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        self.url_entry.insert(0, "")
        
        options_frame = ttk.Frame(self.main_frame)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(options_frame, text="Max Depth:").pack(side=tk.LEFT, padx=(0, 5))
        self.depth_var = tk.StringVar(value="0")
        self.depth_entry = ttk.Entry(options_frame, textvariable=self.depth_var, width=5)
        self.depth_entry.pack(side=tk.LEFT)
        
        ttk.Label(options_frame, text="File Types:").pack(side=tk.LEFT, padx=(10, 5))
        self.filetypes_var = tk.StringVar(value=".bsp,.bz2")
        self.filetypes_entry = ttk.Entry(options_frame, textvariable=self.filetypes_var, width=40)
        self.filetypes_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.stats_label = ttk.Label(self.main_frame, text="Files: 0/0 | Bytes: 0/0")
        self.stats_label.pack(fill=tk.X, pady=(0, 5))
        
        self.timer_label = ttk.Label(self.main_frame, text="Elapsed time: 00:00:00")
        self.timer_label.pack(fill=tk.X, pady=(0, 5))
        
        self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        self.status = ttk.Label(self.main_frame, text="Ready to download")
        self.status.pack(fill=tk.X)
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        self.download_btn = ttk.Button(btn_frame, text="Download Entire Library", command=self.start_download)
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
        
        try:
            max_depth = int(self.depth_var.get())
        except ValueError:
            messagebox.showerror("Invalid Depth", "Please enter a valid number for max depth")
            return
        
        file_types = [ext.strip().lower() for ext in self.filetypes_var.get().split(",")]
        
        now = datetime.now()
        folder_name = f"SCRAPE_{now.strftime('%d-%m_%H-%M')}"
        self.scrape_folder = os.path.join(os.getcwd(), folder_name)
        
        try:
            os.makedirs(self.scrape_folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create scrape folder: {str(e)}")
            return
        
        self.play_sound("join.wav")
            
        self.base_url = url if url.endswith('/') else url + '/'
        self.status.config(text=f"Downloading from: {self.base_url}")
        
        self.downloading = True
        self.cancel_requested = False
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        
        self.total_files = 0
        self.downloaded_files = 0
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.start_time = time.time()
        
        download_thread = Thread(target=self.scrape_and_download, args=(self.base_url, max_depth, file_types))
        download_thread.start()
        
        self.root.after(100, self.check_progress)
    
    def scrape_and_download(self, url, max_depth, file_types, current_depth=0):
        if self.cancel_requested or current_depth > max_depth:
            return
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            
            for link in links:
                if self.cancel_requested:
                    return
                    
                href = link.get('href')
                if href == '../' or href == './':
                    continue
                    
                full_url = urljoin(url, href)
                
                if href.endswith('/'):
                    self.scrape_and_download(full_url, max_depth, file_types, current_depth + 1)
                else:
                    ext = os.path.splitext(href)[1].lower()
                    if any(ext == file_ext for file_ext in file_types):
                        self.total_files += 1
                        self.update_stats()
                        
                        try:
                            head = requests.head(full_url)
                            self.total_bytes += int(head.headers.get('content-length', 0))
                            self.update_stats()
                        except:
                            pass
                            
                        self.download_file(full_url, url)
            
        except Exception as e:
            self.update_status(f"Error scraping {url}: {str(e)}")
    
    def download_file(self, file_url, base_url):
        try:
            relative_path = file_url[len(base_url):]
            save_path = os.path.join(self.scrape_folder, relative_path)
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            self.update_status(f"Downloading {relative_path}...")
            
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                file_size = int(r.headers.get('content-length', 0))
                
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
                            self.downloaded_bytes += len(chunk)
                            progress = int((self.downloaded_bytes / self.total_bytes) * 100) if self.total_bytes > 0 else 0
                            self.update_progress(progress)
                            self.update_stats()
                
            if not self.cancel_requested:
                self.downloaded_files += 1
                self.update_stats()
                
        except Exception as e:
            self.update_status(f"Error downloading {file_url}: {str(e)}")
    
    def update_stats(self):
        self.root.after(0, lambda: self.stats_label.config(
            text=f"Files: {self.downloaded_files}/{self.total_files} | Bytes: {self.format_bytes(self.downloaded_bytes)}/{self.format_bytes(self.total_bytes)}"
        ))
        
        if self.start_time and self.downloading:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.root.after(0, lambda: self.timer_label.config(
                text=f"Elapsed time: {hours:02d}:{minutes:02d}:{seconds:02d}"
            ))
    
    def format_bytes(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"
    
    def cancel_download(self):
        self.cancel_requested = True
        self.play_sound("information.wav")
        self.status.config(text="Cancelling download...")
    
    def update_status(self, text):
        self.root.after(0, lambda: self.status.config(text=text))
    
    def update_progress(self, value):
        self.root.after(0, lambda: self.progress.config(value=value))
    
    def check_progress(self):
        if self.downloading and not self.cancel_requested:
            self.update_stats()
            self.root.after(100, self.check_progress)
        else:
            if not self.cancel_requested and self.downloaded_files > 0:
                self.update_status(f"Download complete! {self.downloaded_files} files saved to {self.scrape_folder}")
                self.play_sound("information.wav")
            elif self.cancel_requested:
                self.update_status(f"Download cancelled! {self.downloaded_files} files saved to {self.scrape_folder}")
            self.reset_ui()
    
    def reset_ui(self):
        self.downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        
        if self.start_time:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            if self.cancel_requested:
                self.timer_label.config(
                    text=f"Cancelled after: {hours:02d}:{minutes:02d}:{seconds:02d}"
                )
            else:
                self.timer_label.config(
                    text=f"Final time: {hours:02d}:{minutes:02d}:{seconds:02d}"
                )
    
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
    splash = SplashScreen()
    splash.show()
    
    root = tk.Tk()
    app = FastDLDownloader(root)
    root.mainloop()