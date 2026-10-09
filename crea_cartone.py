import os
import asyncio
import urllib.parse
import urllib.request
import edge_tts
from moviepy import VideoFileClip, AudioFileClip
from gradio_client import Client

# ==========================================
# 1. GENERAZIONE STORIA (POLLINATIONS)
# ==========================================
def genera_sceneggiatura():
    print("Scrittura della sceneggiatura...")
    prompt = "Scrivi in inglese un breve prompt descrittivo (massimo 15 parole) per generare un video 3D stile Disney Pixar di un cucciolo di cane felice che corre in un prato."
    url = "https://text.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        testo_storia = response.read().decode('utf-8').strip()
        
    print("Prompt Video Generato:\n", testo_storia)
    return testo_storia

# ==========================================
# 2. GENERAZIONE DOPPIAGGIO (EDGE TTS)
# ==========================================
async def crea_doppiaggio(testo_italiano, file_audio_output="voce_narrante.mp3"):
    print("Generazione voce in corso...")
    # Qui impostiamo la battuta che dirà il personaggio in italiano
    battuta = "Evviva! Che bella giornata per correre nel prato!"
    voce = "it-IT-DiegoNeural"
    comunica = edge_tts.Communicate(battuta, voce)
    await comunica.save(file_audio_output)
    print(f"Audio salvato come {file_audio_output}")

# ==========================================
# 3. GENERAZIONE VIDEO PRO (HUGGING FACE)
# ==========================================
def genera_video_animato(prompt_video, file_video_output="scena_video.mp4"):
    print("Connessione ai server di Hugging Face per l'animazione video...")
    print("NOTA: Questo passaggio può richiedere 5-15 minuti per via delle code pubbliche.")
    
    # Ci colleghiamo a uno "Space" pubblico che usa modelli video avanzati
    client = Client("multimodalart/zeroscope-v2") 
    
    try:
        # Inviamo il comando ai server pubblici
        result = client.predict(
            prompt_video,
            "low quality, distorted, bad animation", # Prompt negativo (cose da evitare)
            api_name="/infer"
        )
        # Il server ci restituisce il percorso del video generato
        percorso_scaricato = result[0]
        
        # Rinominiamo e spostiamo il video nella nostra cartella
        os.rename(percorso_scaricato, file_video_output)
        print("Video animato scaricato con successo!")
        
    except Exception as e:
        print(f"Errore durante la generazione video: {e}")
        print("Il server pubblico potrebbe essere troppo occupato. Riproverà domani.")

# ==========================================
# 4. MONTAGGIO FINALE (MOVIEPY)
# ==========================================
def monta_video_e_audio(file_video, file_audio, file_finale="short_finito.mp4"):
    print("Montaggio video in corso...")
    if os.path.exists(file_video) and os.path.exists(file_audio):
        video = VideoFileClip(file_video)
        audio = AudioFileClip(file_audio)
        
        # Uniamo i due file
        video_finale = video.with_audio(audio)
        video_finale.write_videofile(file_finale, codec="libx264", audio_codec="aac", fps=24)
        print(f"SUCCESSO! Il tuo cartone animato PRO è pronto: {file_finale}")

# ==========================================
# IL NUOVO "MOTORE" PRO
# ==========================================
async def avvia_fabbrica():
    print("--- AVVIO FABBRICA CARTONI ANIMATI PRO ---")
    prompt_inglese = genera_sceneggiatura()
    await crea_doppiaggio(prompt_inglese, "voce_narrante.mp3")
    genera_video_animato(prompt_inglese, "scena_video.mp4")
    monta_video_e_audio("scena_video.mp4", "voce_narrante.mp3", "short_finito.mp4")

if __name__ == "__main__":
    asyncio.run(avvia_fabbrica())
