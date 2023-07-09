import pylrc
import os
from pylrc.classes import Lyrics

class qe_rs:
    def __init__(self):
        self.start_line = None
        self.mode = None

class lrc2srt:
    """
    将lrc文件转换为srt文件
    """
    def __init__(self, lrc_file_path) -> None:
        self.main_subs = None
        self.sub_subs = None
        self.lrc_file_path = lrc_file_path
        self.lrc_file = open(self.lrc_file_path, encoding='utf-8')
        lrc_string = ''.join(self.lrc_file.readlines())
        self.lrc_file.close()
        self.subs = pylrc.parse(lrc_string)


    def show_lrc(self, subs) -> None:  # 为什么不用self.subs
        """
        展示歌词
        """
        # subs_copy = [sub.text+'\r' for sub in self.subs]
        subs_copy = enumerate(subs)
        for sub in subs_copy: 
            print(sub[0], sub[1].text)

    def interact_lrc(self) -> qe_rs:
        """
        交互模式
        通过递归确保输入正确
        或许用装饰器更好?
        """

        def lan_mode():
            """
            获取lrc中的语言格式
            """
            lan_mode = input('选择语言模式:\n[1]单语\n[2]双语\n>>>')
            os.system('cls') 
            return lan_mode
        
        def start_line_(mode=True):
            """
            起始切割行数
            """
            self.show_lrc(subs=self.subs)
            if mode != True:
                print('输入异常,请重新输入!')
            most_line = len(self.subs) 
            try:
                start_line = int(input('输入开始行数(包含该行数):\n>>>')) #  if start_line != 'exit' else exit()
            except ValueError:
                os.system('cls')
                return start_line_(mode=False)
            os.system('cls')
            if start_line <= most_line:
                return start_line
            else:
                return start_line_(mode=False)
            
        def cut_line():
            """
            切割模式
            """
            mode = input('选择切割模式:\n[1]切割一半\n[2]交替切割\n>>>')  
            if mode == '1':
                return 'half'
            elif mode == '2':
                return 'alt'
            elif mode == 'exit':
                exit()
            else:
                return cut_line()
        
        qe = qe_rs()
        lan_mode_ = lan_mode()

        if lan_mode_ == '1':
            qe.start_line = start_line_()
            return qe
        elif lan_mode_ == '2':
            qe.start_line = start_line_()
            qe.mode = cut_line()
            return qe  
        elif lan_mode_ == 'exit':
            exit()
        else:
            return self.interact_lrc()


    def spilt_lrc(self, start_line, mode=''):
        """
        切割歌词
        """
        for _ in range(start_line):
            self.subs.pop(0)    # del无效
        self.main_subs = Lyrics() 
        self.sub_subs = Lyrics() 
        if mode == 'half':  # 对半切割
            i = 0
            for sub in self.subs:
                if i < len(self.subs)/2:  
                    self.main_subs.append(sub)
                else:
                    self.sub_subs.append(sub)
                i += 1
        elif mode == 'alt': # 交替切割
            i = 0
            for sub in self.subs:
                if i%2 == 0:
                    self.main_subs.append(sub)
                else:
                    self.sub_subs.append(sub)
                i += 1
        else:
            pass

    def remove_lrc(self, subs, line) -> None:
        """
        移除某一行歌词
        """
        del subs[line]
        pass

    def check_lrc(self) -> None:
        """
        检查歌词
        """
        self.show_lrc(subs=self.main_subs)
        line = input('输入要移除的行数:\n>>>')
        if line == 'ok':
            pass
        else:
            try:
                line = int(line)    # 可以集成和其他功能一起  # 拆分开来，关注点分离，单一职责原则 如果不在main调用就是拆开 这个lrc2srt就是单独处理歌词的
            except ValueError:  # 为啥不单独写个命令行工具来切割lrc，在这个文件再集成
                """
            应该是  但是生成srt只需要不到五行 但也不能class里的def里class和def，这是屎山的第一步
            我有强迫症
            感觉还好 特性不用白不用
            def嵌套是我在尝试用递归   其实可以不用def嵌套搞，但是我懒得想了
            class可以丢上面去
            - lrc2srt
            | - __init__.py
            | - 切割src.py
            | - 生成srt.py
                """
                return self.check_lrc()
        self.show_lrc(subs=self.sub_subs)
        pass

    def tosrt(self) -> None:
        """
        生成srt文件
        """
        if any([self.main_subs, self.sub_subs]):
            main_srt = self.main_subs.toSRT()
            sub_srt = self.sub_subs.toSRT()
            with open('resource/main.srt', 'w', encoding='utf-8') as srt_file:
                srt_file.write(main_srt)
                srt_file.close()
            with open('resource/sub.srt', 'w', encoding='utf-8') as srt_file:
                srt_file.write(sub_srt)
                srt_file.close()
        else:
            srt = self.subs.toSRT()
            with open('resource/main.srt', 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt)
                srt_file.close()
        print('如果有乱码, 用gb2312打开')


if __name__ == '__main__':
    pass


