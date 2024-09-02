import os
import time
import pypandoc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# 自定义路径
source_directory = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/"
output_directory = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/md-2-doc-epub/docx-and-epub/"

# 自定义关键字，可以根据需求增加
keywords = ['Discourse', 'Lesson', 'Topic', 'Note', 'Summary']

# 已处理文件列表，避免重复处理
processed_files = set()

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".md"):
            self.convert_file(event.src_path)

    def convert_file(self, file_path):
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # 检查文件名是否包含关键字
        if not any(keyword in file_name for keyword in keywords):
            return
        
        # 检查文件是否已处理
        if file_path in processed_files:
            return

        try:
            # 尝试从文件名中提取日期部分
            parts = file_name.split('_')
            if len(parts) > 2 and len(parts[-2]) == 8:
                date_part = parts[-2][4:]  # 提取日期的月日部分，例如 "0822"
                main_part = '_'.join(parts[1:-2])  # 提取文件的主体部分
            else:
                # 如果文件名没有日期，使用文件的创建日期
                creation_time = os.path.getctime(file_path)
                date_part = datetime.fromtimestamp(creation_time).strftime('%m%d')
                main_part = '_'.join(parts[1:])

            prefix = parts[0].lower()  # 将前缀 "Discourse" 变为小写

            # 自定义文件名格式
            custom_file_name = f"{date_part}_{main_part}_{prefix}"

            # 转换为 .epub 格式
            epub_output = os.path.join(output_directory, f"{custom_file_name}.epub")
            pypandoc.convert_file(file_path, 'epub', outputfile=epub_output)
            print(f"Converted {file_path} to {epub_output}")

            # 转换为 .docx 格式
            docx_output = os.path.join(output_directory, f"{custom_file_name}.docx")
            pypandoc.convert_file(file_path, 'docx', outputfile=docx_output)
            print(f"Converted {file_path} to {docx_output}")

            # 记录已处理文件
            processed_files.add(file_path)

        except Exception as e:
            print(f"Error converting {file_path}: {e}")

def scan_directory():
    for dirpath, _, filenames in os.walk(source_directory):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                handler.convert_file(file_path)

if __name__ == "__main__":
    handler = FileHandler()

    # 初始扫描
    scan_directory()

    # 实时监测
    observer = Observer()
    observer.schedule(handler, path=source_directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
