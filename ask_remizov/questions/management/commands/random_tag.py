from django.core.management.base import BaseCommand, CommandError
from questions.models import Tag
import random
import string

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

class Command(BaseCommand):
    help = 'Genarating random tag'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int)

    def handle(self, *args, **options):
        number_of_tags = options['number'] if options['number'] is not None else 1
        for i in range(number_of_tags):           
            text = 't' + random_string(5)
            Tag.objects.create(text=text)
            self.stdout.write('Tag created: {0}\n'.format(text))
