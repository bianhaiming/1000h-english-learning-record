import argparse
import os
import re
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence

def process_audio(input_file, output_file, min_silence_len=1000, silence_thresh=-40, silence_multiplier=1.0):
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

def find_and_process_files(directory, output_dir, min_silence_len=1000, silence_thresh=-40, silence_multiplier=1.0):
    # 获取当前日期
    today_str = datetime.now().strftime('%Y%m%d')
    
    # 遍历目录中的文件夹
    for root, dirs, files in os.walk(directory):
        # 检查文件夹名是否包含当前日期
        if re.search(today_str, root):
            for file in files:
                # 检查文件名是否包含关键词 'Discourse' 和 'mp3' 文件
                if re.search(r'Discourse.*\.mp3$', file):
                    input_file = os.path.join(root, file)
                    
                    # 生成新的文件名，添加 "-sX" 后缀，其中 X 是静音倍数
                    new_file_name = file.replace(".mp3", f"-s{silence_multiplier}.mp3")
                    
                    # 将文件保存到指定的输出目录
                    output_file = os.path.join(output_dir, new_file_name)
                    
                    # 处理音频文件
                    process_audio(input_file, output_file, min_silence_len, silence_thresh, silence_multiplier)

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(
        description="Process audio files in the specified directory.")
    parser.add_argument("directory", type=str, help="Directory to search for audio files")
    parser.add_argument("output_dir", type=str, help="Directory to save processed audio files")
    parser.add_argument("--min_silence_len", type=int, default=1000,
                        help="Minimum length of a silence to be used for splitting (in ms)")
    parser.add_argument("--silence_thresh", type=int,
                        default=-40, help="Silence threshold (dB)")
    parser.add_argument("--silence_multiplier", type=float, default=1.0,
                        help="Multiplier for silence duration relative to the audio chunk length")

    # 解析命令行参数
    args = parser.parse_args()

    # 查找并处理文件
    find_and_process_files(args.directory, args.output_dir, args.min_silence_len, args.silence_thresh, args.silence_multiplier)

