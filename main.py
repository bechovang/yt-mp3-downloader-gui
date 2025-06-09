from downloader import download_audio
import os

if __name__ == "__main__":
    print("--- YouTube Audio Downloader (CLI) ---")
    url = input("🔗 Nhập link YouTube cần tải: ").strip()
    if not url:
        print("❌ URL không được để trống.")
    else:
        default_path = os.path.join(os.getcwd(), "downloaded_audios")  # Thư mục mặc định
        path_input_prompt = f"📁 Nhập thư mục lưu file (mặc định: {default_path}): "
        path = input(path_input_prompt).strip()
        if not path:
            path = default_path

        print(f"\nBắt đầu tải từ: {url}")
        print(f"Lưu vào: {path}")
        success, message = download_audio(url, path)

        if success:
            print(f"✅ {message}")
            try:
                # Mở thư mục chứa file sau khi tải (tùy hệ điều hành)
                if os.name == 'nt':  # Windows
                    os.startfile(os.path.realpath(path))
                elif os.name == 'posix':  # macOS/Linux
                    if os.uname().sysname == 'Darwin':
                        os.system(f'open "{os.path.realpath(path)}"')
                    else:
                        os.system(f'xdg-open "{os.path.realpath(path)}"')
            except Exception as e_open:
                print(f"(Không thể tự động mở thư mục: {e_open})")
        else:
            print(f"❌ {message}")