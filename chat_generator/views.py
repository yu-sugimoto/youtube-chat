from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from pytube import YouTube
import os
import assemblyai as aai
import openai
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Create your views here.

def index(request):
    return render(request, 'index.html')

# processing until generate chat screen
@csrf_exempt
def generate_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': '無効なデータです'}, status=400)

        # get transcripts
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "トランスクリプトを取得できませんでした"}, status=500)
        
        # save transcripts in vectordb
        save_transription(transcription)

        # use openai to generate the chat
        chat_content = generate_chat_from_transcription(transcription)
        if not chat_content:
            return JsonResponse({'error': "Chatが開始されませんでした"}, status=500)

        # return Youtube chat as a response
        return JsonResponse({'content': chat_content, 'title': yt_title(yt_link)})

    else:
        return JsonResponse({'error': '無効なリクエストです'}, status=405)


# get title
def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

# save .mp3 in media directory
def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

# get transcripts
def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
    # use aai function for transcribe
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text

# save transcripts in a vectordb
def save_transription(transcription):

    # transcripts translated into Japanese (useful for RAG sessions in Japanese)
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f"次のYouTube動画のトランスクリプトを日本語に翻訳してください。:\n\n{transcription}\n\nChat:"
    # get japanese transcription
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    transcription_ja = response.choices[0].message.content.strip()

    # transcripts preprocessing
    text_splitter = CharacterTextSplitter(
        separator = '。',
        chunk_size = 100,
        chunk_overlap = 0,
        length_function = len,
    )
    docs = text_splitter.create_documents([transcription_ja])

    # uses the vector conversion API provided by OpenAI
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(settings.FAISS_STORE_ROOT,'index')

# get summary from transcription
def generate_chat_from_transcription(transcription):
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f"次のYouTube動画のトランスクリプトをもとに、300字程度で包括した要約文を日本語で書きなさい。:\n\n{transcription}\n\nChat:"
    # generate summary
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    generated_content = response.choices[0].message.content.strip()
    return generated_content

