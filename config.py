import yaml as yaml_origin
import os
import sys
import re

debug = True

rootpath = os.path.abspath(os.path.dirname(__file__))

def get_config():
    if os.path.exists('config.yaml'):
        with open(os.path.join(rootpath, 'config.yaml'), 'r', encoding='utf8') as f:
            config = yaml_origin.safe_load(f)  # 解析不了喵 解析了   这里系统查看了字体的路径，发现没字体，所以报错了  路径我乱填的
        conf_ffmpeg = config['ffmpeg']
        conf_folder = config['folder']
        conf_albumen = config['AlbumCover']
        conf_lrc2srt = config['Lrc2Srt']
        conf_keeptemp = config['keep_temp']
        if debug == False:
            assert any(config['folder']), "资源所在文件夹路径必须填写"
            assert any(conf_ffmpeg['path']), "ffmpeg路径必须为填写"
            assert any(config['save_path']), "保存路径必须填写"
            assert os.path.exists(conf_albumen['cn_font']), "中文字体路径不存在"
            assert os.path.exists(conf_albumen['en_font']), "英文字体路径不存在"
            assert os.path.exists(conf_albumen['jn_font']), "日文字体路径不存在"
            assert os.path.exists(conf_albumen['ot_font']), "其他文字体路径不存在"
            assert conf_albumen['choose_font'] in ['cn', 'en', 'jn', 'ot'], "选择字体必须为cn, en, jn, ot之一"
            assert isinstance(conf_albumen['FONT_SIZE_LARGE'], int), "大字体大小必须为整数"
            assert isinstance(conf_albumen['FONT_SIZE_SMALL'], int), "小字体大小必须为整数"
            assert os.path.exists(conf_ffmpeg['path']), "ffmpeg路径不存在"
            assert os.path.isdir(conf_ffmpeg['folder']), "ffmpeg所在文件夹路径不是一个目录"
            assert os.path.isdir(conf_ffmpeg['subtitle_path']), "字幕路径不是一个目录"
            assert re.match(r"\d+x\d+", conf_ffmpeg['frame']), "分辨率格式不正确，应为数字x数字"
            assert isinstance(conf_ffmpeg['fps'], int), "帧率必须为整数"
            assert isinstance(conf_ffmpeg['crf'], int), "视频质量必须为整数"
            assert conf_ffmpeg['vcodec'] in ['libx264', 'libx265'], "视频编码器必须为libx264或libx265之一"
            assert re.match(r"\d+k", conf_ffmpeg['-b:v']), "视频码率格式不正确, 应为数字k"
            assert conf_ffmpeg['-preset'] in ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'], "编码速度必须为ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow之一"
            assert conf_ffmpeg['-pix_fmt'] in ['yuv420p', 'yuv422p', 'yuv444p'], "视频像素格式必须为yuv420p, yuv422p, yuv444p之一"
        return config
#     else:
#         import ruamel.yaml  # 这里先留，会放到README.md里
#
#         generate_yaml = open(os.path.join('./src/data/config.yaml'), 'r', encoding='utf8').read()
#         """\  # 这里原本的作用是，如果没有yaml就生成yaml，下面的文本是yaml的内容
# AlbumCover:
#   albumen: ''          # 专辑名称
#   title: ''               # 歌曲名称
#   artist: ''             # 歌手名称
#   albumcover: ''         # *专辑封面路径
#   save_path: 'data/'          # *保存路径
#   cn_ttf: /usr/share/fonts/truetype/wqy/wqy-microhei.ttc # 中文字体路径
#   en_ttf: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf # 英文字体路径
#   jn_ttf: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc # 日文字体路径
#   ot_ttf: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc # 其他文字体路径 手动指定
#   choose_font: 'ot' # *选择字体
#   FONT_SIZE_LARGE: 115 # *大字体大小
#   FONT_SIZE_SMALL: 60 # *小字体大小
# ffmpeg:               # *ffmpeg配置
#   path: /usr/bin/ffmpeg # *ffmpeg路径
#   folder: data/     # *ffmpeg所在文件夹路径
#   subtitle_path: data/ # *字幕路径
#   frame: 1920x1080      # *分辨率
#   fps: 30               # *帧率
#   crf: 18               # *视频质量, 越小质量越高, 一般在18-28之间
#   vcodec: libx264       # *视频编码器, libx264为h264编码, libx265为h265编码
#   -b:v: 3000k           # *视频码率, 一般为3000k
#   -preset: medium     # *编码速度, 越慢表示压缩率越高，文件越小，但编码时间也越长。
#   -pix_fmt: yuv420p     # *视频像素格式, 一般为yuv420p
#   final_video_name: '' # 最终视频文件名
#   #  -g: 60                # 关键帧间隔, 一般为fps的两倍
#   #  -c:a: aac             # 音频编码器, 一般为aac
#   #  -b:a: 128k            # 音频码率, 一般为128k
#   #  -ac: 2                # 音频通道数, 一般为2
#   #  -ar: 44100            # 音频采样率, 一般为44100
#   #  -f: flv               # 输出格式, 一般为flv
#   #  -tune: zerolatency    # 编码模式, 一般为zerolatency
#   #  -profile:v: high      # 编码级别, 一般为high
#   #  -level: 4.0           # 编码级别, 一般为4.0
#   #  -bufsize: 6000k       # 视频缓冲区大小, 一般为6000k
#   #  -maxrate: 6000k       # 视频最大码率, 一般为6000k
#   #  -minrate: 3000k       # 视频最小码率, 一般为3000k
#   #  pic_path: data/ # 图片路径
#         """
#         yaml = ruamel.yaml.YAML()
#         config = yaml.load(generate_yaml)
#
#         with open(os.path.join(rootpath, 'config.yaml'), 'w', encoding='utf8') as f:
#             yaml.dump(config, f)
#         sys.exit('已生成config.yaml配置文件, 请填写参数后重新运行')

conf = get_config()

if __name__ == '__main__':
    print(type(get_config()))
    print(rootpath)