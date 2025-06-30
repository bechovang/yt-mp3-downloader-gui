# Tên tệp: downloader.py

import yt_dlp
import os

def download_media(url: str, output_path: str, download_type: str = "audio"):
    """
    Tải media (âm thanh hoặc video) từ YouTube.

    Args:
        url (str): Link YouTube.
        output_path (str): Thư mục lưu file.
        download_type (str): Loại tải xuống, "audio" hoặc "video".

    Returns:
        tuple: (True, filename) nếu thành công, (False, error_message) nếu thất bại.
    """
    os.makedirs(output_path, exist_ok=True)

    if download_type == "video":
        print("INFO: Cấu hình tải video 1080p MP4. Yêu cầu có FFmpeg.")
        # Tùy chọn để tải video 1080p và ghép với audio, lưu dưới dạng MP4
        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,  # Không in log của yt-dlp ra console để tránh làm rối
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
        }
    else:  # Mặc định là audio
        print("INFO: Cấu hình tải âm thanh (chất lượng cao nhất).")
        # Tùy chọn để tải audio chất lượng tốt nhất
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'noplaylist': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Tải thông tin và file
            info_dict = ydl.extract_info(url, download=True)
            # Lấy tên file đã được tạo
            filename = ydl.prepare_filename(info_dict)
            base_filename = os.path.basename(filename)
            print(f"✅ Tải thành công: {base_filename}")
            return True, base_filename
    except yt_dlp.utils.DownloadError as e:
        # Lọc ra thông báo lỗi gọn gàng hơn
        error_message = str(e).split(';')[-1].strip()
        print(f"❌ Lỗi tải xuống: {error_message}")
        return False, f"Lỗi tải: {error_message}"
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
        return False, f"Lỗi không xác định: {str(e)}"