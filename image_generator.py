import random
import os


class ImageGenerator:
    def __init__(self):
        self.images_list = os.listdir('image')

    def random_generate(self):
        images_list = self.images_list
        random_index = random.randrange(0, len(images_list))
        return images_list[random_index]
