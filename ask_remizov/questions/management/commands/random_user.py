from django.core.management.base import BaseCommand, CommandError
from questions.models import Profile
from django.contrib.auth.models import User
import names
import random
import string

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


class Command(BaseCommand):
    help = 'Genarating random user'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int)


    def handle(self, *args, **options):
        number_of_users = options['number'] if options['number'] is not None else 1
        for i in range(number_of_users):
            full_name = names.get_full_name()
            login = 'l' + full_name.replace(' ', '')
            # password = 'p' + random_string(7)
            password = 'p' + random_string(5)
            email = password[1:] + '@mail.ru'
            first_name = full_name.split()[0]
            last_name = full_name.split()[1]

            user = User.objects.create_user(username=login,
                                            email=email,
                                            first_name = first_name,
                                            last_name = last_name,
                                            password=password)
            user.save()
            user.profile.rating = random.randint(-100, 100)

            self.stdout.write('User created: {0} {1} {2}\n'.format(login, password, email))
