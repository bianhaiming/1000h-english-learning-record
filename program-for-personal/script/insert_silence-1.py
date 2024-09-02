import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence


def process_audio(input_file, output_file, min_silence_len=1000, silence_thresh=-40):
    # 加载音频
    audio = AudioSegment.from_file(input_file)

    # 分割音频
    chunks = split_on_silence(
        audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # 创建一个新的空音频段
    output_audio = AudioSegment.empty()

    # 遍历每个块，然后在每个块后添加等长的静音
    for chunk in chunks:
        silence = AudioSegment.silent(duration=len(chunk))
        output_audio += chunk + silence

    # 导出修改后的音频
    output_audio.export(output_file, format="mp3")
    print(f"Processed audio has been saved to {output_file}")


if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(
        description="Process an audio file to insert silence after each sentence.")
    parser.add_argument("input_file", type=str, help="Input audio file path")
    parser.add_argument("output_file", type=str, help="Output audio file path")
    parser.add_argument("--min_silence_len", type=int, default=1000,
                        help="Minimum length of a silence to be used for splitting (in ms)")
    parser.add_argument("--silence_thresh", type=int,
                        default=-40, help="Silence threshold (dB)")

    # 解析命令行参数
    args = parser.parse_args()

    # 处理音频
    process_audio(args.input_file, args.output_file,
                  args.min_silence_len, args.silence_thresh)
