from sentence_transformers import SentenceTransformer
import pinecone

class EpisodicMemory:

  def __init__(self, index_name, api_key=None):
    self.index_name = index_name
    self.api_key = '5c61b38c-3e37-44f3-881c-5a4ba7ddcf0b'

    # Charge le modèle sentence-transformers
    self.model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

  def encode(self, experience):
    # Génère l'embedding 
    embedding = self.model.encode(experience)
    return embedding

  def retrieve(self, query):
    
    # Encode la requête
    query_embedding = self.encode(query)

    results = pinecone.query(index_name=self.index_name,
                       query=[query_embedding],
                       top_k=10,
                       api_key=self.api_key)

    return results.ids

  # autres méthodes...

  def save(self, vector, key):
    pinecone.upsert(self.index_name, [vector], [key], api_key=self.api_key)  
    
  def delete(self, key):
    pinecone.delete(self.index_name, [key], api_key=self.api_key)