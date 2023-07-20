from milvus import Milvus, DataType
from sentence_transformers import SentenceTransformer

class SemanticMemory:
    def __init__(self, host='localhost', port='19530', collection_name='semantic_memory'):
        self.client = Milvus(host, port)
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Create collection if it doesn't exist
        if collection_name not in self.client.list_collections():
            self.client.create_collection(collection_name, fields=[
                {"name": "fact_vector", "type": DataType.FLOAT_VECTOR, "params": {"dim": 384}},
                {"name": "fact_id", "type": DataType.INT64}
            ])

    def insert(self, facts):
        vectors = self.model.encode(facts)
        ids = self.client.insert(self.collection_name, [
            {"name": "fact_vector", "type": DataType.FLOAT_VECTOR, "values": vectors},
            {"name": "fact_id", "type": DataType.INT64, "values": list(range(len(facts)))}
        ])
        return ids

    def query(self, vector, top_k=10):
        results = self.client.search(self.collection_name, "fact_vector", [vector], {"metric_type": "L2", "params": {"nprobe": 10}}, top_k)
        return results

    def retrieve(self, id):
        results = self.client.get_entity_by_id(self.collection_name, [id])
        return results

    def delete(self, id):
        self.client.delete_entity_by_id(self.collection_name, [id])
