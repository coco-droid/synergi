import pinecone
from sentence_transformers import SentenceTransformer

class EpisodicMemory:
    def __init__(self, index_name, api_key=None):
        self.index_name = index_name
        self.api_key = api_key
        self.model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

    def encode(self, experience):
        # Encode une expérience utilisateur sous forme de vecteurs
        vectors = self.model.encode([experience])
        return vectors[0]

    def retrieve(self, query):
        # Recherche d'expériences similaires à une requête
        results = pinecone.query(index_name=self.index_name, query=[query], top_k=10, api_key=self.api_key)
        return results.ids

    def save(self, vectors, key):
        # Sauvegarde des vecteurs dans l'index Pinecone
        pinecone.index(index_name=self.index_name, data=vectors, ids=[key], api_key=self.api_key)

    def delete(self, key):
        # Supprime une expérience de la mémoire
        pinecone.delete(index_name=self.index_name, ids=[key], api_key=self.api_key)