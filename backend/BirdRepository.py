from typing import List, Dict
from utils import Util
from Bird import Bird
from elasticsearch import Elasticsearch


# persistence layer
class BirdRepository:
    def __init__(
        self,
        es_client: Elasticsearch,
        index_name: str = "bird-image-index",
        new_indices: bool = False,
    ):
        self.es_client = es_client
        self._index_name = index_name
        # if new_indices:
        #     Util.create_index(es_client, index_name)

    def insert(self, bird: Bird):
        bird.generate_embedding()
        document = bird.__dict__
        self.es_client.index(index=self._index_name, document=document)

    def bulk_insert(self, birds: List[Bird]):
        operations = []
        for bird in birds:
            operations.append({"index": {"_index": self._index_name}})
            operations.append(bird.__dict__)
        self.es_client.bulk(body=operations)

    def search_by_image(self, image_embedding: List[float]):
        field_key = "image_embedding"

        knn = {
            "field": field_key,
            "k": 5,
            "num_candidates": 100,
            "query_vector": image_embedding,
            "boost": 100,
        }

        # The fields to retrieve from the matching documents
        fields = ["name", "scientific_name", "image_path", "description"]

        try:
            resp = self.es_client.search(
                index=self._index_name, body={"knn": knn, "_source": fields}, size=1
            )
            # Return the search results
            return resp
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
