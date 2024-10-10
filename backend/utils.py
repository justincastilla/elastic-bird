# taken from Alex Salgados' code: https://www.elastic.co/search-labs/blog/implementing-image-search-with-elasticsearch
import os
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import dotenv

dotenv.load_dotenv()


class Util:
    @staticmethod
    def get_index_name():
        return "bird-image-index-dev"

    @staticmethod
    def get_connection():
        es_endpoint = os.getenv("ES_ENDPOINT")
        es_api_key = os.getenv("ES_API_KEY")
        es = Elasticsearch(hosts=es_endpoint, api_key=es_api_key)
        es.info()  # should return cluster info
        return es

    @staticmethod
    def create_index(es: Elasticsearch, index_name: str):
        # Specify index configuration
        index_config = {
            "settings": {"index.refresh_interval": "5s", "number_of_shards": 1},
            "mappings": {
                "properties": {
                    "image_embedding": {
                        "type": "dense_vector",
                        "dims": 512,
                        "index": True,
                        "similarity": "cosine",
                    },
                    "bird_id": {"type": "keyword"},
                    "name": {"type": "keyword"},
                    "image_path": {"type": "keyword"},
                    "scientific_name": {"type": "keyword"},
                    "exif": {
                        "properties": {
                            "location": {"type": "geo_point"},
                            "date": {"type": "date"},
                        }
                    },
                }
            },
        }

        # Create index
        if not es.indices.exists(index=index_name):
            index_creation = es.indices.create(
                index=index_name, ignore=400, body=index_config
            )
            print("index created: ", index_creation)
        else:
            print("Index  already exists.")

    @staticmethod
    def delete_index(es: Elasticsearch, index_name: str):
        # delete index
        es.indices.delete(index=index_name, ignore_unavailable=True)
