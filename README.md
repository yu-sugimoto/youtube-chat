Youtube Chat
======================

任意のYouTube動画のリンクを入力すると, その動画に関して非同期チャット形式で質疑応答が可能なアプリケーションです. 
英語で話される海外のコンテンツや長時間コンテンツ等の効率的な理解をサポートします. 

## 概要

このDjangoアプリケーションでは, Youtube動画の文字起こし（AssemblyAI）, Youtube動画の翻訳及び要約（OpenAI）, Youtube動画に関する質疑応答（RAG）を実装した. 
ユーザーからYoutube動画のリンクを受け取ると, その動画をダウンロードし, 文字起こしされたトランスクリプトを取得, 要約してチャットボットが出力する. 
その後, Websocket接続を行い, 非同期でRAGを用いた質疑応答が可能になる. 

RAGの実装は以下の構成である.  
※質疑応答を日本語で行う場合、最初にドキュメントを日本語に翻訳する（ベクトル計算を行うため言語を統一する方が精度が向上する）
1. ドキュメントの読み込み（文字起こしされたトランスクリプトを使用）  
2. ドキュメントの変換
3. テキストデータのベクトル化  
4. ベクトル保存  
5. 情報検索と回答生成

## デモ

準備中...

## 使用技術

### インストール

まず, このアプリケーションをインストールします. 
```
pip install .
```

次に, 必要なパッケージのインストールします. 
```
pip install django
pip install openai
pip install langchain langchain-openai openai
pip install langchain-community
pip install tiktoken
pip install faiss-cpu
```

最後に, 必要なAPIキーを 'settings.py' に追加します. 

```python
OPENAI_API_KEY = "sk-***"
ASSMBLYAI＿API_KEY = "*******"
```

### pytubeに関するエラー

Youtube自体の変更によって頻出するエラーですので取り上げました. 
https://github.com/pytube/pytube/issues

## ディレクトリ構造

準備中...
