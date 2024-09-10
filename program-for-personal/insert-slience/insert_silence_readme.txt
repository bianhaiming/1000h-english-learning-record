
# python insert_slience.py -i "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/" -o "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/processed-audio/" -m 600 -t -45 -s 1.5



### 迭代代码思路

为了实现文件夹和文件的映射，以及在启动时避免重复处理已处理的文件，我们可以采取以下步骤：

1. **存储处理记录**：使用一个文件（如 JSON 文件）来记录已经处理过的文件夹及其对应的文件。如果文件夹中的文件已经处理过，则不再重新处理。
   
2. **记录输出文件**：在处理完一个文件后，将生成的输出文件路径也记录在同一个存储文件中，这样可以追踪哪些文件已经生成了输出。

3. **检查文件状态**：每次启动程序时，首先加载之前保存的处理记录，检查是否存在文件被删除的情况。如果有文件被删除，则重新处理这些文件。

4. **处理逻辑更新**：在处理文件时，首先判断文件是否已经处理过。如果已经处理过且输出文件存在，则跳过处理。如果文件已经处理过但输出文件不存在，则重新处理。

### 完整代码

```python
import os
import re
import json
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence

# 存储处理记录的文件路径
record_file = "processed_files_record.json"

def load_processed_files():
    """加载已处理文件的记录"""
    if os.path.exists(record_file):
        with open(record_file, 'r') as file:
            return json.load(file)
    return {}

def save_processed_files(processed_files):
    """保存已处理文件的记录"""
    with open(record_file, 'w') as file:
        json.dump(processed_files, file, indent=4)

def process_audio(input_file, output_file, min_silence_len=500, silence_thresh=-48, silence_multiplier=2.0):
    """处理音频文件并插入静音"""
    audio = AudioSegment.from_file(input_file)
    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    output_audio = AudioSegment.empty()
    
    for chunk in chunks:
        silence_duration = int(len(chunk) * silence_multiplier)
        silence = AudioSegment.silent(duration=silence_duration)
        output_audio += chunk + silence
    
    output_audio.export(output_file, format="mp3")
    print(f"Processed audio has been saved to {output_file}")

def check_and_process_files(input_dir, output_dir, min_silence_len=500, silence_thresh=-48, silence_multiplier=2.0):
    """检查文件夹并处理符合条件的音频文件"""
    # 加载已处理文件记录
    processed_files = load_processed_files()
    
    for folder in os.listdir(input_dir):
        if re.match(r"\d{8}", folder):
            folder_path = os.path.join(input_dir, folder)
            
            if os.path.isdir(folder_path):
                # 记录该文件夹是否处理过
                if folder not in processed_files:
                    processed_files[folder] = {}
                
                for file in os.listdir(folder_path):
                    if re.search(r"Discourse.*\d{8}.*\.mp3$", file):
                        input_file = os.path.join(folder_path, file)
                        file_name, file_ext = os.path.splitext(file)
                        output_file = os.path.join(output_dir, f"{file_name}-s{silence_multiplier}{file_ext}")

                        # 如果文件已处理且输出文件存在，跳过
                        if file in processed_files[folder] and os.path.exists(output_file):
                            print(f"Skipping already processed file: {file}")
                            continue
                        
                        # 处理音频文件
                        process_audio(input_file, output_file, min_silence_len, silence_thresh, silence_multiplier)
                        
                        # 更新处理记录
                        processed_files[folder][file] = output_file
    
    # 保存处理记录
    save_processed_files(processed_files)

def main():
    # 设置输入路径和输出路径
    input_dir = "/Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/"
    output_dir = "/Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/processed-audio/"
    
    # 自定义处理参数
    min_silence_len = 500  # 最小静音长度 (ms)
    silence_thresh = -48  # 静音阈值 (dB)
    silence_multiplier = 1.2  # 静音时长倍数
    
    # 检查并处理文件
    check_and_process_files(input_dir, output_dir, min_silence_len, silence_thresh, silence_multiplier)

if __name__ == "__main__":
    main()
```

### 代码说明

1. **加载和保存处理记录**：
   - `load_processed_files()` 函数用于加载之前处理过的文件记录，如果记录文件不存在，则返回空字典。
   - `save_processed_files()` 函数用于将更新后的处理记录保存到文件中，使用 JSON 格式存储。

2. **处理音频**：
   - `process_audio()` 函数负责加载音频、分割音频段并在每个段后插入静音，最终导出处理后的音频文件。

3. **检查并处理文件**：
   - `check_and_process_files()` 函数遍历输入目录中的日期文件夹，检查是否有符合条件的 `.mp3` 文件。
   - 在处理前，函数会先查看该文件是否已经处理过，并检查对应的输出文件是否存在。如果文件已经处理过且输出文件存在，则跳过该文件；如果输出文件不存在，则重新处理文件。

4. **保存处理结果**：
   - 在每次处理完文件后，程序会更新处理记录，将文件名和对应的输出文件路径保存到 `processed_files` 字典中，并在最后保存到 `processed_files_record.json` 文件中。

### 总结

通过这次迭代，代码实现了以下功能：
1. 避免重复处理已处理的文件，节省了处理时间和资源。
2. 在文件丢失的情况下能够自动重新处理，保证处理结果的完整性。