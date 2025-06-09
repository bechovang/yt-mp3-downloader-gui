import yt_dlp
import os

def download_audio(url: str, output_path: str = "."):
    """
    Tải file âm thanh gốc từ YouTube mà KHÔNG dùng FFmpeg để chuyển đổi.
    Args:
        url (str): Link YouTube.
        output_path (str): Thư mục lưu file. Mặc định là thư mục hiện tại.
    """
    # Đảm bảo thư mục output tồn tại
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Đã tạo thư mục: {output_path}")

    ydl_opts = {
        'format': 'bestaudio/best',  # Chọn chất lượng âm thanh tốt nhất có sẵn
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Lưu theo tên và định dạng gốc
        'quiet': False,  # Hiện log để biết tiến trình
        'noplaylist': True,  # Không tải playlist nếu link là playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Đang tải file âm thanh gốc từ: {url}")
            ydl.download([url])
        print(f"✅ Đã tải thành công và lưu tại: {output_path}")
        return True, "Tải âm thanh thành công!"
    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Lỗi tải xuống từ yt-dlp: {e}")
        return False, f"Lỗi tải xuống: Video không khả dụng hoặc link không hợp lệ."
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
        return False, f"Lỗi không xác định: {e}"


if __name__ == '__main__':
    # Test thử module
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    test_output_folder = "downloaded_music_test"
    print(f"Bắt đầu test tải từ {test_url} vào thư mục {test_output_folder}")
    success, message = download_audio(test_url, test_output_folder)
    print(f"Kết quả test: {message}")