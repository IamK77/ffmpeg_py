from PIL import Image, ImageDraw, ImageFont, ImageFilter
from config import conf
from pymediainfo import MediaInfo
import subprocess
import time
import glob
import os
from datetime import date
today = date.today()

# 字体
# 中文
# FONT_PATH = r'C:\Windows\Fonts\FZSKBXKK.TTF'
# 英文
# FONT_PATH = r'C:\Windows\Fonts\comic.ttf'
# 日文
# FONT_PATH = r'D:\Downloads\seto\setofont.ttf'
# FONT_SIZE_LARGE = 115
# FONT_SIZE_SMALL = 60

# 颜色
# RGB_BACKGROUND = (172, 176, 157)
RGB_TEXT = (255, 255, 255)

class resource:
    def __init__(self) -> None:
        folder = conf['folder'] # 文件夹名称
        audio_files = glob.glob (os.path.join (folder, "*.flac")) + \
                      glob.glob (os.path.join (folder, "*.mp3")) # 获取所有音频文件路径
        image_files = glob.glob (os.path.join (folder, "*.png")) + \
                      glob.glob (os.path.join (folder, "*.jpg")) + \
                      glob.glob (os.path.join (folder, "*.jpeg")) # 获取所有图片文件路径
        assert any(audio_files), "No audio files found 没有找到音频文件."
        assert any(image_files), "No image files found 没有找到图片文件."
        self.audio_file_path = audio_files[0]
        self.image_file_path = image_files[0]
        media_info = MediaInfo.parse(audio_files[0])
        self.duration = round(int(media_info.tracks[0].duration / 1000))
        self.pic_savepath = f"{conf['AlbumCover']['save_path']}/{today.year}-{today.month}-{today.day}.png"
        if any(conf['AlbumCover']['artist']) or any(conf['AlbumCover']['title']) or any(conf['AlbumCover']['albumen']):
            self.artist = conf['AlbumCover']['artist']
            self.title = conf['AlbumCover']['title']
            self.album = conf['AlbumCover']['albumen']
        else:
            self.title = media_info.tracks[0].title
            self.artist = media_info.tracks[0].album_composer
            print(self.artist)
            self.album = media_info.tracks[0].album
        self.font = conf['AlbumCover']['choose_font']
        if self.font == 'cn':
            self.font = conf['AlbumCover']['cn_font']
        elif self.font == 'en':
            self.font = conf['AlbumCover']['en_font']
        elif self.font == 'jp':
            self.font = conf['AlbumCover']['jp_font']
        else:
            self.font = conf['AlbumCover']['ot_font']



class AlbumCoverGenerator:
    def __init__(self):
        self.resource = resource()
        self.img = Image.open(self.resource.image_file_path) # 将打开的图片缩放尺寸到1280*1280
        self.img = self.img.resize((1280, 1280), Image.ANTIALIAS)

    def draw_text(self, text, position, font, color, outline_color, outline_width):
        draw = ImageDraw.Draw(self.img)
        x, y = position
        # 绘制文本的阴影
        draw.text((x - 1, y - 1), text, fill=color, font=font, stroke_width=outline_width, stroke_fill=outline_color)
        draw.text((x + 1, y + 1), text, fill=color, font=font, stroke_width=outline_width, stroke_fill=outline_color)
        # 绘制文本
        draw.text(position, text, fill=color, font=font)


    def add_image_surface(self):
        background = Image.new('RGB', (700, 700), (255, 255, 255))
        self.img.paste(background, (334, 190))
        surface = Image.open(self.resource.image_file_path)
        surface = surface.resize((668, 668))
        self.img.paste(surface, (350, 206))


    def generate_album_cover(self):
        
        width, height = self.img.size

        # 计算放大比例
        if width < 1080:
            scale = 1080 / width
        else:
            scale = 1
        while width * scale < 2440 or height * scale < 1080:
            scale += 0.1

        # 缩放图片
        new_width = int(width * scale)
        new_height = int(height * scale)
        self.img = self.img.resize((new_width, new_height))

        # 裁剪图片
        left = (new_width - 2440) / 2
        top = (new_height - 1080) / 2
        right = left + 2440
        bottom = top + 1080
        self.img = self.img.crop((left, top, right, bottom))
        self.img = self.img.filter(ImageFilter.GaussianBlur(radius=42))

        # 添加你的专辑封面
        self.add_image_surface()

        # 添加文本
        font_large = ImageFont.truetype(self.resource.font, conf['AlbumCover']['FONT_SIZE_LARGE'])
        font_small = ImageFont.truetype(self.resource.font, conf['AlbumCover']['FONT_SIZE_SMALL'])
        outline_color = (0, 0, 0)
        outline_width = 3
        self.draw_text(self.resource.title, (1152, 240), font_large, RGB_TEXT, outline_color, outline_width)
        self.draw_text(self.resource.artist, (1152, 450), font_small, RGB_TEXT, outline_color, outline_width)
        self.draw_text(self.resource.album, (1152, 540), font_small, RGB_TEXT, outline_color, outline_width)

        # 保存图像
        self.img.save(self.resource.pic_savepath, "PNG")
        # 显示图像
        self.img.show()
        

class ffmpeg_use:
    def __init__(self):
        self.resource = resource()

    # 生成没有音频的视频文件
    def generate_video_without_audio(self):
        command = f'{conf["ffmpeg"]["path"]} ' \
                  f'-hwaccel cuvid ' \
                  f'-r {conf["ffmpeg"]["fps"]} ' \
                  f'-loop 1 ' \
                  f'-i {self.resource.pic_savepath} ' \
                  f'-pix_fmt {conf["ffmpeg"]["-pix_fmt"]} ' \
                  f'-vcodec {conf["ffmpeg"]["vcodec"]} ' \
                  f'-b:v {conf["ffmpeg"]["-b:v"]} ' \
                  f'-r:v {conf["ffmpeg"]["fps"]} ' \
                  f'-preset {conf["ffmpeg"]["-preset"]} ' \
                  f'-crf {conf["ffmpeg"]["crf"]} ' \
                  f'-s {conf["ffmpeg"]["frame"]} ' \
                  f'-vframes {conf["ffmpeg"]["fps"] * self.resource.duration} ' \
                  f'-r {conf["ffmpeg"]["fps"]} ' \
                  f'-t {self.resource.duration} ' \
                  f'{conf["folder"] + "temp_video_without_audio.mp4"}'
        subprocess.call(command, shell=True)

    # 将没有音频的视频文件与音频拼接
    def generate_video_with_audio(self):
        command = f'{conf["ffmpeg"]["path"]} ' \
                  f'-i {conf["folder"]}temp_video_without_audio.mp4 ' \
                  f'-i "{self.resource.audio_file_path}" ' \
                  f'-c:v copy ' \
                  f'-c:a copy ' \
                  f'-strict experimental ' \
                  f'{conf["folder"] + "temp_video_without_font.mp4"}'
        subprocess.call(command, shell=True)

        # 删除临时生成的没有音频的视频文件
        if not conf['keep_temp']:
            subprocess.call(f'del {conf["folder"]}temp_video_without_audio.mp4', shell=True)

    # 添加字幕
    def add_subtitle(self):
        final_video_name = conf["ffmpeg"]["final_video_name"] if any(conf["ffmpeg"]["final_video_name"]) \
            else f"{today.year}-{today.month}-{today.day}.mp4"
        command = f'{conf["ffmpeg"]["path"]} ' \
                  f'-i "{conf["folder"]}temp_video_without_font.mp4" ' \
                  f'-vf subtitles={conf["ffmpeg"]["subtitle_path"]} ' \
                  f'-y "{final_video_name}"'
        subprocess.call(command, shell=True)

        if not conf['keep_temp']:
            subprocess.call(f'del {conf["folder"]}temp_video_without_font.mp4', shell=True)


if __name__ == "__main__":
    generator = AlbumCoverGenerator()
    generator.generate_album_cover()
    ffmpeg = ffmpeg_use()
    ffmpeg.generate_video_without_audio()
    time.sleep(1)
    # ffmpeg.generate_video_with_audio()
    time.sleep(1)
    # ffmpeg.add_subtitle()
