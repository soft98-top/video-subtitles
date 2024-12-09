import os
import whisper
import warnings
import argparse

# 忽略 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# 加载 Whisper 模型
model = whisper.load_model("base")  # 也可尝试 "small" 或 "large"
def generate_subtitles_by_dir(video_folder):
    # 遍历文件夹中的所有视频文件
    for file in os.listdir(video_folder):
        video_path = os.path.join(video_folder, file)
        generate_subtitles_by_file(video_path)

def generate_subtitles_by_file(video_path):
    video_folder = os.path.dirname(video_path)
    file = os.path.basename(video_path)
    if os.path.isdir(video_path):
        generate_subtitles_by_dir(video_path)
    elif file.endswith(('.mp4', '.mkv', '.avi')):  # 检查视频格式
        output_path = os.path.join(video_folder, file.rsplit('.', 1)[0] + ".srt")
        print(f"正在处理 {file} ...")
        result = model.transcribe(video_path)
        # 保存字幕到文件
        save_as_srt(result, output_path)
        print(f"字幕已保存到 {output_path}")

def save_as_srt(transcription, output_file):
    """
    将 Whisper 的转录结果保存为 SRT 字幕文件
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(transcription["segments"]):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"]

            # 写入 SRT 格式
            f.write(f"{idx + 1}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text.strip()}\n\n")

def format_timestamp(seconds):
    """
    格式化时间戳为 SRT 格式 (hh:mm:ss,ms)
    """
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

if __name__ == "__main__":
    # 解析启动命令
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default=None)
    parser.add_argument('--file', type=str, default=None)
    args = parser.parse_args()
    if args.dir:
        generate_subtitles_by_dir(args.dir)
    elif args.file:
        generate_subtitles_by_file(args.file)
    else:
        print("please input dir or file.")