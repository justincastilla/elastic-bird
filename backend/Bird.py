import os
from sentence_transformers import SentenceTransformer
from PIL import Image


# domain class
class Bird:
    model = SentenceTransformer("clip-ViT-B-32")

    def __init__(self, image_path, name, scientific_name):
        self.name = name
        self.scientific_name = scientific_name
        self.image_path = image_path
        self.image_embedding = None

    @staticmethod
    def get_embedding(image_path: str):
        temp_image = Image.open(image_path)
        return Bird.model.encode(temp_image).tolist()

    def generate_embedding(self):
        self.image_embedding = Bird.get_embedding(self.image_path)

    def __repr__(self):
        return (
            f"name={self.name}, image_embedding={self.image_embedding}, "
            f"scientific_name={self.scientific_name})"
            f"image_path={self.image_path}, "
        )

    def to_dict(self):
        return {
            "name": self.name,
            "scientific_name": self.scientific_name,
            "image_path": self.image_path,
            "image_embedding": self.image_embedding,
        }
