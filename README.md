# ffmpeg_py

## 使用

安装依赖的第三方库

``pip install -r requirements.txt``

编辑后运行 start.bat

或

``python main.py``

## 配置

首次运行会生成config.yaml文件, 填写配置项再次运行即可

完整配置项如下

```yaml
# 本文件为配置文件 *为必填项
folder: 'resource/'     # *资源所在文件夹路径
keep_temp: False  # *是否保留临时文件
save_path: 'result/'          # *保存路径
AlbumCover:
  albumen: ''          # 专辑名称
  title: ''               # 歌曲名称
  artist: ''             # 歌手名称 以上三项任意一项手动则全部手动
  albumcover: ''         # *专辑封面路径
  cn_font: C:\Windows\Fonts\*.ttc # 中文字体路径
  en_font: C:\Windows\Fonts\*.ttc # 英文字体路径
  jp_font: C:\Windows\Fonts\*.ttc # 日文字体路径
  ot_font: C:\Windows\Fonts\*.ttf # 其他文字体路径 手动指定
  choose_font: 'jp' # *选择字体
  FONT_SIZE_LARGE: 115 # *大字体大小
  FONT_SIZE_SMALL: 60 # *小字体大小
Lrc2Srt:
  cn_font: 'Consolas' # *中文字体名称
  en_font: 'Consolas' # *英文字体名称
  jp_font: 'Consolas' # *日文字体名称
  ot_font: 'Consolas' # *其他文字体名称 手动指定
  main_font: 'jp' # *双语模式下选择原文字体
  sub_font: 'cn' # *选择译文字体
ffmpeg:               # *ffmpeg配置
  path: ffmpeg # *ffmpeg路径 如果环境已配置可只填ffmpeg
  frame: 2440x1080      # *分辨率
  fps: 30               # *帧率
  crf: 18               # *视频质量, 越小质量越高, 一般在18-28之间
  vcodec: h264_nvenc      # *视频编码器, libx264为h264编码, libx265为h265编码 libaom-av1 libvpx h264_nvenc
  -b:v: 10000k           # *视频码率, 一般为900k
  -preset: slow     # *编码速度, 越慢表示压缩率越高，文件越小，但编码时间也越长。medium
  -pix_fmt: yuv420p     # *视频像素格式, 一般为yuv420p
  final_video_name: '' # 最终视频文件名
```

## 关于FFmpeg

测试用的FFmpeg版本为5.1.2

### FFmpeg 压制字幕的说明
以下为FFmpeg压制字幕的参数说明, 如果需要修改指令，需要到[代码](src/FFmpegUse.py)中的函数add_subtitle里修改

```shell
01.Name             风格(Style)的名称. 区分大小写. 不能包含逗号.
02.Fontname         使用的字体名称, 区分大小写.
03.Fontsize         字体的字号
04.PrimaryColour    设置主要颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR. 为字幕填充颜色
05.SecondaryColour  设置次要颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR. 在卡拉OK效果中由次要颜色变为主要颜色.
06.OutlineColour    设置轮廓颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR.
07.BackColour       设置阴影颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR. ASS的这些字段还包含了alpha通道信息. (AABBGGRR), 注ASS的颜色代码要在前面加上&H
08.Bold             -1为粗体, 0为常规
09.Italic           -1为斜体, 0为常规
10.Underline       [-1 或者 0] 下划线
11.Strikeout       [-1 或者 0] 中划线/删除线
12.ScaleX          修改文字的宽度. 为百分数
13.ScaleY          修改文字的高度. 为百分数
14.Spacing         文字间的额外间隙. 为像素数
15.Angle           按Z轴进行旋转的度数, 原点由alignment进行了定义. 可以为小数
16.BorderStyle     1=边框+阴影, 3=纯色背景. 当值为3时, 文字下方为轮廓颜色的背景, 最下方为阴影颜色背景.
17.Outline         当BorderStyle为1时, 该值定义文字轮廓宽度, 为像素数, 常见有0, 1, 2, 3, 4.
18.Shadow          当BorderStyle为1时, 该值定义阴影的深度, 为像素数, 常见有0, 1, 2, 3, 4.
19.Alignment       定义字幕的位置. 字幕在下方时, 1=左对齐, 2=居中, 3=右对齐. 1, 2, 3加上4后字幕出现在屏幕上方. 1, 2, 3加上8后字幕出现在屏幕中间. 例: 11=屏幕中间右对齐. Alignment对于ASS字幕而言, 字幕的位置与小键盘数字对应的位置相同.
20.MarginL         字幕可出现区域与左边缘的距离, 为像素数
21.MarginR         字幕可出现区域与右边缘的距离, 为像素数
22.MarginV         垂直距离
```

RGB十六进制[参考](https://www.cnblogs.com/cainiao-chuanqi/p/11301471.html)

透明度十六进制[参考](https://www.cnblogs.com/riyueqian/p/13492932.html)

参考指令如下
    
```shell
PATH_TO\ffmpeg.exe -i "input_video.mp4" -lavfi "subtitles=path_to/srt.srt:force_style='Alignment=6,Fontname=Consolas,OutlineColour=&HFFFFFF00,BorderStyle=3,Outline=1,Shadow=0,Fontsize=18,MarginL=5,MarginV=20,'" -crf 28 -c:a copy "output.mp4"
```

### 关于字幕字体

Windows系统中的字体文件位于`C:\Windows\Fonts`目录下

请直接复制名称到conf中Lrc2Srt的Fontname字段中

关于如何安装字体，可以参考[此处](https://www.zhihu.com/question/391991118)


## 项目结构
  
  ```shell
  ├── README.md
  ├── config.yaml
  ├── requirements.txt
  ├── resource
  │   ├── 1.mp3
  │   ├── 1.lrc
  │   └── 1.jpg
  │   
  ├── result
  │   ├── output.mp4
  │   └── output.jpg
  ├── src 
  │   ├── FFmpegUse.py
  │   ├── Lrc2Srt.py
  │   ├── __init__.py
  │   ├── AlbumCover.py
  │   └── Resource.py
  ├── start.bat
  └── main.py
  ```
