from django.core.management.base import BaseCommand, CommandError
from questions.models import Tag, Question, Profile
import random
import string

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

class Command(BaseCommand):
    help = 'Genarating random question with existing user and tags'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int)

    def handle(self, *args, **options):
        number = options['number'] if options['number'] is not None else 1
        for i in range(number):           
            author = Profile.objects.get_random()
            title = 'T_' + random_string(random.randint(10, 16))
            body = 'b' + random_string(random.randint(128, 1024))
            rating = random.randint(0, 16)
            question = Question(author=author, title=title,
                                body=body, rating=rating)
            question.save()
            for _ in range(random.randint(1, 5)):
                tag = Tag.objects.get_random()
                question.tags.add(tag)

            question.save()
            self.stdout.write('Question created: {0}\n'.format(title))
