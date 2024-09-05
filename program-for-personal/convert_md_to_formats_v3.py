import os
import time
import json
import pypandoc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

source_directory = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/"
output_directory = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/docx-and-epub/"
record_file = "processed_files.json"

# 加载处理记录
def load_processed_files():
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            return json.load(f)
    return {"files": [], "folders": []}

# 保存处理记录
def save_processed_files(processed_files):
    with open(record_file, 'w') as f:
        json.dump(processed_files, f)

processed_files = load_processed_files()

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".md"):
            self.convert_file(event.src_path)

    def convert_file(self, file_path):
        file_name = os.path.basename(file_path)

        # 检查文件是否已处理
        if file_name in processed_files["files"]:
            print(f"{file_name} 已处理，跳过...")
            return

        try:
            # 文件转换逻辑
            file_name_without_ext = os.path.splitext(file_name)[0]
            parts = file_name_without_ext.split('_')

            # 获取日期部分和主部分
            if len(parts) > 2 and len(parts[-2]) == 8:
                date_part = parts[-2][4:]
                main_part = '_'.join(parts[1:-2]).strip('_')
            else:
                creation_time = os.path.getctime(file_path)
                date_part = datetime.fromtimestamp(creation_time).strftime('%m%d')
                main_part = '_'.join(parts[1:]).strip('_')

            prefix = parts[0].lower().strip('_')

            custom_file_name = f"{date_part}_{main_part}_{prefix}" if main_part else f"{date_part}_{prefix}"

            # 插入标题并转换文件
            with open(file_path, 'r') as f:
                content = f.read()

            title_with_newline = f"\n{custom_file_name}\n\n{content}"

            with open(file_path, 'w') as f:
                f.write(title_with_newline)

            # 生成目标文件路径
            epub_output = os.path.join(output_directory, f"{custom_file_name}.epub")
            docx_output = os.path.join(output_directory, f"{custom_file_name}.docx")

            # 执行转换
            pypandoc.convert_file(file_path, 'epub', outputfile=epub_output)
            print(f"Converted {file_path} to {epub_output}")

            pypandoc.convert_file(file_path, 'docx', outputfile=docx_output)
            print(f"Converted {file_path} to {docx_output}")

            # 记录已处理文件
            processed_files["files"].append(file_name)
            save_processed_files(processed_files)

        except Exception as e:
            print(f"Error converting {file_path}: {e}")

def scan_directory():
    for dirpath, _, filenames in os.walk(source_directory):
        folder_name = os.path.basename(dirpath)

        # 检查文件夹是否已处理
        if folder_name in processed_files["folders"]:
            print(f"{folder_name} 已处理，跳过...")
            continue

        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                handler.convert_file(file_path)

        # 记录已处理文件夹
        processed_files["folders"].append(folder_name)
        save_processed_files(processed_files)

def main():
    global handler
    handler = FileHandler()

    # 初始扫描目录
    scan_directory()

    # 监听文件夹变化
    observer = Observer()
    observer.schedule(handler, path=source_directory, recursive=True)
    observer.start()

    try:
        print(f"Monitoring directory: {source_directory}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()