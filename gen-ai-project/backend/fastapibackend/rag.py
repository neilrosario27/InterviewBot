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
     SystemMessage(content="""You are an AI assistant chatbot acting as a professional interviewer for candidates with an engineering background. Your task is to conduct detailed and comprehensive interviews by asking pertinent and insightful questions based on the candidate's engineering expertise, experience, and career aspirations. You should tailor your questions to the candidate's specific area of engineering, whether it be software, civil, mechanical, electrical, etc. Your goal is to evaluate their technical skills, problem-solving abilities, and professional experiences. Additionally, assess their communication skills and cultural fit for the company they are applying to. If a candidate's response is unclear or insufficient, ask follow-up questions to gather more details. If the candidate does not have the relevant experience, acknowledge it politely and shift to another relevant topic. Remember to be professional, encouraging, and objective throughout the interview process.""")

]

# embed_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
# text_field = "text"
# vectorstore = Pinecone(index, embed_model.embed_query,text_field)


# current_script_dir = os.path.dirname(os.path.abspath(__file__))

# # Construct the path to the 'data' folder relative to the current script
# data_directory_path = os.path.join(current_script_dir, 'data')

# # Construct the path to 'data.pdf' within the 'data' folder
# dir_path = os.path.join(data_directory_path, 'data.pdf')


# def get_pdf_text(dir_path):
#     loader = PyPDFLoader(file_path=dir_path)
#     data = loader.load()
#     return data


# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
#     chunks = text_splitter.split_documents(text)
#     return chunks


# def get_vector_store(texts):
#     index_name = "chatbook"
#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
#     docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)


# def process_pinecone():
#     pdf_text = get_pdf_text(dir_path)
#     text_chunks = get_text_chunks(pdf_text)
#     get_vector_store(text_chunks)



def augment_prompt(text, jd, exp):

   

    augemented_prompt =  f"""You are to check the reply from the user and also generate one new questions according to the users Job Description and experience
    
    
    Job Description:
    {jd}

    Experience : 
    {exp}

    User Reply : 
    {text}"""

    return augemented_prompt



def starting_point(text, jd, exp):
    prompt = HumanMessage(
        content = augment_prompt(text, jd, exp)
        )
    message.append(prompt)
    res = chat(message)
    message.append(res)
    return res.content

# def reset_the_pinecone():
#     pinecone.delete_index("chatbook")
#     pinecone.create_index(name="chatbook", dimension=1536, metric='cosine')


               

# def process_pinecone_url(url):
#     loader = WebBaseLoader(url)
#     data = loader.load()
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     texts = text_splitter.split_documents(data)
#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
#     docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
