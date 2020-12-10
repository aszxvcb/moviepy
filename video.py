from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/local/Cellar/imagemagick/7.0.10-46/bin/convert"})

def generate_video(audio_src_path="", disaster = "" ):
    # path지정
    path ="./web/static/video/"
    # audio_src_path = "./web/static/video/test.wav"
    disaster_name = path + disaster +".mp4"

    # 영상 배경
    background = VideoFileClip(path +"news_template2.mp4", audio=False).subclip(0,22)
    w ,h = moviesize = background.size

    # 뉴스 참고 자료 영상
    # disaster_name =path +"/dust.mp4"
    disaster_video = (VideoFileClip(disaster_name ,audio=False).
                subclip(0 ,22).
                resize(( w /1.8 , h /1.8)).    # one third of the total screen
                margin( 6 ,color=(255 ,255 ,255)).  # white margin
                margin( bottom=130, right=20, opacity=0). # transparent
                set_pos(('right' ,'bottom')))

    # 뉴스 title_재난 종류
    text ="긴급재난방송_"

    if disaster=="dust":
        text=text+"미세먼지"
    elif disaster=="typhoon":
        text=text+"태풍"

    # text ="Breaking News"
    text =text.encode('utf-8')
    # txt = TextClip(text, font="Arial" ,color='white' ,fontsize=30)
    txt = TextClip(text, font="/Library/Fonts/NanumBarunGothic.otf", color='white', fontsize=30)
    txt_col = txt.on_color(size=(background.w + txt. w +20 ,txt. h +40),
                           color=(0 ,0 ,0), pos=(6 ,'center'), col_opacity=0.6)
    txt_mov = txt_col.set_pos( lambda t: (max( w /30 ,int( w -0.5 * w * t)),
                                          max( 5 * h /6 ,int(50 * t))) )

    # 뉴스 자막_재난 종류
    if disaster=="dust":
        sub_txt = [((0, 6), '재난 속보입니다.\n현재 미세먼지 경보가\n발령되었습니다.\n자세한 뉴스는 리포터를\n통해 전해드리겠습니다.\n'),\
                   ((6, 12), '재난 속보입니다.\n시베리아 한파를 타고\n몰려온 미세먼지로 인해\n서울지역에 미세먼지\n경보가 발령되었습니다.\n'),\
                   ((12, 15), '\n어린이, 노약자는\n실외 활동을 자제 바랍니다.\n'),\
                   ((15, 22), '또한 대중교통\n이용을 권장 드리며,\n보건용 마스크를 착용하여\n건강 관리에 유의하시길\n바랍니다.\n')]

    elif disaster=="typhoon":
        sub_txt = [((0, 6), '재난 속보입니다.\n현재 태풍 경보가\n발령되었습니다.\n자세한 뉴스는 리포터를\n통해 전해드리겠습니다.\n'),\
                   ((6, 9), '재난 속보입니다.\n진도 지역에서\n태풍 경보가\n발령되었습니다.\n'),\
                   ((9, 15), '신속히 안전한 곳으로\n대피하시고,\n외출을 삼가하시기\n바랍니다.\n')]

    generator =lambda t :TextClip(t, font="/Library/Fonts/NanumBarunGothic.otf", color='white', fontsize=20)
    subtitles =SubtitlesClip(sub_txt, generator).set_position((0.032,0.3), relative=True)

    # outro_voice
    # voice =AudioFileClip(path +"/test.wav")
    voice = AudioFileClip(audio_src_path)
    voice_new = CompositeAudioClip([voice])

    # outro_영상, 자막, voice 합쳐짐
    final = CompositeVideoClip([background ,subtitles ,txt_mov ,disaster_video])
    final.audio =voice_new

    clip_time=22
    final.subclip(0 ,clip_time).write_videofile( path+"outro.mp4" ,fps=24 ,codec='libx264')

    intro=VideoFileClip(path+"intro.mp4")
    outro=VideoFileClip(path+"outro.mp4")

    res=concatenate_videoclips([intro,outro])
    output_path = path + "news.mp4"
    res.write_videofile(output_path, fps=24, codec='libx264')

    return output_path


if __name__ == '__main__':
    generate_video("./web/static/video/test.wav", "dust");