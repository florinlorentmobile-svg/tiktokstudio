import json
import time
from google import genai

def genereaza_poveste(tema, numar_scene, limba, cheie_api, format_ales="video"):
    client = genai.Client(api_key=cheie_api)
    limba_text = "ROMÂNĂ" if limba == "RO" else "ENGLEZĂ"

    if format_ales == "video":
        prompt_sistem = f"""
        Ești un regizor de documentare. Creează un scenariu din {numar_scene} scene despre: "{tema}".
        Scrie narațiunea strict în limba {limba_text}. Scena 1 TREBUIE să fie un Hook șocant.
        Imaginea (img_prompt) în ENGLEZĂ. Stil: Photorealistic, cinematic, 8k --no sci-fi, no text. FĂRĂ logo-uri sau steaguri.
        Returnează strict JSON:
        [ {{ "text": "...", "img_prompt": "..." }} ]
        """
    else:
        prompt_sistem = f"""
        Ești un expert în cultură generală. Generează {numar_scene} curiozități despre: "{tema}".
        
        REGULI STRICTE:
        1. "text": Curiozitatea TREBUIE scrisă strict în limba {limba_text}, foarte scurtă (1-2 propoziții).
        2. "img_prompt": Descrierea imaginii TREBUIE să fie în ENGLEZĂ, fotorealist, extrem de detaliat. FĂRĂ TEXT.
        3. "emoji": Acest câmp este OBLIGATORIU. Trebuie să conțină EXACT UN EMOJI (un steag 🇮🇸, un animal 🐘 sau un obiect 🌋) relevant pentru curiozitate. NU lăsa câmpul gol!
        
        Returnează STRICT JSON valid în acest format:
        [ 
          {{ 
            "text": "Aici pui textul în {limba_text}...", 
            "img_prompt": "Photorealistic description in English...", 
            "emoji": "🚀" 
          }} 
        ]
        """

    # --- SISTEM DE AUTO-REÎNCERCARE (RETRY MECHANISM) ---
    max_incercari = 3
    secunde_asteptare = 5

    for incercare in range(max_incercari):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt_sistem
            )
            
            rezultat_curat = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(rezultat_curat)
            
        except Exception as e:
            # Dacă este eroare de la server aglomerat (503), mai încercăm
            if "503" in str(e) or "UNAVAILABLE" in str(e).upper():
                print(f"⚠️ Serverul Gemini este aglomerat (Încercarea {incercare + 1}/{max_incercari}). Reîncercăm în {secunde_asteptare} secunde...")
                time.sleep(secunde_asteptare)
                secunde_asteptare *= 2 # Mărim timpul de așteptare progresiv (ex: 5s -> 10s)
            else:
                # Dacă e alt tip de eroare, o afișăm direct
                print(f"❌ Eroare generare text: {e}")
                return []
                
    print("❌ Am epuizat toate cele 3 încercări, serverul Google refuză conexiunea momentan.")
    return []