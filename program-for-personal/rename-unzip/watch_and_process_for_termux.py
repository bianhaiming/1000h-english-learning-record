def main():
    # Existing code here

import os
import time
import shutil
import zipfile
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Custom paths
source_dir = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record"
destination_dir = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx"
custom_prefix = "xiaolai"

def get_file_date_from_zip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_info_list = zip_ref.infolist()
        file_dates = [datetime(*info.date_time) for info in file_info_list]
        if file_dates:
            return min(file_dates).strftime('%Y%m%d')
        else:
            return None

def process_compressed_file(file_path):
    if file_path.endswith(".zip"):
        file_date = get_file_date_from_zip(file_path)

        if file_date is None:
            print(f"Failed to extract date, skipping: {file_path}")
            return

        new_folder_name = f"{custom_prefix}_{file_date}"
        extracted_folder = os.path.join(destination_dir, new_folder_name)

        os.makedirs(extracted_folder, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)
        print(f"Extracted to: {extracted_folder}")

        os.remove(file_path)
        print(f"Deleted zip file: {file_path}")

def process_existing_files():
    for root, dirs, files in os.walk(source_dir):
        for file_name in files:
            if file_name.endswith(".zip"):
                file_path = os.path.join(root, file_name)
                print(f"Processing existing file: {file_path}")
                process_compressed_file(file_path)

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            process_compressed_file(event.src_path)

observer = Observer()
event_handler = WatcherHandler()
observer.schedule(event_handler, path=source_dir, recursive=True)

process_existing_files()

observer.start()

try:
    print(f"Monitoring directory: {source_dir}")
    while True:
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()


if __name__ == "__main__":
    main()
