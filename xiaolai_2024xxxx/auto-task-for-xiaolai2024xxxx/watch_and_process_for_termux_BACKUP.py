import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

# Import the scripts
from program_for_personal.watch_and_process_for_termux import process_compressed_file
from program_for_personal.convert_md_to_formats_v1_3 import convert_file
from program_for_personal.reformat_docx_v3 import reformat_docx

# Define the main paths
source_dir = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record"
xiaolai_dir = os.path.join(source_dir, "xiaolai_2024xxxx")
docx_epub_dir = os.path.join(xiaolai_dir, "docx-and-epub")
reformatted_dir = os.path.join(xiaolai_dir, "reformatted-docx")

# Ensure directories exist
os.makedirs(xiaolai_dir, exist_ok=True)
os.makedirs(docx_epub_dir, exist_ok=True)
os.makedirs(reformatted_dir, exist_ok=True)

# Watchdog Event Handler for monitoring file changes
class MainHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == ".zip":
                print(f"New ZIP file detected: {file_path}")
                process_compressed_file(file_path)
            
            elif file_ext == ".md":
                print(f"New Markdown file detected: {file_path}")
                convert_file(file_path, docx_epub_dir)
            
            elif file_ext == ".docx" and not file_path.endswith("_reformat.docx"):
                print(f"New DOCX file detected: {file_path}")
                reformat_docx(file_path, reformatted_dir)

# Function to scan and process existing files
def process_existing_files():
    for root, dirs, files in os.walk(source_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            if file_ext == ".zip":
                print(f"Processing existing ZIP file: {file_path}")
                process_compressed_file(file_path)
            
            elif file_ext == ".md":
                print(f"Processing existing Markdown file: {file_path}")
                convert_file(file_path, docx_epub_dir)
            
            elif file_ext == ".docx" and not file_name.endswith("_reformat.docx"):
                print(f"Processing existing DOCX file: {file_path}")
                reformat_docx(file_path, reformatted_dir)

# Start monitoring
def main():
    # Process existing files
    process_existing_files()
    
    # Set up watchdog observer
    observer = Observer()
    event_handler = MainHandler()
    observer.schedule(event_handler, path=source_dir, recursive=True)
    
    # Start observing
    observer.start()
    print(f"Monitoring directory: {source_dir}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()
