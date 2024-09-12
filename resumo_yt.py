import pytube
import ffmpeg
import openai
import sys

# Inicializar OpenAI com a chave da API
openai.api_key = 'sua-chave-api'

# Baixa o áudio do arquivo
url = sys.argv[1]
filename = 'audio.wav'
yt = pytube.YouTube(url)
stream = yt.streams.filter(only_audio=True).first().url
ffmpeg.input(stream).output(filename, format='wav', loglevel="error").run()

# Cria transcrição
with open(filename, "rb") as audio_file:
    transcript = openai.Audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    ).text

# Pede pela revisão
completion = openai.ChatCompletion.create(
    model="gpt-4",  # Altere para o modelo correto
    messages=[
        {"role": "system", "content": "Você é um sistema que resume vídeos detalhados. Responda com formatação Markdown."},
        {"role": "user", "content": f"Descreva o seguinte vídeo: {transcript}"}
    ]
)

# Salva o resumo em um arquivo Markdown
with open("resumo.md", "w+") as md:
    md.write(completion.choices[0].message['content'])
