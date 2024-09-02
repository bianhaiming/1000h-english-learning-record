import os
import re
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence

def process_audio(input_file, output_file, min_silence_len=500, silence_thresh=-48, silence_multiplier=2.0):
    # 加载音频
    audio = AudioSegment.from_file(input_file)

    # 分割音频
    chunks = split_on_silence(
        audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # 创建一个新的空音频段
    output_audio = AudioSegment.empty()

    # 遍历每个块，然后在每个块后添加根据倍数计算的静音
    for chunk in chunks:
        silence_duration = int(len(chunk) * silence_multiplier)
        silence = AudioSegment.silent(duration=silence_duration)
        output_audio += chunk + silence

    # 导出修改后的音频
    output_audio.export(output_file, format="mp3")
    print(f"Processed audio has been saved to {output_file}")

def check_and_process_files(input_dir, output_dir, min_silence_len=500, silence_thresh=-48, silence_multiplier=2.0):
    # 获取当前日期
    today_date = datetime.now().strftime("%Y%m%d")

    # 查找符合日期格式的文件夹
    for folder in os.listdir(input_dir):
        if re.match(r"\d{8}", folder):
            folder_path = os.path.join(input_dir, folder)

            if os.path.isdir(folder_path):
                # 查找符合条件的文件
                for file in os.listdir(folder_path):
                    if re.search(r"Discourse.*\d{8}.*\.mp3$", file):
                        input_file = os.path.join(folder_path, file)
                        file_name, file_ext = os.path.splitext(file)
                        output_file = os.path.join(output_dir, f"{file_name}-s{silence_multiplier}{file_ext}")
                        
                        # 处理音频文件
                        process_audio(input_file, output_file, min_silence_len, silence_thresh, silence_multiplier)

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
