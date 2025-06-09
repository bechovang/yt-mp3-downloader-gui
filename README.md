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

1.  **Tương thích với Termux:**
    *   Kiểm tra và đảm bảo các thư viện (`yt-dlp`) hoạt động tốt trên môi trường của Termux.
    *   Cần cài đặt Python và các gói cần thiết trong Termux:
        ```bash
        pkg install python
        pip install yt-dlp
        ```
    *   Phiên bản CLI (`main.py`) sẽ là trọng tâm chính vì Termux không hỗ trợ GUI Tkinter một cách tự nhiên.

2.  **Tạo script tiện lợi:**
    *   Viết một script shell (`.sh`) đơn giản để người dùng có thể chạy ứng dụng chỉ bằng một lệnh ngắn gọn trong Termux.
    *   Script này sẽ tự động điều hướng đến thư mục dự án và thực thi file `main.py`.

3.  **Hỗ trợ lưu trữ trên Android:**
    *   Sử dụng `termux-storage-setup` để cho phép Termux truy cập vào bộ nhớ trong của điện thoại.
    *   Sửa đổi code để mặc định lưu các file tải về vào các thư mục công cộng như `Download` hoặc `Music` trên điện thoại.

4.  **(Nâng cao) Giao diện người dùng đơn giản:**
    *   Thay vì GUI, có thể xây dựng một giao diện dựa trên text (TUI - Text-based User Interface) bằng các thư viện như `dialog` (thông qua shell script) hoặc các thư viện Python như `whiptail` để làm cho phiên bản CLI thân thiện hơn với người dùng không chuyên.

### Ví dụ cách chạy trên Termux (sau khi phát triển)

1.  Mở Termux.
2.  Chạy script cài đặt (chỉ lần đầu):
    ```bash
    sh setup-termux.sh
    ```
3.  Chạy ứng dụng:
    ```bash
    ./start-downloader.sh
    ```
4.  Làm theo hướng dẫn trên màn hình để dán link và tải nhạc.

Đây là một hướng đi rất khả thi để biến một công cụ desktop đơn giản thành một tiện ích di động mạnh mẽ cho người dùng Android.

