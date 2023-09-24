from langchain.document_loaders import UnstructuredFileLoader, PyPDFLoader, UnstructuredWordDocumentLoader, MWDumpLoader, UnstructuredPowerPointLoader, CSVLoader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import os
import PyPDF2
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
        self.init_langchain_components()

    def init_langchain_components(self):
        # Création d'un index de vecteurs à partir de documents
        document_loaders = [UnstructuredFileLoader, PyPDFLoader, UnstructuredWordDocumentLoader, MWDumpLoader, UnstructuredPowerPointLoader, CSVLoader]
        documents = []

        for loader in document_loaders:
            documents.extend(self.load_documents_with_loader(loader))

        self.create_and_save_vector_index(documents)

        # Configuration du récupérateur et de l'interface de questions-réponses
        self.retriever = self.init_retriever()
        self.qa_interface = self.init_qa_interface()

    def load_documents_with_loader(self, loader):
        documents = []
        # Remplacez les chemins par les chemins de vos documents
        document_paths = ["document1.pdf", "document2.docx", "document3.epub", "document4.txt"]
        
        for document_path in document_paths:
            if os.path.isfile(document_path):
                with open(document_path, 'rb') as file:
                    doc_loader = loader(file_path=document_path)
                    doc = doc_loader.load_and_split(self.text_splitter)
                    documents.extend(doc)

        return documents

    def create_and_save_vector_index(self, documents):
        if not os.path.exists(self.vector_index_directory):
            os.makedirs(self.vector_index_directory)

        # Création de l'index de vecteurs
        embeddings = OpenAIEmbeddings(deployment="text-embedding-ada-002", chunk_size=1)
        self.vector_index = FAISS.from_documents(documents, embeddings)
        
        # Sauvegarde de l'index de vecteurs
        self.vector_index.save_local(self.vector_index_directory)

    def init_retriever(self):
        # Configuration du récupérateur
        retriever = self.vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        return retriever

    def init_qa_interface(self):
        # Configuration de l'interface de questions-réponses
        qa_interface = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(),
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
        )
        return qa_interface

    def predict_QA(self, prompt, document_path):
        # Chargement du texte à partir du document
        document_text = self.load_text_from_document(document_path)
        
        # Recherche de questions-réponses basée sur le prompt et le texte du document
        response = self.qa_interface(
            f"{document_text}\nPrompt: {prompt}"
        )
        
        return response["result"]

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
        pdf = PyPDF2.PdfFileReader(open(document_path, "rb"))
        for page_num in range(pdf.getNumPages()):
            page = pdf.getPage(page_num)
            text += page.extractText()
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

# Exemple d'utilisation
if __name__ == "__main__":
    openai_api_key = "Your OpenAI API Key"
    bot = DocumentChatbot(openai_api_key)

    # Posez une question basée sur un document
    prompt = "Quelles sont les principales conclusions du rapport annuel 2022 ?"
    document_path = "document1.pdf"  # Remplacez par le chemin de votre document
    response = bot.predict_QA(prompt, document_path)
    print("Réponse basée sur le document :")
    print(response)
