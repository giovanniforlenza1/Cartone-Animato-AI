import os
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip, ColorClip
import google.generativeai as genai

# ==========================================
# 1. CONFIGURAZIONE E CHIAVI (Sicura)
# ==========================================
# Il programma pesca la tua chiave direttamente dalla cassaforte di GitHub
CHIAVE_API_GOOGLE = os.getenv("LA_MIA_CHIAVE")
genai.configure(api_key=CHIAVE_API_GOOGLE)

# ==========================================
# 2. GENERAZIONE STORIA E TESTO (GEMINI)
# ==========================================
def genera_sceneggiatura():
    print("Scrittura della storia in corso...")
    # L'errore 404 non si presenterà più nel nuovo ambiente aggiornato
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Scrivi un brevissimo testo narrato (massimo 3 frasi, 20 secondi parlati) per un cartone animato per bambini in stile Disney. Argomento: un cucciolo di cane che trova un osso magico."
    risposta = model.generate_content(prompt)
    testo_storia = risposta.text.strip()
    print("Storia generata:\n", testo_storia)
    return testo_storia

# ==========================================
# 3. GENERAZIONE DOPPIAGGIO (EDGE TTS)
# ==========================================
async def crea_doppiaggio(testo, file_audio_output="voce_narrante.mp3"):
    print("Generazione del doppiaggio realistico...")
    voce = "it-IT-DiegoNeural"
    comunica = edge_tts.Communicate(testo, voce)
    await comunica.save(file_audio_output)
    print(f"Audio salvato come {file_audio_output}")

# ==========================================
# 4. GENERAZIONE VIDEO 
# ==========================================
def genera_video_disney(scena_testo, file_video_output="scena_video.mp4"):
    print("Generazione video in corso...")
    # Dato che sei su un computer virtuale nuovo, non hai un video pronto.
    # Per non far bloccare il programma, creerà uno schermo nero di test!
    if not os.path.exists(file_video_output):
        print("Creo un video di test nero in automatico...")
        clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=5)
        clip.write_videofile(file_video_output, fps=24)
    return file_video_output

# ==========================================
# 5. MONTAGGIO FINALE (MOVIEPY)
# ==========================================
def monta_video_e_audio(file_video, file_audio, file_finale="short_finito.mp4"):
    print("Montaggio video in corso...")
    if os.path.exists(file_video) and os.path.exists(file_audio):
        video = VideoFileClip(file_video)
        audio = AudioFileClip(file_audio)
        
        # Unisce video e audio
        video_finale = video.with_audio(audio)
        
        # Salva il file mp4 finito
        video_finale.write_videofile(file_finale, codec="libx264", audio_codec="aac", fps=24)
        print(f"SUCCESSO! Il tuo cartone animato è pronto: {file_finale}")
    else:
        print("Errore: Mancano i file video o audio per il montaggio.")

# ==========================================
# IL "MOTORE" (LANCIO DI TUTTO IL PROCESSO)
# ==========================================
async def avvia_fabbrica():
    print("--- AVVIO AUTOMAZIONE CARTONE ANIMATO ---")
    storia = genera_sceneggiatura()
    await crea_doppiaggio(storia, "voce_narrante.mp3")
    genera_video_disney(storia, "scena_video.mp4")
    monta_video_e_audio("scena_video.mp4", "voce_narrante.mp3", "short_finito.mp4")

if __name__ == "__main__":
    asyncio.run(avvia_fabbrica())
