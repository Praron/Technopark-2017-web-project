from django.core.management.base import BaseCommand, CommandError
from questions.models import Question, Profile, Answer
import random
import string

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

class Command(BaseCommand):
    help = 'Genarating random answer to random existing question'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int)

    def handle(self, *args, **options):
        number = options['number'] if options['number'] is not None else 1
        for i in range(number):           
            author = Profile.objects.get_random()
            question = Question.objects.get_random()
            body = 'b' + random_string(random.randint(128, 1024))
            rating = random.randint(0, 16)
            Answer.objects.create(author=author, body=body,
                                  rating=rating, question=question)
            # answer.save()

            # question.save()
            self.stdout.write('Anwer created: {0}\n'.format(body))
