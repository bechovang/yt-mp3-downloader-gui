# yt-mp3-downloader-gui



## 🧩 MỤC TIÊU ỨNG DỤNG

* ✅ Nhập link YouTube
* ✅ Tải về file MP3 chất lượng cao
* ✅ Lưu tại thư mục do người dùng chọn (hoặc mặc định)
* ✅ Giao diện dòng lệnh hoặc GUI đơn giản

---

## 🗂️ CẤU TRÚC PROJECT (Dự kiến)

```
youtube_mp3_downloader/
├── main.py
├── downloader.py
├── requirements.txt
└── gui_app.py     # (tuỳ chọn nếu bạn làm GUI)
```

---

## 📌 STEP-BY-STEP PLANNING

### 🔹 **1. Cài đặt thư viện cần thiết**

Tạo `requirements.txt`:

```txt
yt-dlp
tkinter        # nếu dùng GUI
```

Cài bằng lệnh:

```bash
pip install -r requirements.txt
```

---

### 🔹 **2. Viết module tải MP3 – `downloader.py`**

```python
import yt_dlp

def download_mp3(url: str, output_path: str = "./"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
```

---

### 🔹 **3. Viết giao diện dòng lệnh – `main.py`**

```python
from downloader import download_mp3

if __name__ == "__main__":
    url = input("🔗 Nhập link YouTube cần tải MP3: ")
    path = input("📁 Nhập thư mục lưu file (Enter để mặc định): ").strip()
    if not path:
        path = "."

    try:
        download_mp3(url, path)
        print("✅ Tải MP3 thành công!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
```

---

### 🔹 **4. (Tuỳ chọn) Giao diện đồ hoạ đơn giản – `gui_app.py`**

```python
import tkinter as tk
from tkinter import filedialog
from downloader import download_mp3

def browse_folder():
    path = filedialog.askdirectory()
    if path:
        output_path.set(path)

def start_download():
    try:
        download_mp3(url_entry.get(), output_path.get())
        result_label.config(text="✅ Tải thành công!", fg="green")
    except Exception as e:
        result_label.config(text=f"❌ Lỗi: {e}", fg="red")

app = tk.Tk()
app.title("YouTube to MP3 Downloader")

url_label = tk.Label(app, text="YouTube URL:")
url_label.pack()
url_entry = tk.Entry(app, width=50)
url_entry.pack()

output_path = tk.StringVar(value=".")
folder_btn = tk.Button(app, text="Chọn thư mục lưu", command=browse_folder)
folder_btn.pack()

download_btn = tk.Button(app, text="Tải MP3", command=start_download)
download_btn.pack()

result_label = tk.Label(app, text="")
result_label.pack()

app.mainloop()
```

---

## 🚀 CÁCH CHẠY ỨNG DỤNG

### CLI:

```bash
python main.py
```

### GUI:

```bash
python gui_app.py
```

---

## 🎁 GỢI Ý MỞ RỘNG

* ✅ Hỗ trợ tải playlist
* ✅ Cho phép chọn định dạng khác (m4a, wav,...)
* ✅ Giao diện đẹp hơn với PyQt, customtkinter
* ✅ Cho phép dán link tự động từ clipboard
* ✅ Gói app thành `.exe` bằng `pyinstaller`

---

Nếu bạn muốn, mình có thể:

* Nén trọn project mẫu gửi bạn (.zip)
* Viết thêm tính năng nâng cao
* Hướng dẫn đóng gói thành `.exe` Windows



-------------------------------




Mặc định, khi bạn chạy lệnh `yt-dlp` trong **Command Prompt**, thì file MP3 sẽ được lưu **ngay tại thư mục hiện tại của CMD** – tức là nơi bạn đang đứng trong dòng lệnh.

---

## 📍 **Cách kiểm tra nơi lưu file**

1. Khi bạn mở **cmd**, hãy xem dòng như sau:

   ```cmd
   C:\Users\Wincy>
   ```

   👉 Nghĩa là file sẽ được lưu ở thư mục `C:\Users\Wincy`

2. Nếu bạn đã chuyển thư mục bằng lệnh `cd`, ví dụ:

   ```cmd
   cd C:\yt-dlp
   ```

   👉 Thì file sẽ được lưu ở `C:\yt-dlp`

---

## ✅ **Cách chỉ định thư mục lưu file**

Bạn có thể thêm tùy chọn `-o` để chọn nơi lưu rõ ràng:

### Ví dụ: lưu vào ổ D, thư mục NhacYT

```cmd
yt-dlp.exe -f bestaudio --extract-audio --audio-format mp3 -o "D:\NhacYT\%(title)s.%(ext)s" https://youtu.be/dQw4w9WgXcQ
```

> Nếu thư mục `D:\NhacYT` chưa tồn tại, bạn nên tạo trước.

---

## 🧠 Gợi ý:

Bạn có thể thêm lệnh `explorer .` ngay sau đó để mở thư mục hiện tại trên Windows Explorer:

```cmd
explorer .
```

---

Nếu bạn chưa chắc mình đang ở thư mục nào trong CMD, hãy dùng lệnh:

```cmd
cd
```

Nó sẽ hiển thị đường dẫn hiện tại.

---

Bạn có muốn mình viết sẵn 1 file `.bat` để bạn chỉ cần **double-click là tải MP3 từ YouTube**?

