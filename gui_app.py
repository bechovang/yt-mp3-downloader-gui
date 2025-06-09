import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkFont
from downloader import download_audio # Assuming downloader.py exists and is correct
import threading
import os
import time
from datetime import datetime
import queue # Note: self.download_queue (the queue.Queue object) is initialized but not used.
import json

class YouTubeDownloaderApp:
    def __init__(self):
        self.app = tk.Tk()
        self.setup_window()
        self.setup_fonts()
        self.setup_variables()
        self.setup_ui()
        # self.setup_download_queue() # This method was empty, can be removed or kept.
                                     # It actually initialized self.queue_urls = []
                                     # which is also done in setup_variables if we make a slight change.
                                     # For now, I'll keep it as it defines self.queue_urls.
        self.setup_download_queue()
        self.load_download_history()
        
    def setup_window(self):
        self.app.title("🎵 YouTube Audio Downloader Pro")
        self.app.geometry("800x600") # Adjusted geometry slightly as one tab is removed
        self.app.configure(bg="#f0f2f5")
        self.app.resizable(True, True)
        
        try:
            self.app.iconbitmap("icon.ico")
        except:
            pass # Icon is optional
    
    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.header_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")
        self.default_font = tkFont.Font(family="Segoe UI", size=10)
        self.small_font = tkFont.Font(family="Segoe UI", size=9)
    
    def setup_variables(self):
        self.output_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloaded_audios"))
        self.download_queue_obj = queue.Queue() # This specific queue.Queue object is not used.
                                                # self.queue_urls (list) is used for the queue logic.
        self.is_downloading = False
        self.download_history = []
        self.history_file = "download_history.json"
        self.queue_urls = [] # Moved initialization here, setup_download_queue can be removed if preferred
    
    def setup_ui(self):
        main_container = tk.Frame(self.app, bg="#f0f2f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_container, text="🎵 YouTube Audio Downloader Pro", 
                              font=self.title_font, bg="#f0f2f5", fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Download Tab
        self.download_frame = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=20)
        self.notebook.add(self.download_frame, text="📥 Tải xuống")
        
        # Queue Tab
        self.queue_frame = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=20)
        self.notebook.add(self.queue_frame, text="⏳ Hàng chờ")
        
        self.setup_download_tab()
        # self.setup_files_tab() # REMOVED
        self.setup_queue_tab()
    
    def setup_download_tab(self):
        url_section = tk.LabelFrame(self.download_frame, text="🔗 Nhập URL", 
                                   font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        url_section.pack(fill=tk.X, pady=(0, 15))
        
        self.url_entry = tk.Text(url_section, height=4, font=self.default_font, 
                                wrap=tk.WORD, relief=tk.FLAT, bd=1)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        self.url_entry.configure(highlightbackground="#ddd", highlightthickness=1)
        
        placeholder_text = "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)..."
        self.url_entry.insert("1.0", placeholder_text)
        self.url_entry.config(fg="gray")
        
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)
        
        buttons_frame = tk.Frame(url_section, bg="#ffffff")
        buttons_frame.pack(fill=tk.X)
        
        add_queue_btn = tk.Button(buttons_frame, text="➕ Thêm vào hàng chờ", 
                                 command=self.add_to_queue, font=self.default_font,
                                 bg="#3498db", fg="white", relief=tk.FLAT, padx=20, pady=8,
                                 cursor="hand2")
        add_queue_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        download_now_btn = tk.Button(buttons_frame, text="⚡ Tải ngay", 
                                    command=self.download_now, font=self.default_font,
                                    bg="#e74c3c", fg="white", relief=tk.FLAT, padx=20, pady=8,
                                    cursor="hand2")
        download_now_btn.pack(side=tk.LEFT)
        
        path_section = tk.LabelFrame(self.download_frame, text="📂 Thư mục lưu", 
                                    font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        path_section.pack(fill=tk.X, pady=(0, 15))
        
        path_frame = tk.Frame(path_section, bg="#ffffff")
        path_frame.pack(fill=tk.X)
        
        browse_btn = tk.Button(path_frame, text="📁 Chọn thư mục", command=self.browse_folder,
                              font=self.default_font, bg="#95a5a6", fg="white", relief=tk.FLAT,
                              padx=15, pady=8, cursor="hand2")
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.path_display = tk.Label(path_frame, text=f"📍 {self.output_path_var.get()}", 
                                    font=self.default_font, bg="#ffffff", fg="#7f8c8d",
                                    wraplength=500, justify=tk.LEFT)
        self.path_display.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        status_section = tk.LabelFrame(self.download_frame, text="📊 Trạng thái", 
                                      font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        status_section.pack(fill=tk.BOTH, expand=True)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_section, variable=self.progress_var, 
                                           mode='determinate', length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(status_section, text="🔄 Sẵn sàng tải xuống", 
                                    font=self.default_font, bg="#ffffff", fg="#27ae60",
                                    wraplength=600, justify=tk.CENTER)
        self.status_label.pack(pady=5)
        
        self.stats_label = tk.Label(status_section, text="📈 Đã tải: 0 file", 
                                   font=self.small_font, bg="#ffffff", fg="#7f8c8d")
        self.stats_label.pack(pady=5)
    
    # def setup_files_tab(self): # REMOVED ENTIRE METHOD

    def setup_queue_tab(self):
        title = tk.Label(self.queue_frame, text="⏳ Hàng chờ tải xuống", 
                        font=self.header_font, bg="#ffffff", fg="#2c3e50")
        title.pack(pady=(0, 15))
        
        controls_frame = tk.Frame(self.queue_frame, bg="#ffffff")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_queue_btn = tk.Button(controls_frame, text="▶️ Bắt đầu tải", 
                                        command=self.start_queue_download,
                                        font=self.default_font, bg="#27ae60", fg="white", 
                                        relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.start_queue_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_queue_btn = tk.Button(controls_frame, text="🗑️ Xóa hàng chờ", 
                                   command=self.clear_queue,
                                   font=self.default_font, bg="#e74c3c", fg="white", 
                                   relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        clear_queue_btn.pack(side=tk.LEFT)
        
        queue_list_frame = tk.Frame(self.queue_frame, bg="#ffffff")
        queue_list_frame.pack(fill=tk.BOTH, expand=True)
        
        queue_scrollbar = tk.Scrollbar(queue_list_frame)
        queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_listbox = tk.Listbox(queue_list_frame, font=self.default_font,
                                       yscrollcommand=queue_scrollbar.set, relief=tk.FLAT,
                                       bg="#f8f9fa", selectbackground="#e74c3c", 
                                       selectforeground="white")
        self.queue_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        queue_scrollbar.config(command=self.queue_listbox.yview)
        
        self.queue_info = tk.Label(self.queue_frame, text="📊 Hàng chờ trống", 
                                  font=self.small_font, bg="#ffffff", fg="#7f8c8d")
        self.queue_info.pack(pady=10)
    
    def setup_download_queue(self):
        # self.queue_urls is already initialized in setup_variables
        # This method could be removed if self.queue_urls is initialized in setup_variables.
        # If kept, it confirms self.queue_urls exists.
        if not hasattr(self, 'queue_urls'):
            self.queue_urls = []
    
    def on_url_focus_in(self, event):
        if self.url_entry.get("1.0", tk.END).strip() == "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...":
            self.url_entry.delete("1.0", tk.END)
            self.url_entry.config(fg="black")
    
    def on_url_focus_out(self, event):
        if not self.url_entry.get("1.0", tk.END).strip():
            self.url_entry.insert("1.0", "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...")
            self.url_entry.config(fg="gray")
    
    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path_var.set(path)
            self.path_display.config(text=f"📍 {path}")
    
    def add_to_queue(self):
        urls_text = self.url_entry.get("1.0", tk.END).strip()
        if not urls_text or urls_text == "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một URL!")
            return
        
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        added_count = 0
        
        for url in urls:
            if url and url not in self.queue_urls:
                self.queue_urls.append(url)
                self.queue_listbox.insert(tk.END, f"⏳ {url}")
                added_count += 1
        
        if added_count > 0:
            self.update_queue_info()
            self.url_entry.delete("1.0", tk.END)
            self.url_entry.insert("1.0", "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...")
            self.url_entry.config(fg="gray")
            messagebox.showinfo("Thành công", f"Đã thêm {added_count} URL vào hàng chờ!")
        else:
            messagebox.showinfo("Thông báo", "Không có URL mới được thêm (có thể đã tồn tại).")
    
    def download_now(self):
        urls_text = self.url_entry.get("1.0", tk.END).strip()
        if not urls_text or urls_text == "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một URL!")
            return
        
        if self.is_downloading:
            messagebox.showwarning("Đang tải", "Đang có quá trình tải khác đang chạy!")
            return
        
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        self.start_download_process(urls)
    
    def start_queue_download(self):
        if not self.queue_urls:
            messagebox.showinfo("Thông báo", "Hàng chờ trống!")
            return
        
        if self.is_downloading:
            messagebox.showwarning("Đang tải", "Đang có quá trình tải khác đang chạy!")
            return
        
        urls_to_download = self.queue_urls.copy()
        self.start_download_process(urls_to_download, from_queue=True)
    
    def start_download_process(self, urls, from_queue=False):
        self.is_downloading = True
        self.start_queue_btn.config(state=tk.DISABLED, text="⏸️ Đang tải...")
        
        if from_queue:
            self.queue_urls.clear()
            self.queue_listbox.delete(0, tk.END)
            self.update_queue_info()
        
        download_thread = threading.Thread(
            target=self.download_multiple_urls,
            args=(urls,)
        )
        download_thread.daemon = True
        download_thread.start()
    
    def download_multiple_urls(self, urls):
        total_urls = len(urls)
        success_count = 0
        
        if not os.path.exists(self.output_path_var.get()):
            try:
                os.makedirs(self.output_path_var.get())
            except OSError as e:
                self.app.after(0, lambda: self.update_download_status(f"❌ Lỗi tạo thư mục: {e}"))
                self.app.after(0, self.download_completed)
                return


        for i, url in enumerate(urls):
            self.app.after(0, lambda u=url, idx=i: self.update_download_status(f"🔄 Đang tải ({idx+1}/{total_urls}): {u[:50]}..."))
            self.app.after(0, lambda: self.progress_var.set((i / total_urls) * 100))
            
            # Ensure downloader.py and its dependencies (like yt_dlp) are correctly installed and accessible
            try:
                success, message_or_filename = download_audio(url, self.output_path_var.get())
                if success:
                    success_count += 1
                    self.app.after(0, lambda u=url, fn=message_or_filename: self.add_to_history(u, fn))
                else: # message_or_filename is an error message
                    self.app.after(0, lambda msg=message_or_filename: self.update_download_status(f"⚠️ Lỗi: {msg}"))

            except Exception as e:
                self.app.after(0, lambda err=str(e): self.update_download_status(f"❌ Lỗi nghiêm trọng khi tải {url}: {err}"))
                success = False # Ensure success is false
            
            time.sleep(0.5)
        
        self.app.after(0, lambda: self.progress_var.set(100))
        self.app.after(0, lambda: self.update_download_status(f"✅ Hoàn thành! Đã tải thành công {success_count}/{total_urls} file"))
        self.app.after(0, self.download_completed) # This already calls self.refresh_files
        
        if success_count > 0:
            time.sleep(1)
            self.app.after(0, self.open_download_folder)
    
    def download_completed(self):
        self.is_downloading = False
        self.start_queue_btn.config(state=tk.NORMAL, text="▶️ Bắt đầu tải")
        self.progress_var.set(0)
        self.refresh_files() # Update stats label
    
    def update_download_status(self, message):
        self.status_label.config(text=message)
    
    def clear_queue(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ hàng chờ?"):
            self.queue_urls.clear()
            self.queue_listbox.delete(0, tk.END)
            self.update_queue_info()
    
    def update_queue_info(self):
        count = len(self.queue_urls)
        if count == 0:
            self.queue_info.config(text="📊 Hàng chờ trống")
        else:
            self.queue_info.config(text=f"📊 {count} URL trong hàng chờ")
    
    def refresh_files(self):
        """
        Counts audio files in the download directory and updates the stats_label.
        """
        download_path = self.output_path_var.get()
        num_files = 0
        
        if os.path.exists(download_path):
            audio_extensions = ['.mp3', '.m4a', '.webm', '.wav', '.aac', '.ogg', '.wma', '.flac']
            try:
                downloaded_file_names = [
                    f for f in os.listdir(download_path) 
                    if os.path.isfile(os.path.join(download_path, f)) and \
                       any(f.lower().endswith(ext) for ext in audio_extensions)
                ]
                num_files = len(downloaded_file_names)
            except Exception as e:
                print(f"Error refreshing file count: {e}") # Log error, but don't crash UI
                num_files = 0 # Or show an error state in stats_label
        
        self.stats_label.config(text=f"📈 Đã tải: {num_files} file")

    def open_download_folder(self):
        path = self.output_path_var.get()
        if not os.path.exists(path):
            try:
                os.makedirs(path) # Create if doesn't exist, though download_multiple_urls also tries
            except Exception as e:
                 messagebox.showerror("Lỗi", f"Không thể tạo thư mục: {e}")
                 return

        try:
            if os.name == 'nt': # Windows
                os.startfile(path)
            elif os.name == 'posix': # macOS, Linux
                if os.uname().sysname == 'Darwin': # macOS
                    os.system(f'open "{path}"')
                else: # Linux
                    os.system(f'xdg-open "{path}"')
            else:
                messagebox.showinfo("Thông báo", f"Không thể tự động mở thư mục trên hệ điều hành của bạn. Đường dẫn: {path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")
    
    # REMOVED METHODS: open_selected_file, show_file_context_menu, play_selected_file,
    # open_file_location, copy_file_path, delete_selected_file
    
    def add_to_history(self, url, filename):
        self.download_history.append({
            'url': url,
            'filename': filename, # This should be the actual filename string
            'timestamp': datetime.now().isoformat()
        })
        self.save_download_history()
    
    def load_download_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.download_history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            self.download_history = [] # Reset to empty list on error
    
    def save_download_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.download_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}") # Log error, don't show messagebox during background save
    
    def run(self):
        self.refresh_files() # Initial count of files for stats_label
        self.app.mainloop()

# Placeholder for downloader.py content if needed for testing
# Ensure you have a downloader.py file with a function like:
# def download_audio(url, output_path):
#     # Dummy implementation for testing UI without actual download
#     print(f"Attempting to download: {url} to {output_path}")
#     if "fail" in url:
#         return False, f"Failed to download {url}"
#     filename = f"audio_{time.time()}.mp3"
#     # Simulate file creation
#     # with open(os.path.join(output_path, filename), "w") as f:
#     #     f.write("dummy audio data")
#     return True, filename # Return (success_status, filename_or_error_message)

if __name__ == "__main__":
    # Example downloader.py (dummy for testing without yt_dlp)
    # Create a file named downloader.py in the same directory with this content:
    """
    import time
    import os

    def download_audio(url, output_path):
        print(f"DUMMY DOWNLOAD: {url} to {output_path}")
        os.makedirs(output_path, exist_ok=True) # Ensure output path exists
        
        # Simulate success/failure
        if "fail" in url.lower():
            time.sleep(1)
            return False, f"Simulated download failure for {url}"
        
        # Simulate a successful download
        # Sanitize URL to create a somewhat valid filename part
        safe_url_part = "".join(c if c.isalnum() else "_" for c in url[-20:])
        filename = f"dummy_audio_{safe_url_part}_{int(time.time())}.mp3"
        file_path = os.path.join(output_path, filename)
        
        try:
            with open(file_path, "w") as f:
                f.write("This is dummy audio content.")
            print(f"DUMMY: Created file {file_path}")
            time.sleep(1) # Simulate download time
            return True, filename # On success, return True and the filename
        except Exception as e:
            return False, f"Error creating dummy file: {str(e)}"
    """
    app_instance = YouTubeDownloaderApp()
    app_instance.run()