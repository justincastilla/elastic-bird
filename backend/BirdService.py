from BirdRepository import BirdRepository
from Bird import Bird
from typing import List


# service layer
class BirdService:

    def __init__(self, BirdRepository: Bird):
        self.bird_repository = BirdRepository

    def register_bird(self, bird: Bird):
        self.bird_repository.insert(bird)

    def register_birds(self, birds: List[Bird]):
        self.bird_repository.bulk_insert(birds)

    def find_bird_by_image(self, image_path: str):
        image_embedding = Bird.get_embedding(image_path)
        return self.bird_repository.search_by_image(image_embedding)
