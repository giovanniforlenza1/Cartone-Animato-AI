import os
import asyncio
import urllib.parse
import urllib.request
import edge_tts
from moviepy import ImageClip, AudioFileClip

# ==========================================
# 1. GENERAZIONE TESTO (POLLINATIONS AI)
# ==========================================
def genera_sceneggiatura():
    print("Scrittura della storia in corso (senza API Key)...")
    prompt = "Scrivi 3 brevi frasi in italiano per un cartone animato per bambini. Protagonista: un tenero cucciolo di cane esploratore."
    url = "https://text.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
    
    # Richiesta diretta al server gratuito
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        testo_storia = response.read().decode('utf-8').strip()
        
    print("Storia generata:\n", testo_storia)
    return testo_storia

# ==========================================
# 2. GENERAZIONE DOPPIAGGIO (EDGE TTS)
# ==========================================
async def crea_doppiaggio(testo, file_audio_output="voce_narrante.mp3"):
    print("Generazione del doppiaggio realistico...")
    voce = "it-IT-DiegoNeural"
    comunica = edge_tts.Communicate(testo, voce)
    await comunica.save(file_audio_output)
    print(f"Audio salvato come {file_audio_output}")

# ==========================================
# 3. GENERAZIONE IMMAGINE (POLLINATIONS AI)
# ==========================================
def genera_immagine_disney(file_immagine_output="scena.jpg"):
    print("Generazione dell'illustrazione in corso...")
    # Puoi cambiare questo prompt per variare le scene!
    prompt_immagine = "3D animation Disney Pixar style, vibrant colors, a cute happy puppy exploring a magical forest, vertical format"
    url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt_immagine) + "?width=1080&height=1920&nologo=true"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        with open(file_immagine_output, "wb") as f:
            f.write(response.read())
            
    print("Immagine scaricata!")
    return file_immagine_output

# ==========================================
# 4. MONTAGGIO FINALE (MOVIEPY)
# ==========================================
def monta_video_e_audio(file_immagine, file_audio, file_finale="short_finito.mp4"):
    print("Montaggio video in corso...")
    if os.path.exists(file_immagine) and os.path.exists(file_audio):
        audio = AudioFileClip(file_audio)
        
        # Trasforma l'immagine in un video lungo esattamente quanto l'audio
        video = ImageClip(file_immagine).with_duration(audio.duration)
        video_finale = video.with_audio(audio)
        
        # Esporta il file mp4
        video_finale.write_videofile(file_finale, codec="libx264", audio_codec="aac", fps=24)
        print(f"SUCCESSO! Il tuo cartone animato è pronto: {file_finale}")

# ==========================================
# IL "MOTORE"
# ==========================================
async def avvia_fabbrica():
    print("--- AVVIO AUTOMAZIONE CARTONE ANIMATO (FREE TIER) ---")
    storia = genera_sceneggiatura()
    await crea_doppiaggio(storia, "voce_narrante.mp3")
    genera_immagine_disney("scena.jpg")
    monta_video_e_audio("scena.jpg", "voce_narrante.mp3", "short_finito.mp4")

if __name__ == "__main__":
    asyncio.run(avvia_fabbrica())
