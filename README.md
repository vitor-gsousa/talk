# Talk - Conversor de Texto para Voz (TTS) via Linha de Comandos

[![Python](https://img.shields.io/badge/Python-3.13.9-blue.svg)](https://www.python.org/)
[![Powered by edge-tts](https://img.shields.io/badge/powered%20by-edge--tts-brightgreen)](https://github.com/rany2/edge-tts)
[![Powered by piper-tts](https://img.shields.io/badge/powered%20by-piper--tts-orange)](https://github.com/rhasspy/piper)

`Talk` é uma ferramenta de linha de comandos simples e poderosa que converte texto em voz. Utiliza as vozes neurais de alta qualidade do serviço **Microsoft Edge TTS** (online) e possui um mecanismo de _fallback_ para uma voz **Piper-TTS** local (offline), garantindo que a funcionalidade esteja sempre disponível, mesmo sem ligação à internet.

## ✨ Funcionalidades

- **Vozes Neurais Online**: Acesso a dezenas de vozes realistas e de alta qualidade do serviço Microsoft Edge TTS
- **Vozes Offline Local**: Suporte a síntese offline com Piper-TTS (modelos ONNX) - sem necessidade de internet
- **Reprodução em Streaming**: Áudio gerado em tempo real sem criar ficheiros temporários
- **Controlo de Velocidade**: Ajuste fino da velocidade de fala (0.5x - 2.0x) apenas para vozes locais
- **Fallback Automático**: Se a voz online não estiver acessível (sem internet ou erro), usa automaticamente a voz local (Piper) com velocidade reduzida (0.7x) para melhor compreensão
- **Interface Simples**: Fácil de usar diretamente a partir do terminal
- **Personalizável**: Escolha entre vozes online ou local através de argumentos
- **Compilável**: Suporte nativo a PyInstaller para gerar executável portátil
- **Multiplataforma**: Funciona em Windows, macOS e Linux

## ⚙️ Instalação

Para utilizar o `Talk`, precisa de ter o **Python 3.13.9 ou superior** instalado no seu sistema.

### Requisitos do Sistema

- **Python**: 3.13.9+
- **Dependências principais**:
  - `edge-tts` (6.1+): Síntese de fala online via Microsoft Edge
  - `piper-tts` (1.2+): Síntese de fala offline com modelos ONNX
  - `pygame` (2.4+): Reprodução de áudio
  - `sounddevice` (0.4.6+): Interface de áudio alternativa
  - `numpy` (1.24+): Processamento de buffers de áudio
  - `aiohttp` (3.8+): Cliente HTTP assíncrono para streaming

### Passos de Instalação

1. **Clone o repositório:**

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_NO_GITHUB>
    cd talk
    ```

2. **Crie um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    # ou
    source venv/bin/activate  # Linux/macOS
    ```

3. **Instale as dependências:**
    O projeto inclui um ficheiro `requirements.txt` com todas as bibliotecas necessárias. Instale-as com o seguinte comando:

    ```bash
    pip install -r requirements.txt
    ```

4. **Verifique a instalação:**

    ```bash
    python talk.py -h
    ```

## 🚀 Como Usar

A utilização é feita através da linha de comandos, passando o texto a ser falado como o primeiro argumento.

### Uso Básico - Voz Online (Edge-TTS)

Para converter um texto simples com a voz padrão (Português de Portugal - Raquel):

```bash
python talk.py "Olá mundo! Este é um teste de conversão de texto para fala."
```

A voz é reproduzida em **velocidade normal** sem ajustes.

### Uso com Voz Local (Piper-TTS Offline)

Para usar a voz local sem necessidade de internet:

```bash
python talk.py --local "Olá! Isto é síntese offline com Piper."
```

A voz local é reproduzida com velocidade **padrão de 0.9x** (ligeiramente mais lenta que o normal).

### Controlo de Velocidade (Voz Local)

O parâmetro `--speed` permite ajustar a velocidade da voz local. Valores aceitos: **0.5 a 2.0**

```bash
# Fala muito lentamente (0.5x)
python talk.py --local --speed 0.5 "Falando bem devagar"

# Fala mais lentamente (0.7x) - útil para compreensão
python talk.py --local --speed 0.7 "Falando devagar"

# Fala na velocidade normal (1.0x)
python talk.py --local --speed 1.0 "Falando normal"

# Fala mais rapidamente (1.5x)
python talk.py --local --speed 1.5 "Falando rápido"

# Fala muito rapidamente (2.0x)
python talk.py --local --speed 2.0 "Falando muito rápido"
```

**Nota**: O parâmetro `--speed` só funciona quando a flag `--local` está ativa.

### Especificar uma Voz Online

Pode usar o argumento `--voice` para escolher outra voz. O padrão é `pt-PT-RaquelNeural`.

**Exemplo com voz em Inglês (EUA):**

```bash
python talk.py "Hello world! This is a text-to-speech conversion test." --voice "en-US-AriaNeural"
```

**Exemplo com voz em Português (Brasil):**

```bash
python talk.py "Oi, pessoal! Testando a voz brasileira." --voice "pt-BR-FranciscaNeural"
```

### Comportamento de Fallback

Se executar a voz online e **falhar a ligação à internet**, a aplicação:

1. Detecta o erro de conexão
2. Carrega automaticamente a voz local Piper
3. Reproduz um aviso: _"A voz neural não está disponível. A utilizar uma voz padrão para a reprodução."_
4. Reproduz o texto com **velocidade reduzida de 0.7x** para melhor compreensão

### Listar Vozes Disponíveis (Online)

Para ver a lista completa de vozes que pode utilizar com o argumento `--voice`, execute:

```bash
edge-tts --list-voices
```

Copie o "Short name" da voz que deseja (ex: `pt-PT-RaquelNeural`) e use-o no seu comando.

### Argumentos Disponíveis

```bash
python talk.py -h
```

Saída esperada:

```bash
usage: talk.py [-h] [--voice VOICE] [--local] [--speed SPEED] text

Conversor de Texto para Fala

positional arguments:
  text                  Texto a ser convertido.

options:
  -h, --help            show this help message and exit
  --voice VOICE         Voz para síntese. (Padrão: pt-PT-RaquelNeural)
  --local               Força o uso da voz local (offline).
  --speed SPEED         Velocidade de fala (apenas para voz local). 
                        (0.5=mais lento, 1.0=normal, 2.0=mais rápido). 
                        Padrão: 0.9
```

## 📦 Criar um Executável (Opcional)

O projeto está configurado para ser compilado num único executável com PyInstaller. Isto permite executar em qualquer máquina Windows sem precisar de instalar Python ou as dependências.

O script está preparado para ser empacotado num único executável com o `PyInstaller`.

1. **Instale o PyInstaller (se não estiver instalado):**

    ```bash
    pip install pyinstaller
    ```

2. **Crie o executável:**

    ```bash
    pyinstaller talk.spec --clean -y
    ```

    O ficheiro final estará em `dist/talk/talk.exe`.

3. **Execute o executável:**

    ```bash
    .\dist\talk\talk.exe "Teste com o executável compilado"
    ```

    Ou com voz local:

    ```bash
    .\dist\talk\talk.exe --local --speed 0.8 "Falando com voz local"
    ```

### Detalhes da Compilação

O ficheiro `talk.spec` está otimizado para:

- **Incluir modelos de voz**: Os modelos ONNX do Piper estão no diretório `models/`
- **Incluir dados do espeak-ng**: Necessários para a fonética da voz offline
- **Streaming de áudio**: Reprodução direta em memória sem ficheiros temporários
- **Ícone e manifesto**: Interface visual profissional no Windows

**Nota importante**: A compilação inclui todos os modelos de voz (`models/`) e dependências no executável, tornando o ficheiro maior (~150-200MB), mas totalmente portátil e independente.

## 🔀 Fluxo de Funcionamento

```text
[Entrada de Texto]
        ↓
    [Analisar Argumentos]
        ↓
    [--local?]
    ↙        ↘
  SIM      NÃO
   ↓         ↓
[Piper]  [Edge-TTS Online]
   ↓         ↓
   ├─────────┤
   ↓         ↓
   OK?  Falhou a internet?
   ↓    ↙          ↘
   ✓  SIM          NÃO
       ↓           ↓
   [Fallback]    [Erro]
    Piper 0.7x
       ↓
  [Reproduzir Áudio]
```

## 🎯 Arquitetura

### Componentes Principais

1. **Edge-TTS**: Interface async para Microsoft Edge vozes (online)
   - Transmissão direta de áudio em formato MP3
   - Suporta dezenas de idiomas e vozes
   - Requer ligação à internet

2. **Piper-TTS**: Síntese neural offline com modelos ONNX
   - Modelo local: `pt_PT-tugão-medium.onnx` (Português)
   - Funciona completamente offline
   - Suporta controlo fino de velocidade via `SynthesisConfig`

3. **Reprodução de Áudio**:
   - `sounddevice` para reprodução local e fallback
   - `pygame.mixer` para streaming de Edge-TTS
   - BytesIO para buffering em memória (sem ficheiros temporários)

4. **PyInstaller**: Empacotamento portátil
   - Inclui espeak-ng-data para fonética offline
   - Suporta ícone e manifesto personalizado
   - Compilação otimizada para Windows

## 📊 Casos de Uso

| Cenário | Comando | Comportamento |
|---------|---------|---------------|
| Voz online padrão | `python talk.py "Texto"` | Edge-TTS Raquel, velocidade normal |
| Voz online customizada | `python talk.py "Texto" --voice "en-US-AriaNeural"` | Edge-TTS com voz escolhida |
| Voz offline | `python talk.py --local "Texto"` | Piper local, velocidade 0.9x |
| Voz offline lenta | `python talk.py --local --speed 0.5 "Texto"` | Piper local, velocidade 0.5x |
| Fallback (sem internet) | `python talk.py "Texto"` | Detecta falha → Piper 0.7x |

## 🐛 Resolução de Problemas

### Erro: "Módulo piper não encontrado"

```bash
pip install -r requirements.txt
```

### Erro: "ESPEAK_DATA configurado para..." (no executável)

Este é um aviso informativo, não é erro. Indica que o executável está a usar os dados de fonética do espeak-ng. Pode ser ignorado.

### Compilação falha com "ficheiro já existe"

```bash
pyinstaller talk.spec --clean -y
# ou manualmente:
Remove-Item -Recurse -Force dist/talk build
pyinstaller talk.spec -y
```

### Sem som após executar

- Verifique se o volume do sistema está ativo
- Teste com: `python talk.py "Teste de som"`
- Em caso de erro, verifique `sounddevice` e `pygame.mixer`

## 📝 Estrutura do Projeto

```text
talk/
├── talk.py              # Script principal
├── talk.spec            # Configuração PyInstaller
├── requirements.txt     # Dependências Python
├── README.md           # Documentação
├── talk.ico            # Ícone do executável
├── talk.manifest       # Manifesto do executável
└── models/             # Modelos de voz ONNX
    ├── pt_PT-tugão-medium.onnx
    └── pt_PT-tugão-medium.onnx.json
```

## 🔧 Desenvolvimento

### Modificar Modelo de Voz Offline

Para usar outro modelo Piper, baixe o ficheiro `.onnx` desejado e:

1. Coloque o ficheiro em `models/`
2. Atualize `LOCAL_VOICE_MODEL` em `talk.py`

```python
LOCAL_VOICE_MODEL = os.path.join(MODELS_DIR, "seu_modelo.onnx")
```

### Adicionar Novas Vozes

Os modelos Piper estão disponíveis em: [Piper Models](https://huggingface.co/rhasspy/piper-voices)

### Testar Offline

Para testar o fallback sem internet:

1. Desative a ligação à internet
2. Execute: `python talk.py "Texto"`
3. Observe o fallback automático para Piper

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o ficheiro `LICENSE` para mais detalhes.
