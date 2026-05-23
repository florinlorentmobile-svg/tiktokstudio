import os
import time
import requests
from dotenv import load_dotenv

# Citim cheia direct din seif
load_dotenv()
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")

def asigura_folder_temp(nume_folder="temp/imagini"):
    if not os.path.exists(nume_folder):
        os.makedirs(nume_folder)
    return nume_folder

def descarca_imagine_leonardo(prompt, index, folder_salvare):
    if not LEONARDO_API_KEY:
        print("    ❌ EROARE: Lipsește LEONARDO_API_KEY din fișierul .env!")
        return None

    url_generare = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}"
    }
    
    # Modelul Leonardo Kino XL (specializat pe cinematic/documentar)
    # Rezoluție 768x1344 (ideal pentru TikTok pe modele XL, ulterior redimensionat de MoviePy la 1080)
    payload = {
        "prompt": prompt,
        "num_images": 1,
        "width": 768,
        "height": 1344,
        "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628", 
        "promptMagic": False
    }

    try:
        print("    ⏳ [Leonardo API] Trimitem comanda către server...")
        # 1. Declanșăm generarea
        response = requests.post(url_generare, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"    ❌ Eroare Leonardo: {response.text}")
            return None
        
        gen_data = response.json()
        gen_id = gen_data.get('sdGenerationJob', {}).get('generationId')
        
        if not gen_id:
            print("    ❌ Nu am primit ID-ul de generare.")
            return None

        print("    ⏳ [Leonardo API] Pictăm... Așteptăm finalizarea randării (aprox 10-20 sec)...")
        url_status = f"https://cloud.leonardo.ai/api/rest/v1/generations/{gen_id}"
        
        # 2. Așteptăm până imaginea este complet generată
        timp_asteptat = 0
        while timp_asteptat < 60:
            time.sleep(3) # Întrebăm serverul din 3 în 3 secunde
            timp_asteptat += 3
            
            res_status = requests.get(url_status, headers=headers)
            if res_status.status_code == 200:
                status_data = res_status.json()
                status = status_data.get('generations_by_pk', {}).get('status')
                
                if status == 'COMPLETE':
                    imagini = status_data.get('generations_by_pk', {}).get('generated_images', [])
                    if imagini:
                        url_imagine_finala = imagini[0].get('url')
                        print("    ✅ [Leonardo API] Imagine gata! Descărcăm pe laptop...")
                        
                        # 3. Descărcăm fișierul fizic
                        img_data = requests.get(url_imagine_finala).content
                        cale_fisier = os.path.join(folder_salvare, f"scena_{index}.jpg")
                        with open(cale_fisier, 'wb') as f:
                            f.write(img_data)
                        return cale_fisier
                elif status == 'FAILED':
                    print("    ❌ Generarea a eșuat pe serverul Leonardo.")
                    return None
                    
        print("    ⚠️ Timeout la așteptarea imaginii.")
        return None
        
    except Exception as e:
        print(f"    ❌ Eroare conexiune: {e}")
        return None

def descarca_pentru_scenariu(scenariu_json, tip="video"):
    if not scenariu_json:
        return []

    print("\n📸 Începem producția de imagini (PREMIUM - LEONARDO AI)...")
    folder = asigura_folder_temp("temp/imagini_video" if tip == "video" else "temp/imagini_carusel")
    scenariu_actualizat = []
    
    for i, scena in enumerate(scenariu_json):
        img_prompt = scena.get("img_prompt", "")
        print(f"  -> Procesăm scena {i+1}/{len(scenariu_json)}...")
        
        cale_locala = descarca_imagine_leonardo(img_prompt, i, folder)
        
        if cale_locala:
            scena["cale_imagine"] = cale_locala
            scenariu_actualizat.append(scena)
        else:
            print(f"  -> ⚠️ Am ratat imaginea {i+1}, o excludem.")

    print(f"✅ Descărcare completă! ({len(scenariu_actualizat)} capodopere salvate)")
    return scenariu_actualizat