import os
import zipfile
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Custom paths
source_dir = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record"
destination_dir = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx"
custom_prefix = "xiaolai"

# To keep track of already processed files and their corresponding folder names
extracted_files_map = {}

def load_extracted_files():
    """Load extracted files mapping from a stored file, if it exists."""
    global extracted_files_map
    mapping_file = os.path.join(destination_dir, "extracted_files_map.txt")
    
    if os.path.exists(mapping_file):
        with open(mapping_file, "r") as f:
            for line in f:
                zip_name, folder_name = line.strip().split(" -> ")
                extracted_files_map[zip_name] = folder_name

def save_extracted_file(zip_name, folder_name):
    """Save the extracted file mapping to a file."""
    mapping_file = os.path.join(destination_dir, "extracted_files_map.txt")
    
    with open(mapping_file, "a") as f:
        f.write(f"{zip_name} -> {folder_name}\n")

def get_file_date_from_zip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_info_list = zip_ref.infolist()
        file_dates = [datetime(*info.date_time) for info in file_info_list]
        if file_dates:
            return min(file_dates).strftime('%Y%m%d')
        else:
            return None

def is_similar_to_existing_file(file_name):
    """Check if a given file name is similar to any already extracted file."""
    base_name = file_name.rsplit("(", 1)[0].split("副本")[0].strip()
    
    for extracted_file in extracted_files_map.keys():
        if extracted_file.startswith(base_name):
            return True
    
    return False

def process_compressed_file(file_path):
    file_name = os.path.basename(file_path)
    
    # Check if the file or a similar one has already been extracted
    if file_name in extracted_files_map or is_similar_to_existing_file(file_name):
        print(f"File {file_name} (or a similar one) has already been processed. Skipping.")
        return
    
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

        # Save the mapping of the compressed file and its corresponding folder
        extracted_files_map[file_name] = new_folder_name
        save_extracted_file(file_name, new_folder_name)

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

def main():
    # Load previously extracted files
    load_extracted_files()

    observer = Observer()
    event_handler = WatcherHandler()
    observer.schedule(event_handler, path=source_dir, recursive=True)

    # Process any existing files in the directory
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