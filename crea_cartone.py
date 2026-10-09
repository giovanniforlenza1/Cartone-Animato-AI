import os
import asyncio
import base64
import edge_tts
from moviepy import VideoFileClip, AudioFileClip
from google import genai

# ==========================================
# 1. CONFIGURAZIONE E CHIAVI 
# ==========================================
CHIAVE_API_GOOGLE = os.getenv("LA_MIA_CHIAVE")
client = genai.Client(api_key=CHIAVE_API_GOOGLE)

# ==========================================
# 2. GENERAZIONE STORIA (TESTO)
# ==========================================
def genera_sceneggiatura():
    print("Scrittura della storia in corso...")
    # Usiamo il metodo corretto per la generazione di testo con il nuovo client
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents="Scrivi un brevissimo testo narrato (massimo 3 frasi, 20 secondi parlati) per un cartone animato per bambini in stile Disney. Argomento: un cucciolo di cane che trova un osso magico."
    )
    testo_storia = response.text.strip()
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
# 4. GENERAZIONE VIDEO OMNI
# ==========================================
def genera_video_disney(scena_testo, file_video_output="scena_video.mp4"):
    print("Generazione video con Gemini Omni in corso...")
    prompt_video = f"Continuous smooth shot. 3D animation Disney Pixar style, vibrant colors. {scena_testo}"
    
    interaction = client.interactions.create(
        model="gemini-omni-1.1-flash",
        input=prompt_video
    )
    
    with open(file_video_output, "wb") as f:
        f.write(base64.b64decode(interaction.output_video.data))
        
    return file_video_output

# ==========================================
# 5. MONTAGGIO FINALE (MOVIEPY)
# ==========================================
def monta_video_e_audio(file_video, file_audio, file_finale="short_finito.mp4"):
    print("Montaggio video in corso...")
    if os.path.exists(file_video) and os.path.exists(file_audio):
        video = VideoFileClip(file_video)
        audio = AudioFileClip(file_audio)
        
        video_finale = video.with_audio(audio)
        video_finale.write_videofile(file_finale, codec="libx264", audio_codec="aac", fps=24)
        print(f"SUCCESSO! Il tuo cartone animato è pronto: {file_finale}")

# ==========================================
# IL "MOTORE"
# ==========================================
async def avvia_fabbrica():
    print("--- AVVIO AUTOMAZIONE CARTONE ANIMATO ---")
    storia = genera_sceneggiatura()
    await crea_doppiaggio(storia, "voce_narrante.mp3")
    genera_video_disney(storia, "scena_video.mp4")
    monta_video_e_audio("scena_video.mp4", "voce_narrante.mp3", "short_finito.mp4")

if __name__ == "__main__":
    asyncio.run(avvia_fabbrica())
