from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone 
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import WebBaseLoader
load_dotenv()
import json

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

pinecone.init(api_key=PINECONE_API_KEY, environment='gcp-starter')

index_name = "chatbook"
index = pinecone.Index(index_name)


chat = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model='gpt-3.5-turbo',
)


message = [
    # SystemMessage(content="""You are an ai assistant chatbot for ecommerce. You have to answer the responses based on the contexts that will be provided to you. 
    #               If the context doesn't have the answer reply 'I am sorry, I do not have the relevant information.' Do not make up your own answer."""),
    # HumanMessage(content="Hi AI, how are you today?"),
    # AIMessage(content="I'm great thank you. How can I help you?")
    SystemMessage(content="""You are an AI assistant chatbot for ecommerce. You have to answer the responses based on the contexts that will be provided to you. 
                  If the context doesn't have the answer reply 'I am sorry, I do not have the relevant information.' Do not make up your own answer.
                  Additionally, you should analyze the sentiment of the user's message and respond accordingly. If the user seems angry, console them; if they seem sad, try to cheer them up before answering their query."""),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?")
]

embed_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
text_field = "text"
vectorstore = Pinecone(index, embed_model.embed_query,text_field)


current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the 'data' folder relative to the current script
data_directory_path = os.path.join(current_script_dir, 'data')

# Construct the path to 'data.pdf' within the 'data' folder
dir_path = os.path.join(data_directory_path, 'data.pdf')


def get_pdf_text(dir_path):
    loader = PyPDFLoader(file_path=dir_path)
    data = loader.load()
    return data


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunks = text_splitter.split_documents(text)
    return chunks


def get_vector_store(texts):
    index_name = "chatbook"
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)


def process_pinecone():
    pdf_text = get_pdf_text(dir_path)
    text_chunks = get_text_chunks(pdf_text)
    get_vector_store(text_chunks)



def augment_prompt(query, emotion):

    if len(message)>2:
        results = vectorstore.similarity_search(str(message[-1])+'\n'+query,k=3)
    else:
        results = vectorstore.similarity_search(query,k=3)
    source_knowledge = "\n".join([x.page_content for x in results])

    augemented_prompt = f"""Using the contexts below, answer the query. Also you are provided with previous conversations of the 
    system with the user. Refer to this conversation and understand what the user is asking for making you a conversational bot.

    Emotion:
    {emotion}

    Context:
    {source_knowledge}

    Query:
    {query}"""
    return augemented_prompt



def starting_point(question, emotion):
    prompt = HumanMessage(
        content = augment_prompt(question, emotion)
        )
    message.append(prompt)
    res = chat(message[-4:])
    message.append(res)
    return res.content

def reset_the_pinecone():
    pinecone.delete_index("chatbook")
    pinecone.create_index(name="chatbook", dimension=1536, metric='cosine')


               

def process_pinecone_url(url):
    loader = WebBaseLoader(url)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(data)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
