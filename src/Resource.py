import glob
import os
from pymediainfo import MediaInfo
from datetime import date

from config import conf

today = date.today()

class resource:
    def __init__(self) -> None:
        self.srt_file_path_ = None
        self.sub_file_path = None
        self.folder = conf['folder'] # 文件夹名称
        audio_files = glob.glob (os.path.join (self.folder, "*.flac")) + \
                      glob.glob (os.path.join (self.folder, "*.wav")) + \
                      glob.glob (os.path.join (self.folder, "*.mp3")) # 获取所有音频文件路径
        image_files = glob.glob (os.path.join (self.folder, "*.png")) + \
                      glob.glob (os.path.join (self.folder, "*.jpg")) + \
                      glob.glob (os.path.join (self.folder, "*.jpeg")) # 获取所有图片文件路径
        lrc_files = glob.glob (os.path.join (self.folder, "*.lrc")) # 获取所有歌词文件路径
        assert any(audio_files), "No audio files found 没有找到音频文件."
        assert any(image_files), "No image files found 没有找到图片文件."
        assert any(lrc_files), "No lrc files found 没有找到歌词文件."
        self.audio_file_path = audio_files[0]
        self.image_file_path = image_files[0]
        self.lrc_file_path = lrc_files[0]
        media_info = MediaInfo.parse(audio_files[0])
        self.duration = round(int(media_info.tracks[0].duration / 1000))
        self.pic_savepath = f"{conf['save_path']}/{today.year}-{today.month}-{today.day}.png"
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
        self.font_mian_srt = conf['Lrc2Srt']['main_font']
        self.font_sub_srt = conf['Lrc2Srt']['sub_font']
        if self.font_mian_srt == 'cn':
            self.font_mian_srt = conf['Lrc2Srt']['cn_font']
        elif self.font_mian_srt == 'en':
            self.font_mian_srt = conf['Lrc2Srt']['en_font']
        elif self.font_mian_srt == 'jp':
            self.font_mian_srt = conf['Lrc2Srt']['jp_font']
        else:
            self.font_mian_srt = conf['Lrc2Srt']['ot_font']
        if self.font_sub_srt == 'cn':
            self.font_sub_srt = conf['Lrc2Srt']['cn_font']
        elif self.font_sub_srt == 'en':
            self.font_sub_srt = conf['Lrc2Srt']['en_font']
        elif self.font_sub_srt == 'jp':
            self.font_sub_srt = conf['Lrc2Srt']['jp_font']
        else:
            self.font_sub_srt = conf['Lrc2Srt']['ot_font']

    def srt_file_path(self):
        self.srt_file_path_ = glob.glob (os.path.join (self.folder, "main.srt"))
        self.sub_file_path = glob.glob (os.path.join (self.folder, "sub.srt"))
        self.srt_file_path_ = self.srt_file_path_[0]
        if any(self.sub_file_path):
            self.sub_file_path = self.sub_file_path[0]
            return True
        else:
            return False



if __name__ == '__main__':
    resource = resource()