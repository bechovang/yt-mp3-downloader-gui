import tkinter as tk
from tkinter import filedialog, messagebox
from downloader import download_audio
import threading
import os

# Hàm chạy tải trong thread riêng
def run_download_in_thread(url, path, result_label_widget, download_button_widget):
    download_button_widget.config(state=tk.DISABLED, text="Đang tải...")
    result_label_widget.config(text="🔄 Đang xử lý, vui lòng chờ...", fg="blue")
    success, message = download_audio(url, path)
    if success:
        result_label_widget.config(text=f"✅ {message}", fg="green")
        try:
            abs_path = os.path.realpath(path)
            if os.name == 'nt':
                os.startfile(abs_path)
            elif os.name == 'posix':
                if os.uname().sysname == 'Darwin':
                    os.system(f'open "{abs_path}"')
                else:
                    os.system(f'xdg-open "{abs_path}"')
        except Exception as e:
            print(f"(Không thể mở thư mục: {e})")
    else:
        result_label_widget.config(text=f"❌ {message}", fg="red")
    download_button_widget.config(state=tk.NORMAL, text="Tải")

def browse_folder():
    path = filedialog.askdirectory()
    if path:
        output_path_var.set(path)
        path_display_label.config(text=f"Lưu tại: {path}")

def start_download():
    url = url_entry.get().strip()
    output_dir = output_path_var.get().strip()
    if not url:
        messagebox.showerror("Lỗi", "Vui lòng nhập YouTube URL.")
        return
    if not output_dir:
        output_dir = os.path.join(os.getcwd(), "downloaded_audios_gui")
        output_path_var.set(output_dir)
        path_display_label.config(text=f"Lưu tại: {output_dir}")
    download_thread = threading.Thread(
        target=run_download_in_thread,
        args=(url, output_dir, result_label, download_btn)
    )
    download_thread.start()

# Khởi tạo giao diện
app = tk.Tk()
app.title("YouTube Audio Downloader")
app.geometry("500x300")

default_font = ("Arial", 10)

main_frame = tk.Frame(app, padx=10, pady=10)
main_frame.pack(expand=True, fill=tk.BOTH)

# Nhập URL
url_frame = tk.Frame(main_frame)
url_frame.pack(fill=tk.X, pady=5)
tk.Label(url_frame, text="YouTube URL:", font=default_font).pack(side=tk.LEFT, padx=(0, 5))
url_entry = tk.Entry(url_frame, width=50, font=default_font)
url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# Chọn thư mục lưu
path_frame = tk.Frame(main_frame)
path_frame.pack(fill=tk.X, pady=5)

initial_output_path = os.path.join(os.getcwd(), "downloaded_audios_gui")
output_path_var = tk.StringVar(value=initial_output_path)

tk.Button(path_frame, text="Chọn thư mục", command=browse_folder, font=default_font).pack(side=tk.LEFT)
path_display_label = tk.Label(path_frame, text=f"Lưu tại: {initial_output_path}", wraplength=380, justify=tk.LEFT, font=default_font)
path_display_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

# Nút tải
download_btn = tk.Button(main_frame, text="Tải", command=start_download, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
download_btn.pack(pady=15, ipadx=10, ipady=5)

# Hiển thị kết quả
result_label = tk.Label(main_frame, text="", font=default_font, wraplength=480)
result_label.pack(pady=5)

app.mainloop()