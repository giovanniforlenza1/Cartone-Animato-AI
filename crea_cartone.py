import os
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip
import google.generativeai as genai

# ==========================================
# 1. CONFIGURAZIONE E CHIAVI
# ==========================================
# Inserisci qui la tua chiave API di Google
CHIAVE_API_GOOGLE = "LA_MIA_CHIAVE"
genai.configure(api_key=CHIAVE_API_GOOGLE)

# ==========================================
# 2. GENERAZIONE STORIA E TESTO (GEMINI)
# ==========================================
def genera_sceneggiatura():
    print("Scrittura della storia in corso...")
    # Usiamo il modello di testo di Gemini per scrivere la storia
    model = genai.GenerativeModel('gemini-1.5-flash')
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
    # Usa una voce italiana espressiva (it-IT-DiegoNeural o it-IT-ElsaNeural)
    voce = "it-IT-DiegoNeural"
    comunica = edge_tts.Communicate(testo, voce)
    await comunica.save(file_audio_output)
    print(f"Audio salvato come {file_audio_output}")

# ==========================================
# 4. GENERAZIONE VIDEO
# ==========================================
def genera_video_disney(scena_testo, file_video_output="scena_video.mp4"):
    print("Generazione video (Richiesta API)...")
    # Qui andrà integrata la chiamata al modello video specifico di Google 
    # quando avrai sbloccato le tue 3 generazioni video giornaliere via API.
    # Per ora il programma richiede che ci sia un file video di test chiamato "scena_video.mp4"
    # generato manualmente se l'API non è ancora attiva per il tuo account.
    
    if not os.path.exists(file_video_output):
        print(f"ATTENZIONE: Assicurati di avere un file '{file_video_output}' nella cartella per il montaggio.")
    return file_video_output

# ==========================================
# 5. MONTAGGIO FINALE (MOVIEPY)
# ==========================================
def monta_video_e_audio(file_video, file_audio, file_finale="short_finito.mp4"):
    print("Montaggio video in corso...")
    if os.path.exists(file_video) and os.path.exists(file_audio):
        video = VideoFileClip(file_video)
        audio = AudioFileClip(file_audio)
        
        # Taglia o adatta i tempi e imposta l'audio sotto il video
        video_finale = video.set_audio(audio)
        # Salva il file mp4 finito
        video_finale.write_videofile(file_finale, codec="libx264", audio_codec="aac")
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
    
    # Genera/Scarica la clip video
    genera_video_disney(storia, "scena_video.mp4")
    
    # Monta il prodotto finale
    monta_video_e_audio("scena_video.mp4", "voce_narrante.mp3", "short_finito.mp4")

# Comando per avviare il programma
if __name__ == "__main__":
    asyncio.run(avvia_fabbrica())
