from PIL import Image, ImageDraw, ImageFont, ImageFilter

from src.Resource import resource, conf

RGB_TEXT = (255, 255, 255)

class AlbumCoverGenerator:
    """
    专辑图片生成
    """
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
        assert type(self.resource.title) is str, "专辑标题异常，请手动填写专辑信息"
        assert type(self.resource.artist) is str, "专辑艺术家异常，请手动填写专辑信息"
        assert type(self.resource.album) is str, "专辑名称异常，请手动填写专辑信息"
        self.draw_text(self.resource.title, (1152, 240), font_large, RGB_TEXT, outline_color, outline_width)
        self.draw_text(self.resource.artist, (1152, 450), font_small, RGB_TEXT, outline_color, outline_width)
        self.draw_text(self.resource.album, (1152, 540), font_small, RGB_TEXT, outline_color, outline_width)

        # 保存图像
        self.img.save(self.resource.pic_savepath, "PNG")
        # 显示图像
        self.img.show()