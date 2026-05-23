import os
import asyncio
import edge_tts

def asigura_folder_temp(nume_folder="temp/audio"):
    """Creează folderul pentru fișiere audio dacă nu există."""
    if not os.path.exists(nume_folder):
        os.makedirs(nume_folder)
    return nume_folder

async def genereaza_fisier_audio(text, cale_salvare, voce):
    """Funcția asincronă care comunică cu serverele Microsoft Edge TTS."""
    comunicare = edge_tts.Communicate(text, voce)
    await comunicare.save(cale_salvare)

def genereaza_voci(scenariu_json, limba):
    """
    Primește scenariul generat și creează un fișier mp3 pentru fiecare scenă.
    Returnează scenariul cu căile către fișierele audio locale adăugate.
    """
    if not scenariu_json:
        print("❌ Scenariul este gol, nu avem ce citi.")
        return []

    print("\n🎙️ Începem generarea vocilor sintetice (Text-to-Speech)...")
    folder = asigura_folder_temp()
    
    # Alegem vocea în funcție de limba selectată
    # ro-RO-EmilNeural este o voce masculină excelentă pentru RO
    # en-US-ChristopherNeural este o voce masculină stil documentar pentru EN
    voce_aleasa = "en-US-ChristopherNeural" if limba == "EN" else "ro-RO-EmilNeural"
    
    scenariu_actualizat = []
    
    for i, scena in enumerate(scenariu_json):
        text_narare = scena.get("text", "")
        if not text_narare:
            continue
            
        print(f"  -> Înregistrăm scena {i+1}/{len(scenariu_json)}...")
        
        cale_locala = os.path.join(folder, f"audio_scena_{i}.mp3")
        
        try:
            # edge-tts folosește funcții asincrone, deci trebuie rulate așa
            asyncio.run(genereaza_fisier_audio(text_narare, cale_locala, voce_aleasa))
            
            scena["cale_audio"] = cale_locala
            scenariu_actualizat.append(scena)
            
        except Exception as e:
            print(f"❌ Eroare la generarea vocii pentru scena {i+1}: {e}")
            
    print(f"✅ Voci generate cu succes! ({len(scenariu_actualizat)} fișiere audio salvate)")
    return scenariu_actualizat

# Bloc de testare rapidă
if __name__ == "__main__":
    scenariu_test = [
        {"text": "Acesta este un test de voce pentru documentarul nostru automatizat."},
        {"text": "În Islanda, peisajele sunt absolut fascinante, dar știai că nu există țânțari?"}
    ]
    rezultat = genereaza_voci(scenariu_test, "RO")
    print(rezultat)