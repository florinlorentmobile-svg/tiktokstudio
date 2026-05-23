import os
import textwrap
import PIL.Image

if hasattr(PIL.Image, 'Resampling'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
else:
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

cale_magick = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
os.environ["IMAGEMAGICK_BINARY"] = cale_magick

from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# AM MODIFICAT AICI: Salvează strict în "rezultate/video"
def asigura_folder_export(nume_folder="rezultate/video"):
    if not os.path.exists(nume_folder):
        os.makedirs(nume_folder)
    return nume_folder

def asambleaza_final(scenariu_actualizat, nume_fisier_iesire="video_final.mp4"):
    if not scenariu_actualizat: return
    
    folder_export = asigura_folder_export()
    cale_iesire = os.path.join(folder_export, nume_fisier_iesire)
    clipuri_finale = []
    
    for i, scena in enumerate(scenariu_actualizat):
        text_brut, cale_img, cale_aud = scena.get("text", ""), scena.get("cale_imagine"), scena.get("cale_audio")
        if not cale_img or not cale_aud or not os.path.exists(cale_img) or not os.path.exists(cale_aud): continue
            
        audio_clip = AudioFileClip(cale_aud)
        img_clip = ImageClip(cale_img).resize((1080, 1920)).set_duration(audio_clip.duration)
        text_formatat = "\n".join(textwrap.wrap(text_brut, width=28))
        
        # EXACT CUM AI CERUT: Subtitrare galbena peste tot
        culoare_text = 'yellow'
        
        txt_clip = TextClip(text_formatat, fontsize=65, color=culoare_text, font='Arial-Bold', stroke_color='black', stroke_width=3, method='label', align='center')
        txt_clip = txt_clip.set_position(('center', 0.55), relative=True).set_duration(audio_clip.duration)
        
        video_scena = CompositeVideoClip([img_clip, txt_clip]).set_audio(audio_clip)
        clipuri_finale.append(video_scena)
        
    if clipuri_finale:
        print("\n⏳ Randare MP4...")
        video_complet = concatenate_videoclips(clipuri_finale, method="compose")
        video_complet.write_videofile(cale_iesire, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4)
        video_complet.close()
        print(f"✅ VIDEO SALVAT ÎN: {cale_iesire}")