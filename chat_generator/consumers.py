from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from django.conf import settings
from openai import AsyncOpenAI
import json
import uuid
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.messages = []
        await super().connect()

    async def receive(self, text_data):
        # our webhook handling code will go here.
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]

        #show user's message
        user_message_html = render_to_string(
            "ws/chat_message.html",
            {
                "message_text": message_text,
                "is_system": False,
            },
        )
        await self.send(text_data=user_message_html)

        self.messages.append(
            {
                "role": "user",
                "content": message_text,
            }
        )
        message_id = f"message-{uuid.uuid4().hex}"
        system_message_html = render_to_string(
            "ws/chat_message.html",
            {"message_text": "", "is_system": True, "message_id": message_id},
        )
        await self.send(text_data=system_message_html)

        # for RAG
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        # load FAISS data
        chain = load_qa_chain(ChatOpenAI(temperature=0.7, openai_api_key=settings.OPENAI_API_KEY), chain_type="stuff")
        db = FAISS.load_local(settings.FAISS_STORE_ROOT, embeddings, allow_dangerous_deserialization=True)
        # vector serch
        embedding_vector = embeddings.embed_query(message_text)
        docs_and_scores = db.similarity_search_by_vector(embedding_vector)
        # openai_response
        response = await chain.ainvoke({"input_documents": docs_and_scores, "question": message_text}, return_only_outputs=True, stream=True)
        openai_response = response['output_text']

        # streaming send
        chunks = []
        for chunk in openai_response:
            formatted_chunk = chunk.replace("\n", "<br>")
            await self.send(text_data=f'<div id="{message_id}" hx-swap-oob="beforeend">{formatted_chunk}</div>')
            await asyncio.sleep(0.03)
            chunks.append(chunk)
        self.messages.append({"role": "system", "content": "".join(chunks)})