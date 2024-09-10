import os
import re
import json
import argparse
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

    # 遍历输入目录中的子文件夹
    for folder in os.listdir(input_dir):
        # 检查子文件夹名是否符合 'xiaolai_YYYYMMDD' 格式
        if re.match(r"xiaolai_\d{8}", folder):
            folder_path = os.path.join(input_dir, folder)

            if os.path.isdir(folder_path):
                # 记录该文件夹是否处理过
                if folder not in processed_files:
                    processed_files[folder] = {}

                for file in os.listdir(folder_path):
                    # 检查文件名是否符合条件
                    if re.search(r"Discourse.*\d{8}.*\.mp3$", file):
                        input_file = os.path.join(folder_path, file)
                        file_name, file_ext = os.path.splitext(file)
                        output_file = os.path.join(output_dir, f"{file_name}-s{silence_multiplier}{file_ext}")

                        # 如果文件已处理且输出文件存在，跳过
                        if file in processed_files[folder] and os.path.exists(processed_files[folder][file]):
                            print(f"Skipping already processed file: {file}")
                            continue
                        
                        # 处理音频文件
                        process_audio(input_file, output_file, min_silence_len, silence_thresh, silence_multiplier)
                        
                        # 更新处理记录
                        processed_files[folder][file] = output_file
    
    # 保存处理记录
    save_processed_files(processed_files)

def main():
    """主函数，处理命令行参数并执行处理任务"""
    parser = argparse.ArgumentParser(description="Process audio files with silence insertion.")
    
    parser.add_argument('-i', '--input-dir', required=True, help="Directory containing the input folders.")
    parser.add_argument('-o', '--output-dir', required=True, help="Directory to save the processed audio files.")
    parser.add_argument('-m', '--min-silence-len', type=int, default=500, help="Minimum length of silence to detect (in ms).")
    parser.add_argument('-t', '--silence-thresh', type=int, default=-48, help="Silence threshold (in dB).")
    parser.add_argument('-s', '--silence-multiplier', type=float, default=2.0, help="Multiplier for silence duration.")

    args = parser.parse_args()

    check_and_process_files(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        min_silence_len=args.min_silence_len,
        silence_thresh=args.silence_thresh,
        silence_multiplier=args.silence_multiplier
    )

if __name__ == "__main__":
    main()
    
    
    #  python /data/data/com.termux/files/home/1000h-english-learning-record/program-for-personal/insert_slience.py -i "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/" -o "/data/data/com.termux/files/home/EnjoyLibrary/1000h-english-learning-record/xiaolai_2024xxxx/processed-audio/" -m 600 -t -45 -s 1.5
    
    
    