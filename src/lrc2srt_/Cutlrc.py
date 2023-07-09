import os
import pylrc

class qe_rs:
    def __init__(self):
        self.start_line = None
        self.mode = None

class lrc2srt:
    '''
    将lrc文件转换为srt文件
    '''
    def __init__(self):
        self.lrc_file = open('TOKYO 4AM-MusicEnc.lrc', encoding='utf-8') # file_path = conf.lrc_file_path
        lrc_string = ''.join(self.lrc_file.readlines())
        self.lrc_file.close()
        self.subs = pylrc.parse(lrc_string)
        print(self.subs)

    def show_lrc(self) -> None: 
        '''
        展示歌词
        '''
        # subs_copy = [sub.text+'\r' for sub in self.subs]
        subs_copy = enumerate(self.subs)
        for sub in subs_copy: 
            print(sub[0], sub[1].text)
    
    @staticmethod
    def lan_mode():
        '''
        获取lrc中的语言格式
        '''
        lan_mode = input('选择语言模式:\n[1]单语\n[2]双语\n>>>')
        os.system('cls')
        return lan_mode

    def start_line_(self,mode=True):
        '''
        起始切割行数
        '''
        self.show_lrc(subs=self.subs)
        if mode != True:
            print('输入异常,请重新输入!')
        most_line = len(self.subs) 
        try:
            start_line = int(input('输入开始行数(包含该行数):\n>>>')) if start_line != 'exit' else exit()
        except ValueError:
            os.system('cls')
            return self.start_line_(mode=False)
        os.system('cls')
        if start_line <= most_line:
            return start_line
        else:
            return self.start_line_(mode=False)
    
    def cut_line(self):
        '''
        切割模式
        '''
        mode = input('选择切割模式:\n[1]切割一半\n[2]交替切割\n>>>')  
        if mode == '1':
            return 'half'
        elif mode == '2':
            return 'alt'
        elif mode == 'exit':
            exit()
        else:
            return self.cut_line()

    def interact_lrc(self) -> None: 
        qe = qe_rs()
        lan_mode_ = self.lan_mode()

        if lan_mode_ == '1':
            qe.start_line = self.start_line_()
            return qe
        elif lan_mode_ == '2':
            qe.start_line = self.start_line_()
            qe.mode = self.cut_line()
            return qe  
        elif lan_mode_ == 'exit':
            exit()
        else:
            return self.interact_lrc()

    def spilt_lrc(self, staet_line, mode=''):
        '''
        切割歌词
        '''
        i = 0
        while i == staet_line:
            del self.subs[i]
            i += 1
        if mode == 'half':
            self.subs = self.subs[:len(self.subs)//2]
        elif mode == 'alt':
            self.main_subs = self.subs[::2]
            self.sub_subs = self.subs[1::2]
        else:
            pass

    def remove_lrc(self, subs, line) -> None:
        '''
        移除某一行歌词
        '''
        del subs[line]
        pass

    def check_lrc(self) -> None:
        '''
        检查歌词
        '''
        self.show_lrc(subs=self.main_subs)
        line = input('输入要移除的行数:\n>>>')
        if line == 'ok':
            pass
        else:
            try:
                line = int(line) 
            except ValueError:  
                return self.check_lrc()
        self.show_lrc(subs=self.sub_subs)
        pass