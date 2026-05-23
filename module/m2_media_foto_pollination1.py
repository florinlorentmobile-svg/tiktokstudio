import os
import requests
import urllib.parse
import time

def asigura_folder_temp(nume_folder="temp/imagini"):
    """Creează folderul temporar dacă nu există."""
    if not os.path.exists(nume_folder):
        os.makedirs(nume_folder)
    return nume_folder

def descarca_imagine(prompt, index, folder_salvare):
    """
    Trimite promptul către API și descarcă imaginea.
    Are sistem de reîncercare și imagine de avarie.
    """
    prompt_curat = urllib.parse.quote(prompt)
    width = 1080
    height = 1920
    url = f"https://image.pollinations.ai/prompt/{prompt_curat}?width={width}&height={height}&nologo=true"
    cale_fisier = os.path.join(folder_salvare, f"scena_{index}.jpg")
    
    # Mascăm scriptul ca fiind un browser de PC pentru a nu fi blocați de server
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Încercăm de 2 ori să descărcăm imaginea reală
    for incercare in range(2):
        try:
            print(f"    ⏳ Contactăm serverul foto (încercarea {incercare+1}/2)...")
            raspuns = requests.get(url, headers=headers, timeout=60)
            
            if raspuns.status_code == 200:
                with open(cale_fisier, 'wb') as f:
                    f.write(raspuns.content)
                return cale_fisier
            else:
                print(f"    ⚠️ Eroare de la server: {raspuns.status_code}")
                
        except requests.exceptions.Timeout:
            print("    ⚠️ Timeout: Serverul este supraaglomerat.")
        except Exception as e:
            print(f"    ❌ Eroare: {e}")
            
        time.sleep(2) # Așteptăm 2 secunde înainte de a reîncerca
        
    # SISTEM DE AVARIE: Dacă API-ul e picat de tot, descărcăm o poză gri cu text
    # Acest lucru asigură că MoviePy are cu ce să lucreze pentru testul final!
    print("    🔄 Serverul AI nu răspunde. Generăm o imagine de siguranță pentru a continua montajul...")
    url_placeholder = f"https://placehold.co/{width}x{height}/222222/FFFFFF/png?text=Scena+{index+1}+Foto+Indisponibila"
    
    try:
        rasp_place = requests.get(url_placeholder, headers=headers, timeout=15)
        with open(cale_fisier, 'wb') as f:
            f.write(rasp_place.content)
        return cale_fisier
    except:
        return None

def descarca_pentru_scenariu(scenariu_json, tip="video"):
    """
    Parcurge întregul scenariu și descarcă pozele pentru fiecare scenă.
    """
    if not scenariu_json:
        print("❌ Scenariul este gol, nu avem ce descărca.")
        return []

    print("\n📸 Începem generarea și descărcarea imaginilor...")
    folder = asigura_folder_temp("temp/imagini_video" if tip == "video" else "temp/imagini_carusel")
    scenariu_actualizat = []
    
    for i, scena in enumerate(scenariu_json):
        text_narare = scena.get("text", "")
        img_prompt = scena.get("img_prompt", "")
        
        print(f"  -> Procesăm imaginea {i+1}/{len(scenariu_json)}...")
        
        cale_locala = descarca_imagine(img_prompt, i, folder)
        
        if cale_locala:
            scena["cale_imagine"] = cale_locala
            scenariu_actualizat.append(scena)
        else:
            print(f"  -> ⚠️ Am ratat definitiv imaginea {i+1}, o excludem din montaj.")

    print(f"✅ Descărcare completă! ({len(scenariu_actualizat)} imagini salvate)")
    return scenariu_actualizat