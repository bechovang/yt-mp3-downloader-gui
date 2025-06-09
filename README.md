# YouTube Audio Downloader (GUI & CLI)

Một ứng dụng đơn giản để tải âm thanh từ các video YouTube, hỗ trợ cả giao diện đồ họa (GUI) và dòng lệnh (CLI).

![Giao diện ứng dụng](https://i.imgur.com/your-screenshot-url.png) <!-- Bạn nên thay thế bằng ảnh chụp màn hình thực tế của ứng dụng -->

## Giới thiệu

Ứng dụng này cho phép bạn nhanh chóng tải về bản âm thanh gốc từ một video YouTube bất kỳ. Bạn có thể dán link video, chọn thư mục lưu và ứng dụng sẽ tự động tải về file âm thanh với chất lượng tốt nhất có sẵn mà không cần chuyển đổi định dạng.

## Tính năng

-   **Giao diện đồ họa (GUI):** Dễ sử dụng với các nút bấm và trường nhập liệu trực quan.
-   **Giao diện dòng lệnh (CLI):** Dành cho những ai thích làm việc trên terminal.
-   **Chất lượng gốc:** Tải về file âm thanh chất lượng cao nhất mà YouTube cung cấp.
-   **Không chuyển đổi:** Giữ nguyên định dạng gốc của audio (thường là `.m4a` hoặc `.webm`), đảm bảo không làm giảm chất lượng.
-   **Đa nền tảng:** Hoạt động trên Windows, macOS và Linux.
-   **Tự động mở thư mục:** Sau khi tải xong, ứng dụng sẽ tự động mở thư mục chứa file đã tải.

## Cài đặt

### Yêu cầu

-   Python 3.6+
-   `pip` (trình quản lý gói của Python)
-   `venv` (để tạo môi trường ảo, khuyến khích)

### Các bước cài đặt

0. tải python 3.10.9

1.  **Clone repository này về máy:**

    ```bash
    git clone https://github.com/your-username/yt-mp3-downloader-gui.git
    cd yt-mp3-downloader-gui
    ```

2.  **Tạo và kích hoạt môi trường ảo (`venv`):**

    *   **Trên Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    *   **Trên macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Cài đặt các gói cần thiết:**

    ```bash
    pip install -r requirements.txt
    ```

## Cách sử dụng

Bạn có thể chạy ứng dụng theo hai cách:

### 1. Chạy với giao diện đồ họa (GUI)

Thực thi file `gui_app.py`:

```bash
python gui_app.py
```

Một cửa sổ sẽ hiện lên. Bạn chỉ cần:
- Dán URL của video YouTube vào ô nhập liệu.
- (Tùy chọn) Nhấn nút "Chọn thư mục" để thay đổi nơi lưu file. Mặc định, file sẽ được lưu vào thư mục `downloaded_audios_gui`.
- Nhấn nút "Tải".

### 2. Chạy bằng dòng lệnh (CLI)

Thực thi file `main.py`:

```bash
python main.py
```

Ứng dụng sẽ hỏi bạn:
- Nhập link YouTube.
- Nhập đường dẫn thư mục lưu file. Nếu bạn bỏ trống, file sẽ được lưu vào thư mục `downloaded_audios`.

## Hướng phát triển trong tương lai: Android với Termux

Đây là một dự án có tiềm năng để phát triển thành một công cụ tiện lợi trên các thiết bị Android thông qua **Termux**.

### Tại sao lại là Termux?

**Termux** là một trình giả lập terminal mạnh mẽ cho Android, cho phép chạy các môi trường Linux và các công cụ dòng lệnh trực tiếp trên điện thoại mà không cần root. Điều này mở ra khả năng chạy các script Python như `yt-mp3-downloader-gui` trên Android.

### Lộ trình phát triển

Câu hỏi của bạn rất hay và thực tế. Bạn đang muốn xây dựng một ứng dụng Android để **tương tác với Termux**, hoặc thậm chí là **sửa lại Termux để tạo giao diện thân thiện hơn** cho người dùng phổ thông, chỉ tập trung vào chức năng tải video từ YouTube.

Dưới đây là phân tích chi tiết về 2 hướng bạn nêu:

---

## 🔹 **Hướng 1: Xây dựng App Android tương tác với Termux**

### ✅ Có thể làm được không?
- **Có**, hoàn toàn có thể.
- Termux hoạt động như một môi trường Linux trên Android, và bạn có thể chạy các lệnh shell, script Python,... trong đó.
- Nếu bạn xây dựng một ứng dụng Android (ví dụ bằng Kotlin/Java hoặc Flutter), bạn **có thể gọi Termux để chạy các lệnh thông qua Intent hoặc Shell**.

### 🧱 Cách tiếp cận:
#### A. Dùng Termux API
Termux cung cấp một số API giúp các ứng dụng khác tương tác với nó qua `termux-api` package.

Ví dụ:
```bash
pkg install termux-api
```

Bạn có thể gọi các lệnh như:
```bash
termux-notification -t "Thông báo" -c "Đang tải nhạc..."
termux-toast "Chức năng này chưa khả dụng"
```

Tuy nhiên, để chạy một script Python từ ứng dụng Android thì bạn cần:
- Gửi lệnh tới Termux thông qua Intent.
- Hoặc chạy lệnh shell từ ứng dụng Android bằng cách sử dụng thư viện root/shell execution (nhưng sẽ phức tạp).

#### B. Tự viết ứng dụng Android gọi Termux

Ứng dụng của bạn có thể:
1. Kiểm tra xem Termux đã được cài chưa.
2. Mở Termux và gửi lệnh tự động (qua Intent).
3. Ví dụ mở Termux và chạy một script:
```kotlin
val intent = Intent()
intent.setClassName("com.termux", "com.termux.app.RunCommandService")
intent.putExtra("com.termux.RUN_COMMAND", "cd /sdcard/ytdownloader && python main.py")
intent.putExtra("com.termux.BACK_ON_ALL_PROCESSES_FINISH", true)
startService(intent)
```

> ⚠️ Lưu ý: Đây là cách sử dụng **Termux Plugin API** – bạn cần nghiên cứu kỹ [Termux API documentation](https://wiki.termux.com/wiki/Android_Interface_Integration).

### ✅ Ưu điểm:
- Không cần sửa Termux.
- Dễ bảo trì, cập nhật.
- Người dùng chỉ cần cài Termux + app của bạn.

### ❌ Nhược điểm:
- Phụ thuộc vào Termux.
- Không phải tất cả thiết bị đều hỗ trợ việc gọi Intent đến Termux.
- Cần hướng dẫn người dùng cài đặt Termux và các gói phụ trợ.

---

## 🔹 **Hướng 2: Clone Termux và chỉnh sửa giao diện**

### ✅ Có thể làm được không?
- **Có thể**, nhưng phức tạp hơn nhiều.

Termux là một ứng dụng mã nguồn mở (open-source) trên GitHub:
👉 https://github.com/termux/termux-app

Bạn có thể clone về, build lại và tùy biến UI của nó.

### 🧱 Cách tiếp cận:
1. Clone repo:
   ```bash
   git clone https://github.com/termux/termux-app
   ```
2. Import vào Android Studio.
3. Chỉnh sửa layout XML để tạo một giao diện đơn giản (ví dụ: EditText để nhập link, Button để bắt đầu tải).
4. Khi người dùng nhấn nút, chạy lệnh trong terminal (bằng lớp `TerminalSession`) để chạy script Python của bạn.

### ✅ Ưu điểm:
- Toàn bộ trong một ứng dụng, không cần Termux ngoài.
- Có thể tối ưu hóa giao diện riêng, phù hợp mục tiêu cụ thể (chỉ tải YouTube).

### ❌ Nhược điểm:
- Phức tạp, đòi hỏi hiểu biết về lập trình Android Native.
- Khó theo kịp các bản cập nhật mới của Termux.
- Khối lượng công việc lớn nếu bạn không quen với hệ thống terminal emulator.

---

## 🔹 Hướng đi gợi ý dành cho bạn (theo mức độ dễ đến khó)

| Cấp độ | Hướng đi | Mô tả |
|--------|----------|-------|
| 🔹 Dễ | Viết script `.sh` + file `README.md` hướng dẫn người dùng | Chỉ cần Termux + vài lệnh là chạy được. Dành cho người dùng kỹ thuật. |
| 🔸 Khá | Viết một app Android nhỏ để mở Termux và chạy lệnh tải video | Sử dụng Termux API, không cần chỉnh sửa Termux. Giao diện đơn giản. |
| 🔷 Khó | Clone Termux, tùy biến giao diện, tích hợp sẵn script tải video | Một ứng dụng độc lập, đẹp, nhưng mất nhiều thời gian phát triển. |

---

## 💡 Gợi ý thực tế:
Nếu bạn muốn một sản phẩm **dễ dùng, thân thiện với người dùng phổ thông**, hãy chọn hướng:

> **Viết một ứng dụng Android đơn giản (Flutter hoặc Kotlin)**  
> - Có ô nhập link YouTube, nút “Tải về”
> - Bên trong app gọi Termux API hoặc chạy yt-dlp bằng subprocess (nếu bạn nhúng yt-dlp thành binary hoặc dùng Python-in-Android như Pydroid3)
> - Hiển thị trạng thái tải xuống, thông báo hoàn tất

-------------------------------

Cảm ơn bạn đã đặt câu hỏi rất thực tế và thiết thực. Dưới đây là giải thích rõ ràng về:

1. **Termux API có tốn tiền không?**
2. **Dùng `yt-dlp` bằng `subprocess` trong Android – ưu, nhược điểm như thế nào?**

---

## 🔹 1. Termux API có tốn tiền không?

### ✅ **Không**, Termux và Termux API hoàn toàn **miễn phí**.

- **Termux** là một ứng dụng terminal giả lập Linux trên Android, **miễn phí 100%**, có sẵn trên Google Play và F-Droid.
- **Termux API** cũng là một phần mở rộng của Termux, **miễn phí**, cho phép bạn sử dụng các chức năng Android (notification, clipboard, sensor,...) thông qua dòng lệnh hoặc script shell/Python.

#### Cách cài đặt Termux API:
```bash
pkg install termux-api
```

> Ví dụ: Gửi thông báo từ script Python/shell:
```bash
termux-notification -t "Tải xong" -c "Bài nhạc đã tải thành công!"
```

👉 Như vậy, bạn **không cần trả bất kỳ khoản phí nào** để dùng Termux và các API của nó.

---

## 🔹 2. Dùng `yt-dlp` bằng `subprocess` trong Android – ưu & nhược điểm

Nếu bạn đang xây dựng một ứng dụng Android (bằng Kotlin, Java hoặc Flutter), bạn có thể chạy `yt-dlp` như một tiến trình con (child process) thông qua `subprocess`.

Trong ngữ cảnh Android, bạn có thể:
- Chạy yt-dlp như một file binary được biên dịch trước (ví dụ: `yt-dlp` phiên bản standalone).
- Hoặc chạy thông qua Python + subprocess nếu có môi trường Python (như Pydroid 3 hoặc Termux).

---

### ✅ **Ưu điểm:**

| Ưu điểm | Mô tả |
|--------|-------|
| **Đơn giản hóa logic** | Bạn chỉ cần gọi `subprocess.run()` với lệnh phù hợp. |
| **Không cần phụ thuộc GUI của Termux** | Có thể tích hợp trực tiếp vào app Android mà không yêu cầu người dùng phải hiểu biết về command line. |
| **Tích hợp tốt với giao diện người dùng** | Hiển thị trạng thái tải xuống, lỗi, % tiến độ dễ dàng hơn. |

---

### ❌ **Nhược điểm:**

| Nhược điểm | Mô tả |
|-----------|-------|
| **Phụ thuộc vào môi trường chạy** | Nếu dùng Python thì phải có Python runtime (Pydroid, Termux,...). |
| **Khó debug lỗi stdout/stderr** | Cần bắt và xử lý output của subprocess để hiển thị lỗi chính xác. |
| **Hiệu suất thấp hơn native code** | Vì chạy dưới dạng tiến trình con, không tối ưu bằng cách biên dịch trực tiếp thành thư viện native. |
| **Không tương tác mượt như SDK gốc** | Không tận dụng hết API của YouTube như luồng streaming, playlist handling,... nếu chỉ dùng subprocess đơn thuần. |

---

## 💡 Gợi ý thực tế:

### Nếu bạn làm app Android cơ bản (giao diện đơn giản, chỉ nhập link + tải video):
- Dùng `subprocess` để chạy `yt-dlp` là hợp lý nhất.
- Có thể chọn:
   - **Termux + Python**: Cài Python và `yt-dlp`, sau đó gọi bằng `subprocess`.
   - **Pydroid 3**: Môi trường Python dành cho Android, hỗ trợ chạy script Python đầy đủ.
   - **Embed yt-dlp binary**: Nếu bạn muốn không phụ thuộc vào Python, bạn có thể biên dịch `yt-dlp` thành binary và chạy trực tiếp bằng `subprocess`.

---

## 🧪 Ví dụ mẫu chạy `yt-dlp` bằng `subprocess` trong Python (trên Termux):

```python
import subprocess

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
output_path = "/sdcard/Download/%(title)s.%(ext)s"

cmd = [
    "yt-dlp",
    "-f", "bestaudio/best",
    "-o", output_path,
    url
]

result = subprocess.run(cmd, capture_output=True, text=True)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
```

-----------------------------------------

Tuyệt vời! Dưới đây là **kế hoạch chi tiết (detailed planning)** để **tích hợp `yt-dlp` vào một ứng dụng Android thuần (native Android app)**. Mục tiêu là tạo ra một ứng dụng đơn giản, thân thiện với người dùng phổ thông, cho phép họ:

- Nhập link video YouTube.
- Chọn định dạng tải về (ví dụ: MP3 hoặc MP4).
- Tải file về thiết bị.
- Hiển thị tiến trình và thông báo hoàn tất.

---

# 🎯 **Mục tiêu chính**
Xây dựng một ứng dụng Android thuần có khả năng chạy `yt-dlp` như một công cụ nền để tải video từ YouTube.

---

# 🔧 **Công nghệ sử dụng**

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ lập trình | Kotlin |
| Giao diện người dùng | Jetpack Compose hoặc XML Layout |
| Xử lý dòng lệnh / subprocess | `ProcessBuilder`, `Runtime.getRuntime().exec()` |
| yt-dlp phiên bản | standalone binary hoặc chạy qua Python |
| Lưu trữ dữ liệu | Internal/External Storage |
| Thông báo người dùng | Toast / Dialog / Notification |

---

# 📦 **Yêu cầu hệ thống**

Ứng dụng sẽ hoạt động trên Android 8.0 (API level 26) trở lên.

---

# 🗂️ **Cấu trúc dự án đề xuất**

```
/app
 ├── src/main/
 │   ├── java/                # Java code nếu cần (tuỳ chọn)
 │   ├── kotlin/              # Kotlin source files
 │   ├── res/                 # Tài nguyên giao diện (layout, drawable,...)
 │   └── AndroidManifest.xml
 ├── build.gradle             # Cấu hình module app
 └── assets/                  # Thư mục chứa yt-dlp binary hoặc script
```

---

# 📋 **Kế hoạch phát triển theo từng giai đoạn**

## 🚧 **Giai đoạn 1: Chuẩn bị môi trường & tích hợp yt-dlp**

### Mục tiêu:
- Có thể chạy được `yt-dlp` trong ứng dụng Android.

### Các bước thực hiện:
1. **Chọn phiên bản yt-dlp phù hợp**:
   - Tùy chọn 1: `yt-dlp` standalone binary (không cần Python).
   - Tùy chọn 2: Dùng `Pydroid 3` hoặc `Termux` + Python + pip install yt-dlp.
   > ✅ Đề xuất: Nếu bạn muốn không phụ thuộc Termux → nên chọn `yt-dlp` standalone.

2. **Biên dịch hoặc tải `yt-dlp` binary dành cho Android**:
   - Có thể dùng bản đã biên dịch sẵn hoặc tự build bằng NDK.

3. **Đưa binary vào thư mục `assets` của ứng dụng**:
   - Khi cài đặt lần đầu, sao chép binary vào `/data/data/<your.package>/files`.

4. **Cho phép quyền thực thi file binary**:
   ```kotlin
   val destFile = getDir("bin", Context.MODE_PRIVATE).resolve("yt-dlp")
   destFile.setExecutable(true)
   ```

5. **Kiểm tra chạy thử command line**:
   ```kotlin
   val process = Runtime.getRuntime().exec("./yt-dlp --version")
   // hoặc
   val process = ProcessBuilder().command("./yt-dlp", "-f", "bestaudio", "https://youtube.com/watch?v=...")
   ```

---

## 🚧 **Giai đoạn 2: Xây dựng giao diện cơ bản**

### Mục tiêu:
- Người dùng nhập link, chọn tùy chọn, nhấn nút “Tải xuống”.

### Các thành phần UI:
- EditText: ô nhập link.
- RadioButton / Spinner: chọn định dạng (MP3 / MP4).
- Button: “Tải xuống”.
- ProgressBar: hiển thị trạng thái tải.
- TextView: hiển thị log hoặc lỗi.

### Ví dụ (sử dụng Jetpack Compose):

```kotlin
@Composable
fun DownloadScreen(viewModel: DownloadViewModel) {
    Column(modifier = Modifier.padding(16.dp)) {
        TextField(
            value = viewModel.url,
            onValueChange = { viewModel.url = it },
            label = { Text("Nhập link YouTube") }
        )
        Spacer(modifier = Modifier.height(8.dp))
        Row {
            RadioButton(
                selected = viewModel.format == "mp3",
                onClick = { viewModel.format = "mp3" })
            Text("MP3 (Audio)")
            RadioButton(
                selected = viewModel.format == "mp4",
                onClick = { viewModel.format = "mp4" })
            Text("MP4 (Video)")
        }
        Button(onClick = { viewModel.startDownload() }) {
            Text("Tải xuống")
        }
    }
}
```

---

## 🚧 **Giai đoạn 3: Xử lý logic tải video**

### Mục tiêu:
- Gọi `yt-dlp` từ Kotlin.
- Nhận kết quả stdout/stderr.
- Hiển thị tiến trình tải.

### Cách làm:
1. **Xây dựng câu lệnh phù hợp**:
   ```kotlin
   val args = mutableListOf<String>()
   args.add("./yt-dlp")
   if (format == "mp3") {
       args.add("-x") // extract audio
       args.add("--audio-format") 
       args.add("mp3")
   } else {
       args.add("-f")
       args.add("bestvideo+bestaudio")
   }
   args.add(url)
   ```

2. **Thực thi bằng `ProcessBuilder`**:
   ```kotlin
   val process = ProcessBuilder()
       .command(args)
       .redirectErrorStream(true)
       .start()
   ```

3. **Theo dõi tiến trình bằng luồng con (Thread)**:
   - Đọc stdout và stderr để hiển thị progress hoặc error.

4. **Lưu file tải về vào bộ nhớ**:
   - Sử dụng `MediaStore` hoặc `Context.getExternalFilesDir()`.

5. **Hiển thị thông báo khi hoàn tất**:
   - Dùng `NotificationCompat` hoặc `Toast`.

---

## 🚧 **Giai đoạn 4: Kiểm thử & tối ưu**

### Mục tiêu:
- Ứng dụng chạy ổn định trên nhiều thiết bị.
- Xử lý lỗi tốt, hỗ trợ resume download, quản lý đường dẫn lưu trữ.

### Các việc cần làm:
- Thử nghiệm với nhiều link khác nhau (playlist, short, private,…).
- Xử lý các lỗi: mạng yếu, không đủ bộ nhớ, URL sai,...
- Cho phép người dùng chọn nơi lưu file.
- Tối ưu hiệu suất và pin.

---

## 🚧 **Giai đoạn 5: Phát hành ứng dụng (tuỳ chọn)**

Nếu bạn muốn chia sẻ hoặc phát hành ứng dụng:

### Nền tảng phát hành:
- Google Play Store (cần đăng ký tài khoản nhà phát triển).
- F-Droid (miễn phí, mã nguồn mở).
- APK local (chia sẻ dưới dạng file `.apk`).

### Yêu cầu pháp lý:
- Tuân thủ điều khoản của YouTube.
- Không vi phạm luật về quyền riêng tư và bản quyền.

---

# 🧰 **Công cụ hỗ trợ đề xuất**

| Công cụ | Mục đích |
|--------|----------|
| Android Studio | IDE chính để xây dựng ứng dụng |
| Termux | Test `yt-dlp` trước khi tích hợp |
| Pydroid 3 | Dùng thử `yt-dlp` với Python nếu không dùng binary |
| FFmpeg | Tùy chọn: chuyển đổi định dạng âm thanh/video |
| Logcat | Debug lỗi trong quá trình chạy subprocess |

---

# 📌 Kết luận

Việc tích hợp `yt-dlp` vào ứng dụng Android thuần là **hoàn toàn khả thi**, nhưng yêu cầu bạn phải xử lý khá nhiều vấn đề liên quan đến:

- Quản lý file binary trên Android.
- Thực thi subprocess và đọc output.
- Thiết kế giao diện người dùng thân thiện.
- Bảo mật và quyền truy cập bộ nhớ.

---

🎯 **Bạn có thể bắt đầu từ đâu?**
- Viết một ứng dụng nhỏ chỉ gọi `yt-dlp` bằng subprocess.
- Sau đó thêm giao diện đơn giản, rồi mở rộng dần tính năng.

---

📩 Nếu bạn cần mình giúp viết từng phần cụ thể như:
- Code mẫu Kotlin chạy `yt-dlp`.
- Demo giao diện Jetpack Compose.
- Cách đưa binary vào asset và chạy.
=> Chỉ cần nói rõ bạn muốn bắt đầu từ đâu nhé! Mình sẽ hướng dẫn từng bước chi tiết 😊
