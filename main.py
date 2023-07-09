from src.lrc2srt import lrc2srt
from src.Resource import resource
from src.AlbumCoverGenerator import AlbumCoverGenerator
from src.FFmpegUse import ffmpeg_use

def main():
    resource_ = resource()
    lrc2srt_ = lrc2srt(resource_.lrc_file_path)
    interact = lrc2srt_.interact_lrc()
    lrc2srt_.spilt_lrc(start_line=interact.start_line, mode=interact.mode)
    lrc2srt_.tosrt()

    generator = AlbumCoverGenerator()
    generator.generate_album_cover()

    ffmpeg = ffmpeg_use()
    ffmpeg.generate_video_without_audio()
    ffmpeg.generate_video_with_audio()
    ffmpeg.add_subtitle()

if __name__ == "__main__":
    main()
