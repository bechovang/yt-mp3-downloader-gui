import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkFont
from downloader import download_audio
import threading
import os
import time
from datetime import datetime
import queue
import json

class YouTubeDownloaderApp:
    def __init__(self):
        self.app = tk.Tk()
        self.setup_window()
        self.setup_fonts()
        self.setup_variables()
        self.setup_ui()
        self.setup_download_queue()
        self.load_download_history()
        
    def setup_window(self):
        self.app.title("🎵 YouTube Audio Downloader Pro")
        self.app.geometry("800x700")
        self.app.configure(bg="#f0f2f5")
        self.app.resizable(True, True)
        
        # Icon và styling
        try:
            self.app.iconbitmap("icon.ico")  # Nếu có icon
        except:
            pass
    
    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.header_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")
        self.default_font = tkFont.Font(family="Segoe UI", size=10)
        self.small_font = tkFont.Font(family="Segoe UI", size=9)
    
    def setup_variables(self):
        self.output_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloaded_audios"))
        self.download_queue = queue.Queue()
        self.is_downloading = False
        self.download_history = []
        self.history_file = "download_history.json"
    
    def setup_ui(self):
        # Main container với padding
        main_container = tk.Frame(self.app, bg="#f0f2f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_container, text="🎵 YouTube Audio Downloader Pro", 
                              font=self.title_font, bg="#f0f2f5", fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Download Tab
        self.download_frame = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=20)
        self.notebook.add(self.download_frame, text="📥 Tải xuống")
        
        # Downloaded Files Tab
        self.files_frame = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=20)
        self.notebook.add(self.files_frame, text="📁 File đã tải")
        
        # Queue Tab
        self.queue_frame = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=20)
        self.notebook.add(self.queue_frame, text="⏳ Hàng chờ")
        
        self.setup_download_tab()
        self.setup_files_tab()
        self.setup_queue_tab()
    
    def setup_download_tab(self):
        # URL Input Section
        url_section = tk.LabelFrame(self.download_frame, text="🔗 Nhập URL", 
                                   font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        url_section.pack(fill=tk.X, pady=(0, 15))
        
        # URL Entry
        self.url_entry = tk.Text(url_section, height=4, font=self.default_font, 
                                wrap=tk.WORD, relief=tk.FLAT, bd=1)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        self.url_entry.configure(highlightbackground="#ddd", highlightthickness=1)
        
        # Placeholder text
        placeholder_text = "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)..."
        self.url_entry.insert("1.0", placeholder_text)
        self.url_entry.config(fg="gray")
        
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)
        
        # Buttons frame
        buttons_frame = tk.Frame(url_section, bg="#ffffff")
        buttons_frame.pack(fill=tk.X)
        
        # Add to queue button
        add_queue_btn = tk.Button(buttons_frame, text="➕ Thêm vào hàng chờ", 
                                 command=self.add_to_queue, font=self.default_font,
                                 bg="#3498db", fg="white", relief=tk.FLAT, padx=20, pady=8,
                                 cursor="hand2")
        add_queue_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Download now button
        download_now_btn = tk.Button(buttons_frame, text="⚡ Tải ngay", 
                                    command=self.download_now, font=self.default_font,
                                    bg="#e74c3c", fg="white", relief=tk.FLAT, padx=20, pady=8,
                                    cursor="hand2")
        download_now_btn.pack(side=tk.LEFT)
        
        # Output Path Section
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
        
        # Status Section
        status_section = tk.LabelFrame(self.download_frame, text="📊 Trạng thái", 
                                      font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        status_section.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_section, variable=self.progress_var, 
                                           mode='determinate', length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(status_section, text="🔄 Sẵn sàng tải xuống", 
                                    font=self.default_font, bg="#ffffff", fg="#27ae60",
                                    wraplength=600, justify=tk.CENTER)
        self.status_label.pack(pady=5)
        
        # Download stats
        self.stats_label = tk.Label(status_section, text="📈 Đã tải: 0 file", 
                                   font=self.small_font, bg="#ffffff", fg="#7f8c8d")
        self.stats_label.pack(pady=5)
    
    def setup_files_tab(self):
        # Title
        title = tk.Label(self.files_frame, text="📁 File âm thanh đã tải", 
                        font=self.header_font, bg="#ffffff", fg="#2c3e50")
        title.pack(pady=(0, 15))
        
        # Toolbar
        toolbar = tk.Frame(self.files_frame, bg="#ffffff")
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        refresh_btn = tk.Button(toolbar, text="🔄 Làm mới", command=self.refresh_files,
                               font=self.default_font, bg="#3498db", fg="white", relief=tk.FLAT,
                               padx=15, pady=5, cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        open_folder_btn = tk.Button(toolbar, text="📂 Mở thư mục", command=self.open_download_folder,
                                   font=self.default_font, bg="#27ae60", fg="white", relief=tk.FLAT,
                                   padx=15, pady=5, cursor="hand2")
        open_folder_btn.pack(side=tk.LEFT)
        
        # Files list frame
        list_frame = tk.Frame(self.files_frame, bg="#ffffff")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(list_frame, font=self.default_font, 
                                       yscrollcommand=scrollbar.set, relief=tk.FLAT,
                                       selectmode=tk.SINGLE, bg="#f8f9fa", 
                                       selectbackground="#3498db", selectforeground="white")
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Double click to open file
        self.files_listbox.bind("<Double-1>", self.open_selected_file)
        self.files_listbox.bind("<Button-3>", self.show_file_context_menu)  # Right click
        
        # Context menu
        self.file_context_menu = tk.Menu(self.app, tearoff=0)
        self.file_context_menu.add_command(label="🎵 Phát file", command=self.play_selected_file)
        self.file_context_menu.add_command(label="📂 Mở thư mục chứa", command=self.open_file_location)
        self.file_context_menu.add_command(label="📋 Copy đường dẫn", command=self.copy_file_path)
        self.file_context_menu.add_command(label="🗑️ Xóa file", command=self.delete_selected_file)
    
    def setup_queue_tab(self):
        # Title
        title = tk.Label(self.queue_frame, text="⏳ Hàng chờ tải xuống", 
                        font=self.header_font, bg="#ffffff", fg="#2c3e50")
        title.pack(pady=(0, 15))
        
        # Queue controls
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
        
        # Queue list
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
        
        # Queue info
        self.queue_info = tk.Label(self.queue_frame, text="📊 Hàng chờ trống", 
                                  font=self.small_font, bg="#ffffff", fg="#7f8c8d")
        self.queue_info.pack(pady=10)
    
    def setup_download_queue(self):
        self.queue_urls = []
    
    # Event handlers
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
        
        for i, url in enumerate(urls):
            self.app.after(0, lambda u=url, idx=i: self.update_download_status(f"🔄 Đang tải ({idx+1}/{total_urls}): {u[:50]}..."))
            self.app.after(0, lambda: self.progress_var.set((i / total_urls) * 100))
            
            success, message = download_audio(url, self.output_path_var.get())
            
            if success:
                success_count += 1
                self.app.after(0, lambda msg=message: self.add_to_history(url, msg))
            
            time.sleep(0.5)  # Tránh spam
        
        # Hoàn thành
        self.app.after(0, lambda: self.progress_var.set(100))
        self.app.after(0, lambda: self.update_download_status(f"✅ Hoàn thành! Đã tải thành công {success_count}/{total_urls} file"))
        self.app.after(0, self.download_completed)
        self.app.after(0, self.refresh_files)
        
        # Mở thư mục sau khi hoàn thành
        if success_count > 0:
            time.sleep(1)
            self.app.after(0, self.open_download_folder)
    
    def download_completed(self):
        self.is_downloading = False
        self.start_queue_btn.config(state=tk.NORMAL, text="▶️ Bắt đầu tải")
        self.progress_var.set(0)
    
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
        self.files_listbox.delete(0, tk.END)
        download_path = self.output_path_var.get()
        
        if not os.path.exists(download_path):
            self.files_listbox.insert(tk.END, "📂 Thư mục chưa tồn tại")
            return
        
        audio_extensions = ['.mp3', '.m4a', '.webm', '.wav', '.aac', '.ogg', '.wma', '.flac']
        files = []
        
        for file in os.listdir(download_path):
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                file_path = os.path.join(download_path, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                files.append((file, file_size))
        
        # Sắp xếp theo thời gian tạo (mới nhất trước)
        files.sort(key=lambda x: os.path.getctime(os.path.join(download_path, x[0])), reverse=True)
        
        for file, size in files:
            self.files_listbox.insert(tk.END, f"🎵 {file} ({size:.1f} MB)")
        
        if not files:
            self.files_listbox.insert(tk.END, "📭 Chưa có file nào được tải")
        
        # Cập nhật stats
        self.stats_label.config(text=f"📈 Đã tải: {len(files)} file")
    
    def open_download_folder(self):
        path = self.output_path_var.get()
        if not os.path.exists(path):
            os.makedirs(path)
        
        try:
            if os.name == 'nt':
                os.startfile(path)
            elif os.name == 'posix':
                if os.uname().sysname == 'Darwin':
                    os.system(f'open "{path}"')
                else:
                    os.system(f'xdg-open "{path}"')
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")
    
    def open_selected_file(self, event):
        selection = self.files_listbox.curselection()
        if selection:
            file_text = self.files_listbox.get(selection[0])
            if file_text.startswith("🎵"):
                filename = file_text.split(" (")[0].replace("🎵 ", "")
                file_path = os.path.join(self.output_path_var.get(), filename)
                try:
                    if os.name == 'nt':
                        os.startfile(file_path)
                    elif os.name == 'posix':
                        if os.uname().sysname == 'Darwin':
                            os.system(f'open "{file_path}"')
                        else:
                            os.system(f'xdg-open "{file_path}"')
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể mở file: {e}")
    
    def show_file_context_menu(self, event):
        try:
            self.files_listbox.selection_clear(0, tk.END)
            self.files_listbox.selection_set(self.files_listbox.nearest(event.y))
            self.file_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.file_context_menu.grab_release()
    
    def play_selected_file(self):
        self.open_selected_file(None)
    
    def open_file_location(self):
        selection = self.files_listbox.curselection()
        if selection:
            file_text = self.files_listbox.get(selection[0])
            if file_text.startswith("🎵"):
                filename = file_text.split(" (")[0].replace("🎵 ", "")
                file_path = os.path.join(self.output_path_var.get(), filename)
                folder_path = os.path.dirname(file_path)
                self.open_download_folder()
    
    def copy_file_path(self):
        selection = self.files_listbox.curselection()
        if selection:
            file_text = self.files_listbox.get(selection[0])
            if file_text.startswith("🎵"):
                filename = file_text.split(" (")[0].replace("🎵 ", "")
                file_path = os.path.join(self.output_path_var.get(), filename)
                self.app.clipboard_clear()
                self.app.clipboard_append(file_path)
                messagebox.showinfo("Thành công", "Đã copy đường dẫn file!")
    
    def delete_selected_file(self):
        selection = self.files_listbox.curselection()
        if selection:
            file_text = self.files_listbox.get(selection[0])
            if file_text.startswith("🎵"):
                filename = file_text.split(" (")[0].replace("🎵 ", "")
                if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa file:\n{filename}?"):
                    file_path = os.path.join(self.output_path_var.get(), filename)
                    try:
                        os.remove(file_path)
                        self.refresh_files()
                        messagebox.showinfo("Thành công", "Đã xóa file!")
                    except Exception as e:
                        messagebox.showerror("Lỗi", f"Không thể xóa file: {e}")
    
    def add_to_history(self, url, filename):
        self.download_history.append({
            'url': url,
            'filename': filename,
            'timestamp': datetime.now().isoformat()
        })
        self.save_download_history()
    
    def load_download_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.download_history = json.load(f)
        except:
            self.download_history = []
    
    def save_download_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.download_history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def run(self):
        # Load files on startup
        self.refresh_files()
        self.app.mainloop()

# Chạy ứng dụng
if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.run()