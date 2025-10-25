from __future__ import annotations

import argparse
import asyncio
import edge_tts
import pygame
import tempfile
import os
import sys
import aiohttp
import sounddevice as sd
import numpy as np
from io import BytesIO
from piper.voice import PiperVoice
from piper.config import SynthesisConfig

def get_base_path():
    """Obtém o caminho base para os recursos, compatível com PyInstaller."""
    if getattr(sys, 'frozen', False):
        # Se a aplicação estiver "congelada" (executável), o caminho é o diretório temporário _MEIPASS
        base_path = sys._MEIPASS
        # Configurar variável de ambiente para espeak-ng
        espeak_data = os.path.join(base_path, 'piper', 'espeak-ng-data')
        if os.path.exists(espeak_data):
            os.environ['ESPEAK_DATA'] = espeak_data
            print(f"ESPEAK_DATA configurado para: {espeak_data}")
        return base_path
    else:
        # Se estiver a ser executado como um script normal
        return os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(get_base_path(), "models")
LOCAL_VOICE_MODEL = os.path.join(MODELS_DIR, "pt_PT-tugão-medium.onnx")

# Variáveis globais para armazenar os modelos de voz carregados e evitar recarregamentos.
_voice_pt: PiperVoice | None = None

def _initialize_offline_voices():
    """Carrega o modelo de voz do Piper na memória. Chamado uma vez no início."""
    global _voice_pt
    try:
        if os.path.exists(LOCAL_VOICE_MODEL):
            print("A carregar modelo de voz offline (Português)...")

            if getattr(sys, 'frozen', False):
                # A aplicação está compilada, pode ser necessário indicar o caminho dos dados do espeak-ng
                # Porém, o piper-tts geralmente consegue localizá-los automaticamente
                _voice_pt = PiperVoice.load(LOCAL_VOICE_MODEL)
            else:
                # A aplicação não está compilada
                _voice_pt = PiperVoice.load(LOCAL_VOICE_MODEL)
        else:
            print(f"Aviso: Modelo de voz em Português não encontrado em {LOCAL_VOICE_MODEL}", file=sys.stderr)

    except Exception as e:
        print(f"Erro ao inicializar o modelo de voz offline: {e}", file=sys.stderr)
        _voice_pt = None  # Garante que o modelo não será usado se o carregamento falhar

def _play_offline_fallback(text: str, error_message: str):
    """Handles the offline TTS fallback using piper-tts.
    
    Quando há falha na voz online, reproduz a voz offline mais lentamente
    para melhor compreensão do fallback.
    """
    print(f"Erro na voz online: {error_message}. A usar o fallback offline.")
    try:
        if not _voice_pt:
            print("Erro: O modelo de voz offline não está carregado. Não é possível usar o fallback.", file=sys.stderr)
            return

        warning_message = "A voz neural não está disponível. A utilizar uma voz padrão para a reprodução."
        print(f"A reproduzir aviso: {warning_message}")
        
        # Reproduzir aviso com velocidade reduzida (0.7x)
        _synthesize_and_play(_voice_pt, warning_message, speed=0.7)
        # Reproduzir texto com velocidade reduzida (0.7x)
        _synthesize_and_play(_voice_pt, text, speed=0.7)

    except Exception as e2:
        print(f"Erro catastrófico no fallback offline: {e2}")

def _synthesize_and_play(voice: PiperVoice, text: str, speed: float = 0.9):
    """Sintetiza o texto com a voz fornecida e reproduz o áudio.
    
    Args:
        voice: Objeto PiperVoice para síntese
        text: Texto a sintetizar
        speed: Velocidade de fala (0.5 = mais lento, 1.0 = normal, 2.0 = mais rápido)
    """
    if not voice:
        print(f"Aviso: Nenhuma voz fornecida para o texto: '{text}'", file=sys.stderr)
        return
    
    print(f"A reproduzir offline: {text} (velocidade: {speed}x)")
    samplerate = voice.config.sample_rate

    # Criar configuração de síntese com controle de velocidade
    # length_scale: < 1 = mais rápido, > 1 = mais lento (inverso da velocidade)
    length_scale = 1.0 / speed if speed != 0 else 1.0
    syn_config = SynthesisConfig(length_scale=length_scale)
    
    audio_bytes = b""
    for chunk in voice.synthesize(text, syn_config=syn_config):
        audio_bytes += chunk.audio_int16_bytes

    if not audio_bytes:
        print("Aviso: A síntese de voz não produziu áudio.", file=sys.stderr)
        return

    audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
    sd.play(audio_data, samplerate)
    sd.wait()

def play_local(text: str, speed: float = 0.9):
    """Sintetiza e reproduz o texto usando a voz offline local.
    
    Args:
        text: Texto a sintetizar
        speed: Velocidade de fala (0.5 = mais lento, 1.0 = normal, 2.0 = mais rápido)
    """
    print("A usar a voz offline (local)...")
    if not _voice_pt:
        print("Erro: O modelo de voz offline não está carregado.", file=sys.stderr)
        return
    try:
        _synthesize_and_play(_voice_pt, text, speed=speed)
    except Exception as e:
        print(f"Erro ao reproduzir a voz offline: {e}", file=sys.stderr)

async def generate_and_play_audio(text, voice):
    """Gera áudio online com edge-tts e reproduz.
    
    Args:
        text: Texto a sintetizar
        voice: Identificador da voz
    """
    try:
        print("A usar a voz online (edge-tts)...")
        
        communicate = edge_tts.Communicate(text, voice)
        
        # Acumular os chunks de áudio em memória com BytesIO
        audio_buffer = BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])

        audio_buffer.seek(0)  # Reposicionar o cursor ao início
        
        if audio_buffer.tell() == 0 and audio_buffer.getbuffer().nbytes == 0:
            raise OSError("Nenhum áudio foi gerado pelo edge-tts")

        # Reproduzir diretamente da memória (sem ficheiro temporário)
        try:
            sound = pygame.mixer.Sound(audio_buffer)
            sound.play()

            while pygame.mixer.get_busy():
                await asyncio.sleep(0.1)
        except Exception as e:
            # Se pygame.mixer.Sound não aceitar BytesIO, usar ficheiro temporário
            print(f"Aviso: A reprodução direto da memória falhou, a usar ficheiro temporário: {e}")
            temp_fd, temp_filename = tempfile.mkstemp(suffix=".mp3")
            try:
                os.write(temp_fd, audio_buffer.getvalue())
                os.close(temp_fd)

                sound = pygame.mixer.Sound(temp_filename)
                sound.play()

                while pygame.mixer.get_busy():
                    await asyncio.sleep(0.1)
            finally:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

    except (aiohttp.ClientError, OSError) as e:
        # Em caso de erro, reproduz o fallback offline com velocidade reduzida
        _play_offline_fallback(text, str(e))

def main():
    parser = argparse.ArgumentParser(description="Conversor de Texto para Fala")
    parser.add_argument("text", type=str, help="Texto a ser convertido.")
    parser.add_argument("--voice", type=str, default="pt-PT-RaquelNeural", help="Voz para síntese.")
    parser.add_argument("--local", action="store_true", help="Força o uso da voz local (offline).")
    parser.add_argument("--speed", type=float, default=0.9, 
                        help="Velocidade de fala (apenas para voz local). (0.5=mais lento, 1.0=normal, 2.0=mais rápido). Padrão: 0.9")
    args = parser.parse_args()

    if args.local:
        _initialize_offline_voices()
        play_local(args.text, speed=args.speed)
    else:
        pygame.mixer.init()
        _initialize_offline_voices() # Necessário para o fallback
        try:
            asyncio.run(generate_and_play_audio(args.text, args.voice))
        finally:
            pygame.quit()

if __name__ == "__main__":
    main()