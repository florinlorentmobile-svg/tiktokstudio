import os
import time
import random
from dotenv import load_dotenv

# Citim cheia din .env-ul tău în siguranță
load_dotenv()
CHEIE_GEMINI = os.getenv("GEMINI_API_KEY")

if not CHEIE_GEMINI:
    print("❌ EROARE: Nu găsesc GEMINI_API_KEY în fișierul .env!")
    exit()

from module import m1_generare_text as text_ai
from module import m2_media_foto as foto_ai
from module import m3_media_audio as audio_ai
from module import m4_randare_video as video_ai
from module import m5_generator_carusel as carusel_maker

# TEME SEPARATE
TEME_VIDEO = ["Cultură generală: Invenții care au schimbat lumea", "Cultură generală: Secretele țărilor de pe glob", "Cultură generală: Curiozități uimitoare despre corpul uman", "Mistere istorice neelucidate", "Curiozități despre univers", "Fenomene inexplicabile din natură", "Mistere istorice neelucidate și conspirații", "Curiozități bizare despre spațiu și univers", "Fenomene inexplicabile din natură", "Secrete și curiozități despre corpul și creierul uman", "Invenții antice pe care știința modernă nu le poate explica", "Civilizații pierdute și secretele lor", "Locuri de pe Pământ unde legile fizicii nu se aplică", "Animale ciudate și comportamente bizare din regnul animal", "Mistere nerezolvate ale istoriei și arheologiei", "Curiozități despre spațiu și fenomene cosmice inexplicabile", "Secrete și curiozități despre corpul uman și bolile misterioase", "Invenții futuriste care par desprinse din science fiction", "Civilizații avansate care au dispărut fără urmă", "Locuri de pe Pământ cu fenomene paranormale sau inexplicabile", "Animale preistorice și creaturi mitologice care ar putea fi reale", "Mistere nerezolvate ale istoriei și arheologiei", "Curiozități despre spațiu și fenomene cosmice inexplicabile", "Secrete și curiozități despre corpul uman și bolile misterioase", "Invenții futuriste care par desprinse din science fiction", "Civilizații avansate care au dispărut fără urmă", "Locuri de pe Pământ cu fenomene paranormale sau inexplicabile", "Animale preistorice și creaturi mitologice care ar putea fi reale", "Curiozități despre spațiu și fenomene cosmice inexplicabile", "Secrete și curiozități despre corpul uman și bolile misterioase", "Invenții futuriste care par desprinse din science fiction", "Civilizații avansate care au dispărut fără urmă", "Locuri de pe Pământ cu fenomene paranormale sau inexplicabile", "Animale preistorice și creaturi mitologice care ar putea fi reale"]
TEME_POZE = ["Cultură generală: Invenții care au schimbat lumea", "Cultură generală: Secretele țărilor de pe glob", "Cultură generală: Curiozități uimitoare despre corpul uman", "Mistere istorice neelucidate", "Curiozități despre univers", "Fenomene inexplicabile din natură", "Mistere istorice neelucidate și conspirații", "Curiozități bizare despre spațiu și univers", "Fenomene inexplicabile din natură", "Secrete și curiozități despre corpul și creierul uman", "Invenții antice pe care știința modernă nu le poate explica", "Civilizații pierdute și secretele lor", "Locuri de pe Pământ unde legile fizicii nu se aplică", "Animale ciudate și comportamente bizare din regnul animal", "Mistere nerezolvate ale istoriei și arheologiei", "Curiozități despre spațiu și fenomene cosmice inexplicabile", "Secrete și curiozități despre corpul uman și bolile misterioase", "Invenții futuriste care par desprinse din science fiction", "Civilizații avansate care au dispărut fără urmă", "Locuri de pe Pământ cu fenomene paranormale sau inexplicabile", "Animale preistorice și creaturi mitologice care ar putea fi reale", "Mistere nerezolvate ale istoriei și arheologiei", "Curiozități despre spațiu și fenomene cosmice inexplicabile", "Secrete și curiozități despre corpul uman și bolile misterioase", "Invenții futuriste care par desprinse din science fiction", "Civilizații avansate care au dispărut fără urmă", "Locuri de pe Pământ cu fenomene paranormale sau inexplicabile", "Animale preistorice și creaturi mitologice care ar putea fi reale", "Curiozități despre spațiu și fenomene cosmice inexplicabile", "Secrete și curiozități despre corpul uman și bolile misterioase", "Invenții futuriste care par desprinse din science fiction", "Civilizații avansate care au dispărut fără urmă", "Locuri de pe Pământ cu fenomene paranormale sau inexplicabile", "Animale preistorice și creaturi mitologice care ar putea fi reale"]

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print(" 🎬 TIKTOK STUDIO - GENERATOR DUAL (VIDEO / POZE) 🎬 ")
    print("="*60)
    
    # 1. Selectie format
    print("\n[1] 🎥 Video (Poze rulate + Sunet + Subtitrare galbenă)")
    print("[2] 📸 Set de Poze (Text font special + Steag/Logo pentru carusel)")
    format_ales = input("👉 Ce dorești să generezi? (1/2): ")
    if format_ales not in ['1', '2']: return
    tip_continut = "video" if format_ales == '1' else "poze"

    # 2. Selectie limba
    print("\n[1] Română (RO)  |  [2] Engleză (EN)")
    limba = "EN" if input("👉 Alege limba subtitrării/textului (1/2): ") == '2' else "RO"

    # 3. Selectie numar bucati
    unitate = "scene" if tip_continut == "video" else "fotografii"
    try:
        numar = int(input(f"\n👉 Câte {unitate} să aibă proiectul?: "))
    except ValueError:
        numar = 3 # Default

    # Randomizare tema in functie de selectie (punctul 4.2)
    lista_teme = TEME_VIDEO if tip_continut == "video" else TEME_POZE
    tema_aleasa = random.choice(lista_teme)
    
    print(f"\n🚀 START -> Format: {tip_continut.upper()} | Limba: {limba} | Cantitate: {numar} | Tema: '{tema_aleasa}'\n" + "-"*40)
    
    # Executia modulelor
    scenariu = text_ai.genereaza_poveste(tema_aleasa, numar, limba, CHEIE_GEMINI, tip_continut)
    if not scenariu: return
        
    scenariu_cu_poze = foto_ai.descarca_pentru_scenariu(scenariu, tip=tip_continut)
    
    # Punctele 4.1 si 4.2: Ramificare clara
    if tip_continut == "video":
        scenariu_complet = audio_ai.genereaza_voci(scenariu_cu_poze, limba)
        video_ai.asambleaza_final(scenariu_complet, f"Video_{limba}_{int(time.time())}.mp4")
    else:
        carusel_maker.genereaza_slide_uri(scenariu_cu_poze, limba)

if __name__ == "__main__":
    main()