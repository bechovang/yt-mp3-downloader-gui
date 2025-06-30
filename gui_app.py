# Tên tệp: app_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkFont
from downloader import download_media  # Import hàm mới
import threading
import os
import time
from datetime import datetime
import json

class YouTubeDownloaderApp:
    def __init__(self):
        self.app = tk.Tk()
        self.setup_window()
        self.setup_fonts()
        self.setup_variables()
        self.setup_ui()
        self.load_download_history()

    def setup_window(self):
        self.app.title("🚀 YouTube Downloader Pro")
        self.app.geometry("800x680")  # Tăng chiều cao cho các tùy chọn mới
        self.app.configure(bg="#f0f2f5")
        self.app.resizable(True, True)
        try:
            # Nếu có file icon.ico, nó sẽ được sử dụng
            self.app.iconbitmap("icon.ico")
        except:
            pass

    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.header_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")
        self.default_font = tkFont.Font(family="Segoe UI", size=10)
        self.small_font = tkFont.Font(family="Segoe UI", size=9)

    def setup_variables(self):
        self.output_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "Downloads"))
        self.is_downloading = False
        self.download_history = []
        self.history_file = "download_history.json"
        self.queue_urls = []
        self.download_type_var = tk.StringVar(value="audio")  # Biến cho lựa chọn audio/video

    def setup_ui(self):
        main_container = tk.Frame(self.app, bg="#f0f2f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        title_label = tk.Label(main_container, text="🚀 YouTube Downloader Pro",
                               font=self.title_font, bg="#f0f2f5", fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.download_frame = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=20)
        self.notebook.add(self.download_frame, text="📥 Tải xuống")
        self.queue_frame = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=20)
        self.notebook.add(self.queue_frame, text="⏳ Hàng chờ")
        self.setup_download_tab()
        self.setup_queue_tab()

    def setup_download_tab(self):
        # 1. Khung nhập URL
        url_section = tk.LabelFrame(self.download_frame, text="🔗 Nhập URL",
                                    font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        url_section.pack(fill=tk.X, pady=(0, 15))
        self.url_entry = tk.Text(url_section, height=4, font=self.default_font,
                                 wrap=tk.WORD, relief=tk.FLAT, bd=1, highlightbackground="#ddd", highlightthickness=1)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        placeholder_text = "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)..."
        self.url_entry.insert("1.0", placeholder_text)
        self.url_entry.config(fg="gray")
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)

        # 2. Khung Tùy chọn Tải xuống (MỚI)
        options_section = tk.LabelFrame(self.download_frame, text="⚙️ Chọn định dạng",
                                        font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=10)
        options_section.pack(fill=tk.X, pady=(0, 15))
        audio_rb = tk.Radiobutton(options_section, text="🎵 Âm thanh (Chất lượng cao nhất)",
                                  variable=self.download_type_var, value="audio",
                                  font=self.default_font, bg="#ffffff", anchor=tk.W)
        audio_rb.pack(fill=tk.X)
        video_rb = tk.Radiobutton(options_section, text="🎬 Video (MP4 1080p nếu có)",
                                  variable=self.download_type_var, value="video",
                                  font=self.default_font, bg="#ffffff", anchor=tk.W)
        video_rb.pack(fill=tk.X)

        # 3. Khung Nút hành động
        buttons_frame = tk.Frame(self.download_frame, bg="#ffffff")
        buttons_frame.pack(fill=tk.X, pady=(0, 15))
        add_queue_btn = tk.Button(buttons_frame, text="➕ Thêm vào hàng chờ", command=self.add_to_queue,
                                  font=self.default_font, bg="#3498db", fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        add_queue_btn.pack(side=tk.LEFT, padx=(0, 10))
        download_now_btn = tk.Button(buttons_frame, text="⚡ Tải ngay", command=self.download_now,
                                     font=self.default_font, bg="#e74c3c", fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        download_now_btn.pack(side=tk.LEFT)

        # 4. Khung Đường dẫn lưu
        path_section = tk.LabelFrame(self.download_frame, text="📂 Thư mục lưu",
                                     font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        path_section.pack(fill=tk.X, pady=(0, 15))
        path_frame = tk.Frame(path_section, bg="#ffffff")
        path_frame.pack(fill=tk.X)
        browse_btn = tk.Button(path_frame, text="📁 Chọn thư mục", command=self.browse_folder,
                               font=self.default_font, bg="#95a5a6", fg="white", relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.path_display = tk.Label(path_frame, text=f"📍 {self.output_path_var.get()}",
                                     font=self.default_font, bg="#ffffff", fg="#7f8c8d", wraplength=500, justify=tk.LEFT)
        self.path_display.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 5. Khung Trạng thái
        status_section = tk.LabelFrame(self.download_frame, text="📊 Trạng thái",
                                       font=self.header_font, bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
        status_section.pack(fill=tk.BOTH, expand=True)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_section, variable=self.progress_var, mode='determinate', length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        self.status_label = tk.Label(status_section, text="🔄 Sẵn sàng tải xuống",
                                     font=self.default_font, bg="#ffffff", fg="#27ae60", wraplength=600, justify=tk.CENTER)
        self.status_label.pack(pady=5)
        self.stats_label = tk.Label(status_section, text="📈 Tổng số file đã tải: 0 file",
                                    font=self.small_font, bg="#ffffff", fg="#7f8c8d")
        self.stats_label.pack(pady=5)

    def setup_queue_tab(self):
        title = tk.Label(self.queue_frame, text="⏳ Hàng chờ tải xuống", font=self.header_font, bg="#ffffff", fg="#2c3e50")
        title.pack(pady=(0, 15))
        controls_frame = tk.Frame(self.queue_frame, bg="#ffffff")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        self.start_queue_btn = tk.Button(controls_frame, text="▶️ Bắt đầu tải hàng chờ", command=self.start_queue_download,
                                         font=self.default_font, bg="#27ae60", fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.start_queue_btn.pack(side=tk.LEFT, padx=(0, 10))
        clear_queue_btn = tk.Button(controls_frame, text="🗑️ Xóa hàng chờ", command=self.clear_queue,
                                    font=self.default_font, bg="#e74c3c", fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        clear_queue_btn.pack(side=tk.LEFT)
        queue_list_frame = tk.Frame(self.queue_frame, bg="#ffffff")
        queue_list_frame.pack(fill=tk.BOTH, expand=True)
        queue_scrollbar = tk.Scrollbar(queue_list_frame)
        queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.queue_listbox = tk.Listbox(queue_list_frame, font=self.default_font, yscrollcommand=queue_scrollbar.set,
                                        relief=tk.FLAT, bg="#f8f9fa", selectbackground="#e74c3c", selectforeground="white")
        self.queue_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        queue_scrollbar.config(command=self.queue_listbox.yview)
        self.queue_info = tk.Label(self.queue_frame, text="📊 Hàng chờ trống", font=self.small_font, bg="#ffffff", fg="#7f8c8d")
        self.queue_info.pack(pady=10)

    def get_urls_from_entry(self):
        urls_text = self.url_entry.get("1.0", tk.END).strip()
        if not urls_text or urls_text == "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một URL!")
            return None
        return [url.strip() for url in urls_text.split('\n') if url.strip()]

    def download_now(self):
        if self.is_downloading:
            messagebox.showwarning("Đang tải", "Quá trình tải khác đang chạy!")
            return
        urls = self.get_urls_from_entry()
        if urls:
            download_type = self.download_type_var.get()
            self.start_download_process(urls, download_type)

    def start_queue_download(self):
        if not self.queue_urls:
            messagebox.showinfo("Thông báo", "Hàng chờ trống!")
            return
        if self.is_downloading:
            messagebox.showwarning("Đang tải", "Quá trình tải khác đang chạy!")
            return
        urls_to_download = [item['url'] for item in self.queue_urls]
        download_type = self.queue_urls[0]['type']
        self.start_download_process(urls_to_download, download_type, from_queue=True)

    def start_download_process(self, urls, download_type, from_queue=False):
        self.is_downloading = True
        self.start_queue_btn.config(state=tk.DISABLED, text="⏸️ Đang tải...")
        if from_queue:
            self.queue_urls.clear()
            self.queue_listbox.delete(0, tk.END)
            self.update_queue_info()
        download_thread = threading.Thread(target=self.download_multiple_urls, args=(urls, download_type))
        download_thread.daemon = True
        download_thread.start()

    def download_multiple_urls(self, urls, download_type):
        success_count = 0
        output_path = self.output_path_var.get()
        for i, url in enumerate(urls):
            status_msg = f"🔄 ({i+1}/{len(urls)}) Đang tải {download_type.upper()}..."
            self.app.after(0, self.update_download_status, status_msg)
            self.app.after(0, self.progress_var.set, (i / len(urls)) * 100)
            try:
                success, msg = download_media(url, output_path, download_type)
                if success:
                    success_count += 1
                    self.app.after(0, self.add_to_history, url, msg, download_type)
                else:
                    self.app.after(0, self.update_download_status, f"⚠️ Lỗi: {msg}")
                    time.sleep(2)
            except Exception as e:
                self.app.after(0, self.update_download_status, f"❌ Lỗi nghiêm trọng: {e}")
                time.sleep(2)
        final_msg = f"✅ Hoàn tất! {success_count}/{len(urls)} file đã được tải."
        self.app.after(0, self.update_download_status, final_msg)
        self.app.after(0, self.download_completed)
        if success_count > 0:
            time.sleep(1)
            self.app.after(0, self.open_download_folder)

    def download_completed(self):
        self.is_downloading = False
        self.start_queue_btn.config(state=tk.NORMAL, text="▶️ Bắt đầu tải hàng chờ")
        self.progress_var.set(0)
        self.refresh_files()

    def add_to_queue(self):
        urls = self.get_urls_from_entry()
        if not urls: return
        added_count = 0
        download_type = self.download_type_var.get()
        if self.queue_urls and self.queue_urls[0]['type'] != download_type:
            msg = f"Hàng chờ đang chứa các link tải '{self.queue_urls[0]['type']}'. Bạn có muốn xóa đi và thêm link mới để tải '{download_type}' không?"
            if not messagebox.askyesno("Xác nhận", msg): return
            self.clear_queue(confirm=False)
        for url in urls:
            if not any(item['url'] == url for item in self.queue_urls):
                self.queue_urls.append({'url': url, 'type': download_type})
                self.queue_listbox.insert(tk.END, f"[{download_type.upper()}] {url}")
                added_count += 1
        if added_count > 0:
            self.update_queue_info()
            self.url_entry.delete("1.0", tk.END)
            self.on_url_focus_out(None)
            messagebox.showinfo("Thành công", f"Đã thêm {added_count} URL vào hàng chờ!")
        else:
            messagebox.showinfo("Thông báo", "Các URL này đã có trong hàng chờ.")

    def clear_queue(self, confirm=True):
        if confirm and not messagebox.askyesno("Xác nhận", "Xóa toàn bộ hàng chờ?"):
            return
        self.queue_urls.clear()
        self.queue_listbox.delete(0, tk.END)
        self.update_queue_info()

    def refresh_files(self):
        path = self.output_path_var.get()
        num_files = 0
        if os.path.exists(path):
            try:
                num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and not f.startswith('.')])
            except Exception as e:
                print(f"Lỗi khi đếm file: {e}")
        self.stats_label.config(text=f"📈 Tổng số file đã tải: {num_files} file")

    def add_to_history(self, url, filename, download_type):
        self.download_history.append({'url': url, 'filename': filename, 'type': download_type, 'timestamp': datetime.now().isoformat()})
        self.save_download_history()

    def on_url_focus_in(self, event):
        if self.url_entry.get("1.0", tk.END).strip() == "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...":
            self.url_entry.delete("1.0", tk.END)
            self.url_entry.config(fg="black")

    def on_url_focus_out(self, event):
        if not self.url_entry.get("1.0", tk.END).strip():
            self.url_entry.insert("1.0", "Nhập một hoặc nhiều YouTube URL (mỗi URL một dòng)...")
            self.url_entry.config(fg="gray")

    def browse_folder(self):
        path = filedialog.askdirectory(initialdir=self.output_path_var.get())
        if path:
            self.output_path_var.set(path)
            self.path_display.config(text=f"📍 {path}")

    def update_download_status(self, message):
        self.status_label.config(text=message)

    def update_queue_info(self):
        count = len(self.queue_urls)
        if count == 0:
            self.queue_info.config(text="📊 Hàng chờ trống")
        else:
            q_type = self.queue_urls[0]['type'].upper()
            self.queue_info.config(text=f"📊 {count} URL trong hàng chờ (Loại: {q_type})")

    def open_download_folder(self):
        path = self.output_path_var.get()
        try:
            if os.name == 'nt': os.startfile(path)
            elif os.uname().sysname == 'Darwin': os.system(f'open "{path}"')
            else: os.system(f'xdg-open "{path}"')
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")

    def load_download_history(self):
        if not os.path.exists(self.history_file): return
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.download_history = json.load(f)
        except Exception as e:
            print(f"Lỗi tải lịch sử: {e}")
            self.download_history = []

    def save_download_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.download_history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi lưu lịch sử: {e}")

    def run(self):
        self.refresh_files()
        self.app.mainloop()

if __name__ == "__main__":
    app_instance = YouTubeDownloaderApp()
    app_instance.run()