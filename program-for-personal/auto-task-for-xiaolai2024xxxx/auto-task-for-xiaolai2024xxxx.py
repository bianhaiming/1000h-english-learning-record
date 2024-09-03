import os
import sys
import time
import shutil
import zipfile
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Adding the program-for-personal directory to the sys.path to import custom modules
sys.path.append("/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/program-for-personal")

# Importing the three custom scripts as modules
import watch_and_process_for_termux
import convert_md_to_formats_v3
import reformat_docx_v3

def main():
    print("Starting the watch_and_process_for_termux module...")
    watch_and_process_for_termux.main()
    
    # Adding a short delay to ensure completion
    time.sleep(10)  # Adjust the delay as needed

    print("Starting the convert_md_to_formats_v1_3 module...")
    convert_md_to_formats_v3.main()
    
    # Adding a short delay to ensure completion
    time.sleep(10)  # Adjust the delay as needed

    print("Starting the reformat_docx_v3 module...")
    reformat_docx_v3.main()

if __name__ == "__main__":
    main()
