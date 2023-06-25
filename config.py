import yaml as yaml_origin
import os
import sys


rootpath = os.path.abspath(os.path.dirname(__file__))


def get_config():
    if os.path.exists('config.yaml'):
        with open(os.path.join(rootpath, 'config.yaml'), 'r', encoding='utf8') as f:
            config = yaml_origin.safe_load(f)
        conf_ffmpeg = config['ffmpeg']
        # assert type(conf_ffmpeg['port']) is int, "数据库端口号必须为int类型"
        return config
    else:
        import ruamel.yaml
        generate_yaml = """\
AlbumCover:
  albumen: ''          # 专辑名称
  title: ''               # 歌曲名称
  artist: ''             # 歌手名称
  albumcover: ''         # *专辑封面路径
  save_path: 'data/'          # *保存路径
  cn_ttf: /usr/share/fonts/truetype/wqy/wqy-microhei.ttc # 中文字体路径
  en_ttf: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf # 英文字体路径
  jn_ttf: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc # 日文字体路径
  ot_ttf: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc # 其他文字体路径 手动指定
  choose_font: 'ot' # *选择字体
  FONT_SIZE_LARGE: 115 # *大字体大小
  FONT_SIZE_SMALL: 60 # *小字体大小
ffmpeg:               # *ffmpeg配置
  path: /usr/bin/ffmpeg # *ffmpeg路径
  folder: data/     # *ffmpeg所在文件夹路径
  subtitle_path: data/ # *字幕路径
  frame: 1920x1080      # *分辨率
  fps: 30               # *帧率
  crf: 18               # *视频质量, 越小质量越高, 一般在18-28之间
  vcodec: libx264       # *视频编码器, libx264为h264编码, libx265为h265编码
  -b:v: 3000k           # *视频码率, 一般为3000k
  -preset: medium     # *编码速度, 越慢表示压缩率越高，文件越小，但编码时间也越长。
  -pix_fmt: yuv420p     # *视频像素格式, 一般为yuv420p
  final_video_name: '' # 最终视频文件名
  #  -g: 60                # 关键帧间隔, 一般为fps的两倍
  #  -c:a: aac             # 音频编码器, 一般为aac
  #  -b:a: 128k            # 音频码率, 一般为128k
  #  -ac: 2                # 音频通道数, 一般为2
  #  -ar: 44100            # 音频采样率, 一般为44100
  #  -f: flv               # 输出格式, 一般为flv
  #  -tune: zerolatency    # 编码模式, 一般为zerolatency
  #  -profile:v: high      # 编码级别, 一般为high
  #  -level: 4.0           # 编码级别, 一般为4.0
  #  -bufsize: 6000k       # 视频缓冲区大小, 一般为6000k
  #  -maxrate: 6000k       # 视频最大码率, 一般为6000k
  #  -minrate: 3000k       # 视频最小码率, 一般为3000k
  #  pic_path: data/ # 图片路径
        """
        yaml = ruamel.yaml.YAML()
        config = yaml.load(generate_yaml)

        with open(os.path.join(rootpath, 'config.yaml'), 'w', encoding='utf8') as f:
            yaml.dump(config, f)
        sys.exit('已生成config.yaml配置文件，请填写参数后重新运行')


conf = get_config()

if __name__ == '__main__':
    print(type(get_config()))
    print(rootpath)
