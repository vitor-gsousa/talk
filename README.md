# Talk - Conversor de Texto para Voz (TTS) via Linha de Comandos

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Powered by edge-tts](https://img.shields.io/badge/powered%20by-edge--tts-brightgreen)](https://github.com/rany2/edge-tts)

`Talk` é uma ferramenta de linha de comandos simples e poderosa que converte texto em voz. Utiliza as vozes neurais de alta qualidade do serviço **Microsoft Edge TTS** e possui um mecanismo de _fallback_ para uma voz offline padrão, garantindo que a funcionalidade esteja sempre disponível, mesmo sem ligação à internet.

## ✨ Funcionalidades

- **Vozes Neurais de Alta Qualidade**: Acesso a dezenas de vozes realistas do serviço Edge TTS.
- **Fallback Offline**: Se a voz online não estiver acessível (por falta de internet ou erro no serviço), a aplicação utiliza automaticamente uma voz TTS padrão do sistema (`pyttsx3`).
- **Interface Simples**: Fácil de usar diretamente a partir do terminal.
- **Personalizável**: Permite escolher a voz desejada através de um argumento.
- **Portátil**: Funciona em Windows, macOS e Linux.

## ⚙️ Instalação

Para utilizar o `Talk`, precisa de ter o **Python 3.7 ou superior** instalado no seu sistema.

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_NO_GITHUB>
    cd talk
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Linux: source venv/bin/activate
    ```

3.  **Instale as dependências:**
    O projeto inclui um ficheiro `requirements.txt` com todas as bibliotecas necessárias. Instale-as com o seguinte comando:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Como Usar

A utilização é feita através da linha de comandos, passando o texto a ser falado como o primeiro argumento.

### Uso Básico

Para converter um texto simples com a voz padrão (Português de Portugal - Raquel):

```bash
python talk.py "Olá mundo! Este é um teste de conversão de texto para fala."
```

### Especificar uma Voz

Pode usar o argumento `--voice` (ou `-v`) para escolher outra voz.

**Exemplo com voz em Inglês (EUA):**
```bash
python talk.py "Hello world! This is a text-to-speech conversion test." --voice "en-US-AriaNeural"
```

**Exemplo com voz em Português (Brasil):**
```bash
python talk.py "Oi, pessoal! Testando a voz brasileira." --voice "pt-BR-FranciscaNeural"
```

### Como Listar as Vozes Disponíveis?

Para ver a lista completa de vozes que pode utilizar com o argumento `--voice`, execute o seguinte comando, que faz parte da biblioteca `edge-tts`:

```bash
edge-tts --list-voices
```

Copie o "Short name" da voz que deseja (ex: `pt-PT-RaquelNeural`) e use-o no seu comando.

## 📦 Criar um Executável (Opcional)

O script está preparado para ser empacotado num único executável com o `PyInstaller`. Isto permite que o execute em qualquer máquina sem precisar de instalar o Python ou as dependências.

1.  **Instale o PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Crie o executável:**
    ```bash
    pyinstaller --onefile --noconsole talk.py
    ```
    O ficheiro final estará na pasta `dist`.

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o ficheiro `LICENSE` para mais detalhes.
