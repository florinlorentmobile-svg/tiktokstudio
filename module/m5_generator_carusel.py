import os
import textwrap
import time
from PIL import Image, ImageDraw, ImageFont

def asigura_folder(cale):
    if not os.path.exists(cale):
        os.makedirs(cale)
    return cale

def genereaza_slide_uri(scenariu_actualizat, limba, folder_baza="rezultate/poze"):
    if not scenariu_actualizat: return
        
    folder_export = asigura_folder(os.path.join(folder_baza, f"Set_{int(time.time())}"))
    
    # 1. AM SCOS BECULEȚUL 💡 DE AICI CA SĂ SCĂPĂM DE DREPTUNGHI
    antet = "ȘTIAȚI CĂ?" if limba == "RO" else "DID YOU KNOW?"
    
    # Încărcăm fonturile de text cu calea absolută din Windows
    try:
        cale_arial = r"C:\Windows\Fonts\arialbd.ttf"
        font_titlu = ImageFont.truetype(cale_arial, 80)
        font_text = ImageFont.truetype(cale_arial, 60)
    except Exception as e:
        print(f"⚠️ Atenție: Nu am găsit Arial Bold. Folosesc font standard. ({e})")
        font_titlu, font_text = ImageFont.load_default(), ImageFont.load_default()

    # 2. Încărcăm fontul de Emoji FORȚAT cu calea absolută
    try:
        cale_emoji = r"C:\Windows\Fonts\seguiemj.ttf"
        font_emoji = ImageFont.truetype(cale_emoji, 120)
        are_font_emoji = True
    except:
        are_font_emoji = False
        print("⚠️ Atenție: Nu am putut găsi fontul de Emoji în Windows (seguiemj.ttf).")

    for i, scena in enumerate(scenariu_actualizat):
        text = scena.get("text", "")
        cale_img = scena.get("cale_imagine")
        emoji = scena.get("emoji", "")
        
        # Printează în consolă să vedem clar dacă Gemini ne-a dat emoticonul
        print(f"  -> Desenăm poza {i+1}... (Emoji primit de la AI: {emoji})")
        
        if not cale_img or not os.path.exists(cale_img): continue
            
        img = Image.open(cale_img).convert("RGBA")
        resample_metoda = getattr(Image, 'Resampling', Image).LANCZOS
        img = img.resize((1080, 1920), resample_metoda)
        
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 160))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # Desenăm titlul curat (fără dreptunghi)
        draw.text((540, 300), antet, font=font_titlu, fill="yellow", anchor="mm")
        
        # Desenăm emoji-ul dacă sistemul a reușit să încarce fontul
        if emoji and are_font_emoji:
            try:
                draw.text((540, 480), emoji, font=font_emoji, fill="white", anchor="mm", embedded_color=True)
            except Exception as e:
                print(f"    ⚠️ Eroare la lipirea emoji-ului pe poza {i+1}: {e}")
        
        text_formatat = "\n".join(textwrap.wrap(text, width=28))
        draw.text((540, 1000), text_formatat, font=font_text, fill="white", anchor="mm", align="center")
        
        img.convert("RGB").save(os.path.join(folder_export, f"Foto_{i+1}.jpg"), quality=95)
        
    print(f"\n✅ SET POZE SALVAT ÎN: {folder_export}")