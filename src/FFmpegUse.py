import subprocess
from datetime import date

from src.Resource import resource, conf

today = date.today()

class ffmpeg_use:
    def __init__(self):
        self.resource_ = resource()

    # 生成没有音频的视频文件
    def generate_video_without_audio(self):
        command = f'{conf["ffmpeg"]["path"]} ' \
                  f'-hwaccel cuvid ' \
                  f'-r {conf["ffmpeg"]["fps"]} ' \
                  f'-loop 1 ' \
                  f'-i {self.resource_.pic_savepath} ' \
                  f'-pix_fmt {conf["ffmpeg"]["-pix_fmt"]} ' \
                  f'-vcodec {conf["ffmpeg"]["vcodec"]} ' \
                  f'-b:v {conf["ffmpeg"]["-b:v"]} ' \
                  f'-r:v {conf["ffmpeg"]["fps"]} ' \
                  f'-preset {conf["ffmpeg"]["-preset"]} ' \
                  f'-crf {conf["ffmpeg"]["crf"]} ' \
                  f'-s {conf["ffmpeg"]["frame"]} ' \
                  f'-vframes {conf["ffmpeg"]["fps"] * self.resource_.duration} ' \
                  f'-r {conf["ffmpeg"]["fps"]} ' \
                  f'-t {self.resource_.duration} ' \
                  f'{conf["save_path"] + "temp_video_without_audio.mp4"}'
        subprocess.call(command, shell=True)

    # 将没有音频的视频文件与音频拼接
    def generate_video_with_audio(self):
        command = f'{conf["ffmpeg"]["path"]} ' \
                  f'-i {conf["save_path"]}temp_video_without_audio.mp4 ' \
                  f'-i "{self.resource_.audio_file_path}" ' \
                  f'-c:v copy ' \
                  f'-c:a copy ' \
                  f'-strict experimental ' \
                  f'{conf["save_path"] + "temp_video_without_font.mp4"}'
        print(command)
        subprocess.call(command, shell=True)

        # 删除临时生成的没有音频的视频文件
        if not conf['keep_temp']:
            path = conf["save_path"].replace("/", "\\") + "temp_video_without_audio.mp4"
            subprocess.call(f'del {path}', shell=True)

    # 添加字幕
    def add_subtitle(self):
        """
        ffmpeg -i VIDEO.mp4 -vf "subtitles=main.srt:force_style='Alignment=9,Fontsize=24,Fontname=Arial,PrimaryColour=&H0000ff&'" -c:a copy output.mp4
        {conf["ffmpeg"]["path"]} -i "{conf["save_path"]}temp_video_without_font.mp4" -lavfi "subtitles={self.resource_.srt_file_path_}:force_style='Alignment=2,OutlineColour=&HFFFFFF00,BorderStyle=3,Outline=1,Shadow=0,Fontsize=18,MarginL=5,MarginV=20,'" -crf 28 -c:a copy "{final_video_name}"
        :param :
        :return:
        """
        double_lang = self.resource_.srt_file_path()
        final_video_name = conf["ffmpeg"]["final_video_name"] if any(conf["ffmpeg"]["final_video_name"]) \
            else f"{today.year}-{today.month}-{today.day}.mp4"

        without_double_lang_name = 'temp_video_without_double.mp4' if double_lang else final_video_name

        command = f'{conf["ffmpeg"]["path"]} ' \
                  f'-i \"{conf["save_path"]}temp_video_without_font.mp4\" ' \
                  f'-lavfi ' \
                  f'\"subtitles={self.resource_.srt_file_path_}' \
                  f':force_style=' \
                  f'\'Alignment=2,' \
                  f'Fontname={self.resource_.font_mian_srt},' \
                  f'OutlineColour=&HFFFFFF00,' \
                  f'BorderStyle=3,' \
                  f'Outline=1,' \
                  f'Shadow=0,' \
                  f'Fontsize=18,' \
                  f'MarginL=5,' \
                  f'MarginV=20,\'\" ' \
                  f'-crf 28 ' \
                  f'-c:a copy ' \
                  f'-strict -2 ' \
                  f'\"{conf["save_path"]}{without_double_lang_name}\"'
        print(command)
        subprocess.call(command, shell=True)

        if double_lang:
            command = f'{conf["ffmpeg"]["path"]} ' \
                      f'-i \"{conf["save_path"]}{without_double_lang_name}\" ' \
                      f'-lavfi ' \
                      f'\"subtitles={self.resource_.sub_file_path}' \
                      f':force_style=' \
                      f'\'Alignment=6,' \
                      f'Fontname={self.resource_.font_sub_srt},' \
                      f'OutlineColour=&HFFFFFF00,' \
                      f'BorderStyle=3,' \
                      f'Outline=1,' \
                      f'Shadow=0,' \
                      f'Fontsize=18,' \
                      f'MarginL=5,' \
                      f'MarginV=20,\'\" ' \
                      f'-crf 28 ' \
                      f'-c:a copy ' \
                      f'-strict -2 ' \
                      f'\"{conf["save_path"]}{final_video_name}\"'
            print(command)
            subprocess.call(command, shell=True)

            if not conf['keep_temp']:
                path = conf["save_path"].replace("/", "\\") + without_double_lang_name
                subprocess.call(f'del {path}', shell=True)

        if not conf['keep_temp']:
            path = conf["save_path"].replace("/", "\\") + "temp_video_without_font.mp4"
            subprocess.call(f'del {path}', shell=True)


if __name__ == '__main__':
    pass
    # ffmpeg_use = ffmpeg_use()
    # ffmpeg_use.generate_video_without_audio()
    # ffmpeg_use.generate_video_with_audio()
    # ffmpeg_use.add_subtitle()