import os
from pathlib import Path
from django.core.management.base import BaseCommand
from PIL import Image
import glob

from mix_django.settings import MEDIA_ROOT


class Command(BaseCommand):
    help = 'Изменяет размер картинки согласно аргументу size'
    LIST_OF_FILES = ['png', 'jpg', 'jpeg']
    DIRECTORY = MEDIA_ROOT

    def add_arguments(self, parser):
        parser.add_argument('quality', type=int, help=u'Качество изображений в процентах '
                                                   u'(100 как есть. 75 ужать до 75 процентов) ')

    def handle(self, *args, **kwargs):
        quality = kwargs['quality']
        files = []
        for x in self.LIST_OF_FILES:
            files += glob.glob(self.DIRECTORY + f'/**/*.{x}', recursive=True)
        print(files)
        for file in glob.iglob(self.DIRECTORY + f'/**/*.{x}', recursive=True):
            print(file)
        #     file = Image.open("kenya_buzz_2.jpg")
        #     file.save("kenya_buzz_compressed.jpg", format="JPEG", quality=quality)
