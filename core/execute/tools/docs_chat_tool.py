from langchain.document_loaders import UnstructuredFileLoader, PyPDFLoader, UnstructuredWordDocumentLoader, MWDumpLoader, UnstructuredPowerPointLoader, CSVLoader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from docx import Document
from ebooklib import epub
import faiss
from typing import List

class DocumentChatbot:
    def __init__(self, openai_api_key, vector_index_directory='index_store'):
        # Configuration de l'API OpenAI
        os.environ["OPENAI_API_KEY"] = openai_api_key

        # Initialisation des composants LangChain
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vector_index_directory = vector_index_directory
        self.vector_index = None
        self.retriever = None
        self.qa_interface = None
 
    def init_retriever(self):
        # Configuration du récupérateur
        retriever = self.vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        return retriever

    def init_qa_interface(self,prompt):
        # Configuration de l'interface de questions-réponses
        qa_interface = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(),
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
        )
        return qa_interface(prompt)

    def predict_QA(self, prompt, document_path):
        # Chargement du texte à partir du document
        document_text = self.load_text_from_document(document_path)
        
        # Recherche de questions-réponses basée sur le prompt et le texte du document
        #response = self.qa_interface(
          #  f"{document_text}\nPrompt: {prompt}"
        #)
        document_text=self.split_text(document_text)
        print(document_text)
        self.create_vectors(document_text)
        self.retrieve_vectors()
        print(self.retriever)
        pkj=self.init_qa_interface(prompt)["result"]
        print(pkj)
        return 'la'
        #return response["result"]

    def load_text_from_document(self, document_path):
        file_extension = os.path.splitext(document_path)[-1].lower()
        
        if file_extension == ".pdf":
            text = self.extract_text_from_pdf(document_path)
        elif file_extension == ".doc" or file_extension == ".docx":
            text = self.extract_text_from_docx(document_path)
        elif file_extension == ".epub":
            text = self.extract_text_from_epub(document_path)
        elif file_extension == ".txt":
            text = self.extract_text_from_txt(document_path)
        else:
            raise ValueError("Format de fichier non pris en charge")
        
        return text

    def extract_text_from_pdf(self, document_path):
        text = ""
        pdf = PdfReader(open(document_path, "rb"))
        for page_num in range(len(pdf.pages)):  # Use len(pdf.pages) to get the number of pages
          page = pdf.pages[page_num]
          text += page.extract_text()
        return text

    def extract_text_from_docx(self, document_path):
        doc = Document(document_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def extract_text_from_epub(self, document_path):
        book = epub.read_epub(document_path)
        text = ""
        for item in book.items:
            if isinstance(item, epub.EpubHtml):
                text += item.content
        return text

    def extract_text_from_txt(self, document_path):
        with open(document_path, "r", encoding="utf-8") as file:
            text = file.read()
        return text
    def split_text(self,text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.create_documents([text])
        return texts
    def create_vectors(self,text):
        directory = 'index_store'
        vector_index = FAISS.from_documents(text, OpenAIEmbeddings())
        vector_index.save_local(directory)
    def retrieve_vectors(self):
        vector_index = FAISS.load_local("index_store", OpenAIEmbeddings())
        self.retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})

class VideoChatbot:
    def __init__():

# Exemple d'utilisation
if __name__ == "__main__":
    openai_api_key = ''
    bot = DocumentChatbot(openai_api_key)

    # Posez une question basée sur un document
    prompt = "Resume ce livre"
      # Remplacez par le chemin de votre document
    response = bot.predict_QA(prompt,"GSE_7-2.pdf")
    print("Réponse basée sur le document :")
    print(response)
