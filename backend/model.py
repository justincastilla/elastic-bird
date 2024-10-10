from sentence_transformers import SentenceTransformer
from PIL import Image

model = SentenceTransformer("clip-ViT-B-32")


def get_embedding(image_path: str):
    temp_image = Image.open(image_path)
    return model.encode(temp_image).tolist()
