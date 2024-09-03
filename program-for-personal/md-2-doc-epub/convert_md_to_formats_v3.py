import os
import time
import pypandoc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

source_directory = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/"
output_directory = "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/docx-and-epub/"

processed_files = set()

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".md"):
            self.convert_file(event.src_path)

    def convert_file(self, file_path):
        if file_path in processed_files:
            return

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        parts = file_name.split('_')
        if len(parts) > 2 and len(parts[-2]) == 8:
            date_part = parts[-2][4:]
            main_part = '_'.join(parts[1:-2]).strip('_')
        else:
            creation_time = os.path.getctime(file_path)
            date_part = datetime.fromtimestamp(creation_time).strftime('%m%d')
            main_part = '_'.join(parts[1:]).strip('_')

        prefix = parts[0].lower().strip('_')

        custom_file_name = f"{date_part}_{main_part}_{prefix}" if main_part else f"{date_part}_{prefix}"

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            title_with_newline = f"\n{custom_file_name}\n\n{content}"

            with open(file_path, 'w') as f:
                f.write(title_with_newline)

            epub_output = os.path.join(output_directory, f"{custom_file_name}.epub")
            pypandoc.convert_file(file_path, 'epub', outputfile=epub_output)
            print(f"Converted {file_path} to {epub_output}")

            docx_output = os.path.join(output_directory, f"{custom_file_name}.docx")
            pypandoc.convert_file(file_path, 'docx', outputfile=docx_output)
            print(f"Converted {file_path} to {docx_output}")

            processed_files.add(file_path)

        except Exception as e:
            print(f"Error converting {file_path}: {e}")

def scan_directory():
    for dirpath, _, filenames in os.walk(source_directory):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                handler.convert_file(file_path)

def main():
    global handler
    handler = FileHandler()

    # Initial scan of existing .md files in the directory
    scan_directory()

    # Start observing the directory for new .md files
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