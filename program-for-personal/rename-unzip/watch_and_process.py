import os
import time
import shutil
import zipfile
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 自定义路径
source_dir = "/Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record"     # 监控的文件夹路径
destination_dir = "/Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record"  # 解压后的文件夹路径
custom_prefix = "xiaolai"                      # 自定义前缀

# 从压缩包中获取文件的最早日期
def get_file_date_from_zip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 获取压缩包内所有文件的信息
        file_info_list = zip_ref.infolist()
        # 获取最早的文件的日期时间
        file_dates = [datetime(*info.date_time) for info in file_info_list]
        # 返回最早的日期
        if file_dates:
            return min(file_dates).strftime('%Y%m%d')
        else:
            return None

# 文件处理函数
def process_compressed_file(file_path):
    if file_path.endswith(".zip"):
        # 获取压缩包内文件的日期
        file_date = get_file_date_from_zip(file_path)

        if file_date is None:
            print(f"未能提取文件日期，跳过文件: {file_path}")
            return

        # 构建新的文件夹名
        base_name = os.path.basename(file_path)
        new_folder_name = f"{custom_prefix}_{file_date}"
        extracted_folder = os.path.join(destination_dir, new_folder_name)

        # 创建解压文件夹
        os.makedirs(extracted_folder, exist_ok=True)

        # 解压文件
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)
        print(f"文件解压至: {extracted_folder}")

# 处理已存在的文件
def process_existing_files():
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".zip"):
            print(f"处理已存在文件: {file_path}")
            process_compressed_file(file_path)

# 事件处理类
class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"检测到新文件: {event.src_path}")
            process_compressed_file(event.src_path)

# 设置监控
observer = Observer()
event_handler = WatcherHandler()
observer.schedule(event_handler, path=source_dir, recursive=False)

# 在开始监控之前，先处理已存在的压缩文件
process_existing_files()

observer.start()

try:
    print(f"监控目录: {source_dir}")
    while True:
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
