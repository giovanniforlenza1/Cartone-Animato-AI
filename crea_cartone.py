import os
import asyncio
import json
import edge_tts
from moviepy import VideoFileClip, AudioFileClip
from google import genai
from gradio_client import Client

# ==========================================
# 1. CONFIGURAZIONE CHIAVI
# ==========================================
CHIAVE_API_GOOGLE = os.getenv("LA_MIA_CHIAVE")
TOKEN_HF = os.getenv("HF_TOKEN")

client_gemini = genai.Client(api_key=CHIAVE_API_GOOGLE)

# ==========================================
# 2. SHOWRUNNER AI (GEMINI)
# ==========================================
def genera_episodio():
    print("Gemini sta scrivendo il nuovo episodio di Pip...")
    prompt_showrunner = """You are the showrunner of a 3D Pixar-style educational animated series for preschoolers. 
The main character is Pip, a cute and extremely fluffy red panda wearing a small yellow scarf. 
Pip explores the world and learns how to manage emotions (like frustration, fear, or excitement) with a gentle, positive approach. 
Write a new 15-second episode for today. 
Output ONLY a valid JSON object with two keys:
"narration": "A short, sweet voiceover script (max 20 words) in English.",
"video_prompt": "A highly detailed prompt (max 20 words) for a text-to-video AI model, describing Pip in 3D Pixar style doing the action, continuous smooth shot, bright colors."
Do not add any markdown formatting, just the raw JSON."""

    response = client_gemini.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt_showrunner
    )
    
    # Pulizia del testo per assicurarsi che Python legga bene il formato JSON
    testo_pulito = response.text.strip().replace('```json', '').replace('```', '')
    dati_episodio = json.loads(testo_pulito)
    
    print("Sceneggiatura generata:")
    print("- Voce narrante:", dati_episodio["narration"])
    print("- Direzione video:", dati_episodio["video_prompt"])
    
    return dati_episodio

# ==========================================
# 3. GENERAZIONE DOPPIAGGIO (EDGE TTS)
# ==========================================
async def crea_doppiaggio(testo_inglese, file_audio_output="voce_narrante.mp3"):
    print("Registrazione della voce in corso (Inglese)...")
    # Voce femminile dolce e rassicurante (nativa americana)
    voce = "en-US-AnaNeural" 
    comunica = edge_tts.Communicate(testo_inglese, voce)
    await comunica.save(file_audio_output)
    print(f"Audio salvato come {file_audio_output}")

# ==========================================
# 4. GENERAZIONE VIDEO PRO (HUGGING FACE)
# ==========================================
def genera_video_animato(prompt_video, file_video_output="scena_video.mp4"):
    print("Richiesta video ai server Hugging Face (ModelScope)...")
    try:
        # Abbiamo corretto il parametro in "token="
        client_hf = Client("damo-vilab/modelscope-text-to-video-synthesis", token=TOKEN_HF) 
        
        result = client_hf.predict(
            prompt_video,
            "low quality, distorted, bad animation, text, watermark, bad proportions", # Prompt negativo
            api_name="/infer"
        )
        
        percorso_scaricato = result[0]
        os.rename(percorso_scaricato, file_video_output)
        print("Video animato scaricato con successo!")
        
    except Exception as e:
        print(f"Errore durante la generazione video: {e}")

# ==========================================
# 5. MONTAGGIO FINALE (MOVIEPY)
# ==========================================
def monta_video_e_audio(file_video, file_audio, file_finale="short_finito.mp4"):
    print("Montaggio finale in corso...")
    if os.path.exists(file_video) and os.path.exists(file_audio):
        video = VideoFileClip(file_video)
        audio = AudioFileClip(file_audio)
        
        # Sovrappone l'audio al video generato
        video_finale = video.with_audio(audio)
        video_finale.write_videofile(file_finale, codec="libx264", audio_codec="aac", fps=24)
        print(f"SUCCESSO! L'episodio di Pip è pronto: {file_finale}")

# ==========================================
# IL MOTORE CENTRALE
# ==========================================
async def avvia_fabbrica():
    print("--- AVVIO FABBRICA: PIP IL PANDA MINORE ---")
    
    # 1. Gemini inventa la puntata
    episodio = genera_episodio()
    
    # 2. Creiamo l'audio in inglese
    await crea_doppiaggio(episodio["narration"], "voce_narrante.mp3")
    
    # 3. Creiamo il video 3D
    genera_video_animato(episodio["video_prompt"], "scena_video.mp4")
    
    # 4. Montiamo il tutto
    monta_video_e_audio("scena_video.mp4", "voce_narrante.mp3", "short_finito.mp4")

if __name__ == "__main__":
    asyncio.run(avvia_fabbrica())
