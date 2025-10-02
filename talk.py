import argparse
import asyncio
import edge_tts
import pygame
import tempfile
import os
import pyttsx3
import sys
import aiohttp

def _play_offline_fallback(text: str, error_message: str):
    """Handles the offline TTS fallback using pyttsx3."""
    print(f"Erro na voz online: {error_message}. A usar o fallback offline.")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)

        # Tenta encontrar uma voz em inglês para o aviso, senão usa a default
        try:
            voices = engine.getProperty('voices')
            for v in voices:
                if "en-US" in v.id:
                    engine.setProperty('voice', v.id)
                    break
        except RuntimeError:
            print("Aviso: Não foi possível obter as vozes do sistema. A usar a voz padrão.")

        warning_message = "The neural voice is not available. Using a standard voice for playback."
        print(f"A reproduzir aviso: {warning_message}")
        engine.say(warning_message)
        engine.runAndWait()

        # Idealmente, aqui deveria voltar para a voz PT, se disponível, para o texto original.
        # Como o pyttsx3 pode não ter vozes PT por defeito, mantemos a voz selecionada.
        print(f"A reproduzir texto original: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e2:
        print(f"Erro catastrófico no fallback offline: {e2}")
        # Em vez de SystemExit, podemos apenas notificar o erro.
        # raise SystemExit(1)

def get_base_path():
    """Obtém o caminho base para o executável ou script."""
    if getattr(sys, 'frozen', False):
        # Se estiver a correr como um executável PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Se estiver a correr como um script normal
        return os.path.abspath(".")

async def generate_and_play_audio(text, voice):
    # Criar um nome de ficheiro temporário único
    temp_fd, temp_filename = tempfile.mkstemp(suffix=".mp3", dir=get_base_path())
    os.close(temp_fd)  # Fechar o manipulador de ficheiro, precisamos apenas do nome

    try:
        print("A usar a voz online (edge-tts)...")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_filename)

        sound = pygame.mixer.Sound(temp_filename)
        sound.play()

        while pygame.mixer.get_busy():
            await asyncio.sleep(0.1)

    except (aiohttp.ClientError, OSError) as e:
        _play_offline_fallback(text, str(e))
    finally:
        # Garantir que o ficheiro temporário é sempre apagado
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

def main():
    pygame.mixer.init()
    parser = argparse.ArgumentParser(description="Conversor de Texto para Fala")
    parser.add_argument("text", type=str, help="Texto a ser convertido.")
    parser.add_argument("--voice", type=str, default="pt-PT-RaquelNeural", help="Voz para síntese.")
    args = parser.parse_args()

    asyncio.run(generate_and_play_audio(args.text, args.voice))

    pygame.quit()

if __name__ == "__main__":
    main()