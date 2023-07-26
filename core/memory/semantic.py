from sentence_transformers import SentenceTransformer
import milvus

class SemanticMemory:

    def __init__(self):

        self.model = SentenceTransformer('all-MiniLM-L6-v2')  
        self.milvus = milvus.Milvus()
        self.collection_name = "semantic_memory"

        # Création collection etc...

    def insert(self, facts):
       
        embeddings = self.model.encode(facts)

        ids = self.milvus.insert(self.collection_name, {
            "embeddings": embeddings,
            "ids": list(range(len(facts))) 
        })

        return ids

    def query(self, vector, top_k=10):

        results = self.milvus.search(self.collection_name, query_vectors=[vector], top_k=top_k)
        return results

    # Autres méthodes

    def retrieve(self, id):
        results = self.client.get_entity_by_id(self.collection_name, [id])
        return results

    def delete(self, id):
        self.client.delete_entity_by_id(self.collection_name, [id])
