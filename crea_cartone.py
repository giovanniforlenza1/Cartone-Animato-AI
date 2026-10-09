import os
import asyncio
import json
import urllib.parse
import urllib.request
import edge_tts
from moviepy import VideoFileClip, AudioFileClip
from gradio_client import Client

# ==========================================
# 1. CONFIGURAZIONE CHIAVI
# ==========================================
# Google rimosso. Usiamo SOLO il token di Hugging Face.
TOKEN_HF = os.getenv("HF_TOKEN")

# ==========================================
# 2. SHOWRUNNER AI (100% GRATIS VIA POLLINATIONS)
# ==========================================
def genera_episodio():
    print("Scrittura del nuovo episodio di Pip (via AI gratuita)...")
    prompt_showrunner = """You are the showrunner of a 3D Pixar-style educational animated series for preschoolers. 
The main character is Pip, a cute and extremely fluffy red panda wearing a small yellow scarf. 
Output ONLY a JSON object with two keys: "narration" (voiceover max 15 words) and "video_prompt" (visual description max 20 words, continuous smooth shot, bright colors). No markdown, just JSON."""
    
    url = "https://text.pollinations.ai/prompt/" + urllib.parse.quote(prompt_showrunner)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            testo_pulito = response.read().decode('utf-8').strip()
            
        # Pulizia per evitare errori di lettura del formato JSON
        testo_pulito = testo_pulito.replace('```json', '').replace('```', '').strip()
        dati_episodio = json.loads(testo_pulito)
        
        print("Sceneggiatura generata:")
        print("- Voce narrante:", dati_episodio["narration"])
        print("- Direzione video:", dati_episodio["video_prompt"])
        return dati_episodio
        
    except Exception as e:
        print(f"Errore lettura testo: {e}. Uso episodio di backup.")
        # Se il server gratuito fa i capricci, abbiamo un episodio di sicurezza!
        return {
            "narration": "Pip is very happy today. Let's go explore the magical forest together!",
            "video_prompt": "3D Pixar style, cute fluffy red panda with yellow scarf walking happily in a bright green forest, smooth shot"
        }

# ==========================================
# 3. GENERAZIONE DOPPIAGGIO (EDGE TTS)
# ==========================================
async def crea_doppiaggio(testo_inglese, file_audio_output="voce_narrante.mp3"):
    print("Registrazione della voce in corso (Inglese)...")
    voce = "en-US-AnaNeural" # Voce femminile dolce americana
    comunica = edge_tts.Communicate(testo_inglese, voce)
    await comunica.save(file_audio_output)
    print(f"Audio salvato come {file_audio_output}")

# ==========================================
# 4. GENERAZIONE VIDEO PRO (HUGGING FACE)
# ==========================================
def genera_video_animato(prompt_video, file_video_output="scena_video.mp4"):
    print("Richiesta video ai server Hugging Face (ModelScope)...")
    try:
        client_hf = Client("damo-vilab/modelscope-text-to-video-synthesis", token=TOKEN_HF) 
        
        result = client_hf.predict(
            prompt_video,
            "low quality, distorted, bad animation, text, watermark, bad proportions",
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
        
        video_finale = video.with_audio(audio)
        video_finale.write_videofile(file_finale, codec="libx264", audio_codec="aac", fps=24)
        print(f"SUCCESSO! L'episodio di Pip è pronto: {file_finale}")
    else:
        print("Errore nel montaggio: mancano i file sorgente.")

# ==========================================
# IL MOTORE CENTRALE
# ==========================================
async def avvia_fabbrica():
    print("--- AVVIO FABBRICA: PIP IL PANDA MINORE ---")
    episodio = genera_episodio()
    await crea_doppiaggio(episodio["narration"], "voce_narrante.mp3")
    genera_video_animato(episodio["video_prompt"], "scena_video.mp4")
    monta_video_e_audio("scena_video.mp4", "voce_narrante.mp3", "short_finito.mp4")

if __name__ == "__main__":
    asyncio.run(avvia_fabbrica())
