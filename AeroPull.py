import os
import random
import time
import webbrowser
from datetime import datetime
from threading import Thread, Event
from urllib.parse import urlparse, urljoin
import pygame
import requests
import tkinter as tk
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog


class SplashScreen:
    """Splash screen displayed on application startup."""
    
    def __init__(self):
        self.splash = tk.Tk()
        self._setup_window()
        self._load_icon()
        self.play_random_sound()
        self._setup_images()
        self._setup_labels()
        self._setup_loading_animation()
        self.splash.after(3000, self.close)
    
    def _setup_window(self):
        """Configure splash window appearance."""
        self.splash.title("Welcome to AeroPull")
        self.splash.configure(bg='#1e1e1e')
        self.splash.overrideredirect(True)
        self._center_window(500, 375)
        
        try:
            self.splash.attributes('-topmost', True)
        except Exception:
            pass
    
    def _load_icon(self):
        """Load application icon if available."""
        try:
            icon_path = os.path.join("resources", "sourceclown.ico")
            if os.path.exists(icon_path):
                self.splash.iconbitmap(icon_path)
        except Exception:
            pass
    
    def _setup_images(self):
        """Load and display splash screen images."""
        try:
            img_frame = tk.Frame(self.splash, bg='#1e1e1e')
            img_frame.pack(side=tk.TOP, pady=(10, 0))
            
            gaq9_path = os.path.join("resources", "gaq9.png")
            if os.path.exists(gaq9_path):
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
    
    def _setup_labels(self):
        """Create informational labels."""
        tk.Label(
            self.splash, 
            text="Thank you for using AeroPull!", 
            font=("Arial", 16, "bold"), 
            bg='#1e1e1e', 
            fg='#4fc3f7'
        ).pack(pady=(5, 0))
        
        tk.Label(
            self.splash, 
            text="AeroPull Version 1.0 - Made by Kiverix (the clown)", 
            font=("Arial", 10), 
            bg='#1e1e1e', 
            fg='#ffffff'
        ).pack(pady=(5, 0))
    
    def _setup_loading_animation(self):
        """Initialize loading animation."""
        self.loading_var = tk.StringVar(value="Loading")
        self.loading_label = tk.Label(
            self.splash, 
            textvariable=self.loading_var, 
            font=("Arial", 12), 
            bg='#1e1e1e', 
            fg='#ffffff'
        )
        self.loading_label.pack(pady=10)
        self._animate_loading()
    
    def _center_window(self, width, height):
        """Center the window on screen."""
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.splash.geometry(f'{width}x{height}+{x}+{y}')
    
    def _animate_loading(self, count=0):
        """Animate loading dots."""
        if not hasattr(self, 'splash') or not self.splash.winfo_exists():
            return
            
        dots = '.' * ((count % 4) + 1)
        self.loading_var.set(f"Loading{dots}")
        if hasattr(self, 'splash') and self.splash.winfo_exists():
            self.splash.after(200, self._animate_loading, count + 1)
    
    def play_random_sound(self):
        """Play random startup sound."""
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
    
    def close(self):
        """Close splash screen."""
        if hasattr(self, 'splash') and self.splash.winfo_exists():
            self.splash.destroy()
    
    def show(self):
        """Display splash screen."""
        self.splash.mainloop()


class FastDLDownloader:
    """Main application for FastDL downloading with enhanced features."""
    
    def __init__(self, root):
        self.root = root
        self._initialize_properties()
        self._setup_window()
        self._create_custom_title_bar()
        self._setup_ui()
        self._setup_event_handlers()
        self.play_sound("open.wav")
    
    def _initialize_properties(self):
        """Initialize class properties."""
        self.root.title("AeroPull v1.0")  # Updated version
        pygame.mixer.init()
        
        # Download tracking
        self.total_files = 0
        self.downloaded_files = 0
        self.failed_files = 0
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.start_time = None
        self.last_update_time = None
        self.last_bytes = 0
        self.update_interval = 1.0  # Update stats every second
        
        # State flags
        self.running = True
        self.downloading = False
        self.cancel_requested = False
        self.paused = False
        self.pause_event = Event()
        self.counting_files = False
        
        # Sound
        self.waiting_sound = None
        
        # History log
        self.history_file = "download_history.log"
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                f.write("AeroPull Download History\n")
                f.write("="*40 + "\n")
        
        # Failed downloads tracking
        self.failed_downloads = []
        self.max_retries = 3
        self.retry_delay = 5  # seconds between retries
    
    def _setup_window(self):
        """Configure main window appearance."""
        self._center_window(650, 400)  # Slightly taller for new features
        self._set_dark_theme()
    
    def _setup_event_handlers(self):
        """Set up window event handlers."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def _create_custom_title_bar(self):
        """Create custom title bar with controls."""
        self.title_bar = tk.Frame(self.root, bg="#232323", relief=tk.RAISED, bd=0, height=32)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)
        self.title_bar.bind('<Button-1>', self._start_move)
        self.title_bar.bind('<B1-Motion>', self._on_move)
        
        # Title label
        tk.Label(
            self.title_bar,
            text="AeroPull v1.0 - With Love, by Kiverix",
            bg="#232323",
            fg="#4fc3f7",
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = tk.Button(
            self.title_bar,
            text="✕",
            bg="#232323",
            fg="#ff5555",
            font=("Arial", 12, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#3d3d3d",
            activeforeground="#ff5555",
            command=self.on_close,
            cursor="hand2"
        )
        close_btn.pack(side=tk.RIGHT, padx=(0, 10))
        close_btn.bind('<Enter>', self.play_hover_sound)
        
        # Minimize button
        minimize_btn = tk.Button(
            self.title_bar,
            text="━",
            bg="#232323",
            fg="#4fc3f7",
            font=("Arial", 12, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#3d3d3d",
            activeforeground="#4fc3f7",
            command=self.minimize_window,
            cursor="hand2"
        )
        minimize_btn.pack(side=tk.RIGHT, padx=(0, 0))
        minimize_btn.bind('<Enter>', self.play_hover_sound)
    
    def _setup_ui(self):
        """Set up main user interface with new features."""
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL input
        ttk.Label(self.main_frame, text="Enter FastDL Base URL:").pack(anchor=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(self.main_frame, width=80)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        self.url_entry.insert(0, "")
        
        # Options frame
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
        
        # Enhanced stats display
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.stats_label = ttk.Label(stats_frame, text="Files: 0/0 | Bytes: 0/0")
        self.stats_label.pack(side=tk.LEFT)
        
        self.speed_label = ttk.Label(stats_frame, text=" | Speed: 0 KB/s")
        self.speed_label.pack(side=tk.LEFT, padx=10)
        
        self.eta_label = ttk.Label(stats_frame, text=" | ETA: --:--:--")
        self.eta_label.pack(side=tk.LEFT)
        
        self.failed_label = ttk.Label(stats_frame, text=" | Failed: 0")
        self.failed_label.pack(side=tk.LEFT, padx=10)
        
        self.timer_label = ttk.Label(self.main_frame, text="Elapsed time: 00:00:00")
        self.timer_label.pack(fill=tk.X, pady=(0, 5))
        
        self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        self.status = ttk.Label(self.main_frame, text="Ready to download")
        self.status.pack(fill=tk.X)
        
        # Buttons - Added Pause button
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        self.download_btn = ttk.Button(btn_frame, text="Download Entire Library", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(btn_frame, text="Pause", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bottom left corner links
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # GAQ9 Website Link
        self.gaq9_label = tk.Label(
            bottom_frame, 
            text="Go to gaq9.com", 
            fg="purple", 
            bg='#1e1e1e', 
            font=("Arial", 9), 
            cursor="hand2"
        )
        self.gaq9_label.pack(side=tk.LEFT, padx=(0, 10))
        
        def open_gaq9(event=None):
            webbrowser.open("https://gaq9.com")
            self.play_sound("information.wav")
        self.gaq9_label.bind("<Button-1>", open_gaq9)

        # YouTube Channel Link
        self.youtube_label = tk.Label(
            bottom_frame, 
            text="Subscribe to my Youtube", 
            fg="red", 
            bg='#1e1e1e', 
            font=("Arial", 9), 
            cursor="hand2"
        )
        self.youtube_label.pack(side=tk.LEFT)
        
        def open_youtube(event=None):
            webbrowser.open("https://www.youtube.com/@kiverix")
            self.play_sound("information.wav")
        self.youtube_label.bind("<Button-1>", open_youtube)
    
    def _set_dark_theme(self):
        """Configure dark theme for the application."""
        self.root.configure(bg='#1e1e1e')
        
        # Color definitions
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.entry_bg = '#252525'
        self.entry_fg = '#ffffff'
        self.button_bg = '#3c3c3c'
        self.button_fg = '#ffffff'
        self.button_active = '#4a4a4a'
        self.progress_color = '#007acc'
        
        # Style configuration
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
    
    def _center_window(self, width, height):
        """Center the window on screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _start_move(self, event):
        """Start window drag operation."""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _on_move(self, event):
        """Handle window movement during drag."""
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")
    
    def minimize_window(self):
        """Minimize the window."""
        self.root.update_idletasks()
        self.root.iconify()
    
    def validate_url(self, url):
        """Validate the given URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def start_download(self):
        """Start the download process with enhanced tracking."""
        url = self.url_entry.get().strip()
        
        if not self.validate_url(url):
            self.play_sound("error.wav")  # Play error sound when URL is invalid
            return
        
        try:
            max_depth = int(self.depth_var.get())
        except ValueError:
            messagebox.showerror("Invalid Depth", "Please enter a valid number for max depth")
            return
        
        file_types = [ext.strip().lower() for ext in self.filetypes_var.get().split(",")]
        
        # Create download directory
        now = datetime.now()
        folder_name = f"SCRAPE_{now.strftime('%d-%m_%H-%M')}"
        self.scrape_folder = os.path.join(os.getcwd(), folder_name)
        
        try:
            os.makedirs(self.scrape_folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create scrape folder: {str(e)}")
            return
        
        # Play waiting sound at 25% volume
        self.play_waiting_sound()
        
        # Initialize download
        self.base_url = url if url.endswith('/') else url + '/'
        self.status.config(text=f"Counting files from: {self.base_url}")
        
        self.downloading = True
        self.cancel_requested = False
        self.paused = False
        self.download_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.NORMAL)
        self.pause_event.set()  # Ensure downloads can start
        
        # Reset counters
        self.total_files = 0
        self.total_bytes = 0
        self.downloaded_files = 0
        self.downloaded_bytes = 0
        self.failed_files = 0
        self.failed_downloads = []
        self.start_time = time.time()
        self.last_update_time = time.time()
        self.last_bytes = 0
        
        # Update progress bar to 0
        self.update_progress(0)
        
        # Start counting thread first
        count_thread = Thread(
            target=self._perform_file_count_then_download, 
            args=(self.base_url, max_depth, file_types)
        )
        count_thread.start()
        
        # Start the stats update loop
        self.update_stats_loop()
    
    def update_stats_loop(self):
        """Continuously update stats every second while downloading."""
        if self.downloading and not self.cancel_requested:
            self.update_stats()
            self.root.after(int(self.update_interval * 1000), self.update_stats_loop)
    
    def _perform_file_count_then_download(self, base_url, max_depth, file_types):
        """Count files first, then start download."""
        try:
            # First count files
            self.counting_files = True
            self._perform_file_count(base_url, max_depth, file_types)
            # Stop waiting sound before download starts
            self.stop_waiting_sound()
            # Only proceed with download if not cancelled and files were found
            if not self.cancel_requested and self.total_files > 0:
                self.play_sound("join.wav")
                self.status.config(text=f"Downloading {self.total_files} files...")
                # Start the main download process
                self.scrape_and_download(base_url, max_depth, file_types, already_counted=True)
                # After initial download, retry failed downloads if any
                if self.failed_downloads and not self.cancel_requested:
                    self.retry_failed_downloads()
                # Final status update
                if not self.cancel_requested:
                    if self.failed_files > 0:
                        self.update_status(f"Completed with {self.failed_files} failed downloads")
                    else:
                        self.update_status("All files downloaded successfully!")
                        self.play_complete_sound()
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.counting_files = False
            self.stop_waiting_sound()
            self._reset_ui()
    
    def play_complete_sound(self):
        """Play completion sound."""
        try:
            sound_path = os.path.join("resources", "complete.wav")
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(0.5)
                sound.play()
        except Exception:
            pass
            
    def retry_failed_downloads(self):
        """Retry failed downloads until all are downloaded or max retries reached."""
        retry_count = 0
        while self.failed_downloads and retry_count < self.max_retries and not self.cancel_requested:
            retry_count += 1
            self.update_status(f"Retrying failed downloads (attempt {retry_count}/{self.max_retries})...")
            time.sleep(self.retry_delay)  # Small delay before retry
            
            # Make a copy of current failed downloads to process
            current_failed = self.failed_downloads.copy()
            self.failed_downloads = []  # Clear for new attempts
            
            for file_url, base_url in current_failed:
                if self.cancel_requested:
                    break
                    
                self.download_file(file_url, base_url)
            
            # Update failed count display
            self.failed_label.config(text=f" | Failed: {len(self.failed_downloads)}")
        
        # Update final status after retries
        if self.failed_downloads:
            self.update_status(f"Completed with {len(self.failed_downloads)} files still failed after {self.max_retries} retries")
            self.play_sound("warning.wav")
        else:
            self.update_status("All files successfully downloaded after retry!")
            self.play_sound("complete.wav")
    
    def _perform_file_count(self, url, max_depth, file_types):
        """Perform the actual file counting operation."""
        try:
            base_url = url if url.endswith('/') else url + '/'
            total_files = 0
            total_bytes = 0
            
            def count_files_recursive(current_url, current_depth):
                nonlocal total_files, total_bytes
                
                if current_depth > max_depth or self.cancel_requested:
                    return
                
                try:
                    response = requests.get(current_url)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = soup.find_all('a')
                    
                    for link in links:
                        if self.cancel_requested:
                            return
                            
                        href = link.get('href')
                        if href == '../' or href == './':
                            continue
                            
                        full_url = urljoin(current_url, href)
                        
                        if href.endswith('/'):
                            count_files_recursive(full_url, current_depth + 1)
                        else:
                            ext = os.path.splitext(href)[1].lower()
                            if any(ext == file_ext for file_ext in file_types):
                                total_files += 1
                                
                                # Get file size if possible
                                try:
                                    head = requests.head(full_url)
                                    total_bytes += int(head.headers.get('content-length', 0))
                                except:
                                    pass
                
                except Exception as e:
                    pass  # Silently handle errors during counting
            
            # Start counting
            count_files_recursive(base_url, 0)
            
            # Update the counts
            self.total_files = total_files
            self.total_bytes = total_bytes
            
            # Update the stats display
            self.update_stats()
            
        except Exception as e:
            self.update_status(f"Error counting files: {str(e)}")
    
    def scrape_and_download(self, url, max_depth, file_types, already_counted=False, current_depth=0):
        """Recursively scrape and download files from the given URL."""
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
                    self.scrape_and_download(full_url, max_depth, file_types, already_counted, current_depth + 1)
                else:
                    ext = os.path.splitext(href)[1].lower()
                    if any(ext == file_ext for file_ext in file_types):
                        if not already_counted:
                            self.total_files += 1
                            try:
                                head = requests.head(full_url)
                                self.total_bytes += int(head.headers.get('content-length', 0))
                            except:
                                pass
                            self.update_stats()
                            
                        self.download_file(full_url, url)
            
        except Exception as e:
            self.update_status(f"Error scraping {url}: {str(e)}")
    
    def download_file(self, file_url, base_url):
        """Download a single file with pause/resume support."""
        try:
            relative_path = file_url[len(base_url):]
            save_path = os.path.join(self.scrape_folder, relative_path)
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            self.update_status(f"Downloading {relative_path}...")
            
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                file_size = int(r.headers.get('content-length', 0))
                
                # Log download start
                self.log_download(file_url, "STARTED", file_size)
                
                with open(save_path, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        # Check for pause/cancel
                        if self.cancel_requested:
                            self.log_download(file_url, "CANCELLED", downloaded)
                            return
                            
                        self.pause_event.wait()  # Will block if paused
                        
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            self.downloaded_bytes += len(chunk)
                            progress = int((self.downloaded_bytes / self.total_bytes) * 100) if self.total_bytes > 0 else 0
                            self.update_progress(progress)
                
            if not self.cancel_requested:
                self.downloaded_files += 1
                self.log_download(file_url, "COMPLETED", file_size)
                self.update_stats()
                
        except Exception as e:
            self.failed_files += 1
            self.failed_downloads.append((file_url, base_url))
            self.failed_label.config(text=f" | Failed: {self.failed_files}")
            self.log_download(file_url, f"ERROR: {str(e)}", downloaded)
            self.update_status(f"Error downloading {file_url}: {str(e)}")
    
    def update_stats(self):
        """Update download statistics with speed and ETA."""
        current_time = time.time()
        
        # Files and bytes progress
        files_text = f"Files: {self.downloaded_files}/{self.total_files}"
        bytes_text = f" | Bytes: {self._format_bytes(self.downloaded_bytes)}/{self._format_bytes(self.total_bytes)}"
        self.stats_label.config(text=files_text + bytes_text)
        
        # Download speed calculation
        if self.last_update_time and current_time > self.last_update_time:
            time_diff = current_time - self.last_update_time
            bytes_diff = self.downloaded_bytes - self.last_bytes
            download_speed = bytes_diff / time_diff if time_diff > 0 else 0
            self.speed_label.config(text=f" | Speed: {self._format_bytes(download_speed)}/s")
            
            # ETA calculation
            if download_speed > 0:
                remaining_bytes = self.total_bytes - self.downloaded_bytes
                eta_seconds = remaining_bytes / download_speed
                self.eta_label.config(text=f" | ETA: {self._format_time(eta_seconds)}")
            
            # Update tracking variables
            self.last_update_time = current_time
            self.last_bytes = self.downloaded_bytes
        
        # Elapsed time
        if self.start_time:
            elapsed = current_time - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.timer_label.config(text=f"Elapsed time: {hours:02d}:{minutes:02d}:{seconds:02d}")

    def _format_bytes(self, bytes):
        """Format bytes into human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"
    
    def _format_time(self, seconds):
        """Format seconds into HH:MM:SS."""
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def log_download(self, url, status, filesize):
        """Log download activity to history file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        size_mb = filesize / (1024 * 1024)
        log_entry = f"[{timestamp}] {url} - {status} - {size_mb:.2f}MB\n"
        
        with open(self.history_file, "a") as f:
            f.write(log_entry)
        
        # Also update status if error
        if "ERROR" in status:
            self.update_status(f"Error logged: {url}")

    def update_status(self, text):
        """Update status label."""
        self.root.after(0, lambda: self.status.config(text=text))
    
    def update_progress(self, value):
        """Update progress bar."""
        self.root.after(0, lambda: self.progress.config(value=value))
    
    def _reset_ui(self):
        """Reset UI to initial state after download completes."""
        self.downloading = False
        self.paused = False
        self.download_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED, text="Pause")
        self.cancel_btn.config(state=tk.DISABLED)
        
        # Reset speed/ETA displays
        self.speed_label.config(text=" | Speed: 0 KB/s")
        self.eta_label.config(text=" | ETA: --:--:--")

    def toggle_pause(self):
        """Toggle pause/resume download state."""
        self.paused = not self.paused
        if self.paused:
            self.pause_event.clear()  # Blocks threads
            self.pause_btn.config(text="Resume")
            self.status.config(text="Download paused")
            self.play_sound("information.wav")
        else:
            self.pause_event.set()  # Allows threads to run
            self.pause_btn.config(text="Pause")
            self.status.config(text="Resuming download...")
            self.last_update_time = time.time()  # Reset speed calculation
            self.last_bytes = self.downloaded_bytes
    
    def cancel_download(self):
        """Cancel the current download operation."""
        self.cancel_requested = True
        self.pause_event.set()  # Unblock any paused threads
        self.play_sound("information.wav")
        self.status.config(text="Cancelling download...")
        self.log_download("SYSTEM", "DOWNLOAD CANCELLED", self.downloaded_bytes)
    
    def play_sound(self, filename):
        """Play the specified sound file."""
        try:
            sound_path = os.path.join("resources", filename)
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.play()
        except Exception:
            pass
    
    def play_waiting_sound(self):
        """Play the waiting sound at 25% volume."""
        try:
            sound_path = os.path.join("resources", "waiting.wav")
            if os.path.exists(sound_path):
                if self.waiting_sound:
                    self.waiting_sound.stop()
                self.waiting_sound = pygame.mixer.Sound(sound_path)
                self.waiting_sound.set_volume(0.15)
                self.waiting_sound.play(-1)  # Loop indefinitely
        except Exception:
            pass
    
    def stop_waiting_sound(self):
        """Stop the waiting sound."""
        try:
            if self.waiting_sound:
                self.waiting_sound.stop()
        except Exception:
            pass
    
    def play_hover_sound(self, event=None):
        """Play hover sound effect."""
        self.play_sound("hover.wav")
    
    def on_close(self):
        """Handle window close event."""
        self.stop_waiting_sound()  # Ensure sound stops when closing
        self.play_sound("close.wav")
        try:
            import pygame
            start = time.time()
            while pygame.mixer.get_busy() and time.time() - start < 1:
                self.root.update()
                time.sleep(0.05)
        except Exception:
            pass
        self.running = False
        self.root.destroy()


def main():
    """Main application entry point."""
    splash = SplashScreen()
    splash.show()
    
    root = tk.Tk()
    app = FastDLDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()