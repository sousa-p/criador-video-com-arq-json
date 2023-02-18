import json
from moviepy.editor import *
from moviepy.video.fx import all as vfx
import random
import math
import os


def break_text(text, max_line=33):
    # Função que quebra o texto, para caber no vídeo
    words = text.split()
    lines = []
    current_line = ""
    current_line_size = 0

    for word in words:
        if current_line_size + len(word) + 1 > max_line:
            lines.append(current_line.strip())
            current_line = ""
            current_line_size = 0

        current_line += f"{word} "
        current_line_size += len(word) + 1

    if current_line != "":
        lines.append(current_line.strip())

    return "\n".join(lines)


def clean_phrase (text):
    #Limpa a frase
    cleaned = text.replace('"', "").replace("'", "").split("(")[0].strip()
    return cleaned


def create_video (quote, bg_path, music_path, watermark_path, max_duration_video=12, video_size=(1080,1920), font="Bahnschrift",  fontsize=52):
        if not (quote or bg_path or music):
            return False
        
        bg = VideoFileClip(bg_path)
        bg = vfx.resize(bg, width=video_size[0]+70, height=video_size[1]+70)
        bg = bg.fx(vfx.colorx, 0.6)
        bg = bg.set_pos(("center", "center"))

        music = AudioFileClip(music_path)

        # Corta a duração da música caso ela seja maior que o parâmetro max_duration_video
        if max_duration_video and music.duration > max_duration_video:
            music = music.set_duration(max_duration_video)

        frase_txt = TextClip(f'"{break_text(clean_phrase(quote["frase"]))}"', color='white', font=font, fontsize=fontsize, size=(1040,750))
        frase_txt = frase_txt.set_duration(bg.duration)
        frase_txt = frase_txt.set_pos(("center", video_size[0]/3.3))

        autor_txt = TextClip(f"- {quote['autor']}", color='yellow', font=font, fontsize=fontsize, size=(1040,620))
        autor_txt = autor_txt.set_duration(bg.duration)
        autor_txt = autor_txt.set_pos(('center', video_size[0]/2))

        watermark = ImageClip(watermark_path, duration=bg.duration)
        watermark = vfx.resize(watermark, width=982, height=982)
        watermark = watermark.fx(vfx.colorx, 0.6)
        watermark = watermark.set_pos(("center", video_size[0]-100))

        video = CompositeVideoClip([bg, frase_txt, autor_txt, watermark], size=video_size)
        video = video.set_audio(music)
        return video

def main():

    filename = input('Coloque o nome do arquivo json: ')
    try:
        with open(f'.\\json\\{filename}.json') as f:
            quotes = json.load(f)
    except:
        print('Arquivo não encontrado')
        return False
    
    # Pega todos os vídeos de fundo que tenham ó inicio do nome igual ao do json
    extension_bg_video = '.mp4'
    bg_paths = [
        os.path.join('.\\src', nome)
        for nome in os.listdir('.\\src')
        if nome.lower().startswith(filename) and nome.lower().endswith(extension_bg_video)
    ]

    # Pega todas as músicas de fundo da pasta .\\src\\music
    extension_music = '.mpeg'
    musics_paths = [
        os.path.join('.\\src\\music', nome)
        for nome in os.listdir('.\\src\\music')
        if nome.lower().endswith(extension_music)
    ]

    # Caso realmente tenha vídeos
    if len(bg_paths) > 0 and len(musics_paths) > 0:
        for i,quote in enumerate(quotes):
            if quotes[0]["autor"] == quote["autor"]:
                bg = random.choice(bg_paths)
                music =  random.choice(musics_paths)
                video = create_video(quote, bg, music,'.\\src\\watermark.png')

                # Renderiza o vídeo caso este foi gerado
                if video:
                    video.write_videofile(f'.\\videos\\{filename}{i}.mp4', fps=30)
    else:
        print('Não há vídeos de fundo com o nome do arquivo json, ou não há músicas')
if __name__ == "__main__":
    while True:
        main()