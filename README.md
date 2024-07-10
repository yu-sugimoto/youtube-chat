Youtube Chat
======================

任意のYouTube動画のリンクを入力すると, その動画に関して非同期チャット形式で質疑応答が可能なアプリケーションです. 
Youtubeで海外のコンテンツをよく見ますが, 1時間近くあるものも多く, Youtube動画の知りたい情報だけを早く教えてほしいと思い開発しました. 
英語で話される海外のコンテンツや長時間コンテンツ（大学の授業・技術系の動画）等の効率的な理解をサポートします. 

## 概要

このDjangoアプリケーションでは, Youtube動画の文字起こし（AssemblyAI）, Youtube動画の翻訳および要約（OpenAI）, Youtube動画に関する質疑応答（RAG）を実装しました. 
ユーザーからYoutube動画のリンクを受け取ると, その動画をダウンロードし, 文字起こしされたトランスクリプトを取得, 要約してチャットボットが出力します. 
その後, Websocket接続を行い, 非同期でRAGを用いた質疑応答が可能になります. 

### RAGの実装  
※質疑応答を日本語で行うため, 日本語以外の動画も考慮して最初にドキュメントを日本語に翻訳  
（ベクトル検索では言語を統一する方が精度が向上する）
1. ドキュメントの読み込み（文字起こしされたトランスクリプトを使用）  
2. ドキュメントの変換
3. テキストデータのベクトル化  
4. ベクトル保存（Faiss）  
5. 情報検索と回答生成

## デモ

[youtube_chat_demo_720.webm](https://github.com/yu-sugimoto/youtube-chat/assets/94701688/4b4781f5-998a-4512-a1ca-ac6d60de4155)

## 使用技術

- Python 3.11.0
- Django 4.2.1
- tailwindcss
- htmx
- pytube
- OpenAI
- LangChain
- Django Channels
- Faiss


## インストール

まず, このアプリケーションをインストールします. 
```
pip install .
```

次に, 必要なパッケージのインストールします. 
```
pip install django
pip install pytube
pip install openai
pip install langchain langchain-openai openai
pip install langchain-community
pip install tiktoken
pip install faiss-cpu
pip install anyio
```

最後に, 必要なAPIキーを 'settings.py' に追加します. 

```python
OPENAI_API_KEY = "sk-***"
ASSMBLYAI＿API_KEY = "*******"
```

### ※pytubeに関するエラー

Youtube自体の変更によって頻出するエラーですので取り上げました. → https://github.com/pytube/pytube/issues

## ディレクトリ構造

```
.
│  .env
│  .gitignore
│  db.sqlite3
│  LICENSE
│  manage.py
│  README.md
│
├─chat_generator
│  │  admin.py
│  │  apps.py
│  │  consumers.py
│  │  models.py
│  │  routing.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │
│  ├─migrations
│  │  │  __init__.py
│  │  │
│  │  └─__pycache__
│  │          __init__.cpython-311.pyc
│  │
│  └─__pycache__
│          admin.cpython-311.pyc
│          apps.cpython-311.pyc
│          consumers.cpython-311.pyc
│          models.cpython-311.pyc
│          routing.cpython-311.pyc
│          urls.cpython-311.pyc
│          views.cpython-311.pyc
│          __init__.cpython-311.pyc
│
├─media
│  └─faiss_store
├─templates
│  │  index.html
│  │
│  └─ws
│          chat_message.html
│
└─youtube_chat
    │  asgi.py
    │  settings.py
    │  urls.py
    │  wsgi.py
    │  __init__.py
    │
    └─__pycache__
            asgi.cpython-311.pyc
            settings.cpython-311.pyc
            urls.cpython-311.pyc
            wsgi.cpython-311.pyc
            __init__.cpython-311.pyc
```
