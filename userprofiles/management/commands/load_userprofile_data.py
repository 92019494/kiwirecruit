from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand
from django.contrib.auth.models import User as DjangoUser

from userprofiles.models import User, Position
from pytz import UTC


DATETIME_FORMAT = '%m/%d/%Y %H:%M'

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the User data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # #Show this when the user types help
    help = "Loads data from load_userprofile_data.csv into our User model"

    def handle(self, *args, **options):
        if User.objects.exists() or Position.objects.exists():
            print('Users and data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        self.create_user_data()
        self.create_candidate_users()
    
    def create_user_data(self, *args, **options):
        print("Loading User data for the user profile...")
        for row in DictReader(open('./userprofile_data.csv')):
            user = User()
            user.name = row['Name']
            usrNme = row['Username']
            user.username = usrNme
            user.sex = row['Sex']
            user.age = row['Age']
            user.save()
            raw_position_strings = row['Positions']
            position_strings = [str for str in raw_position_strings.split('| ') if str]
            for pos_str in position_strings:
                pos = [str for str in pos_str.split('; ') if str]
                position = Position()
                position.job_title = pos[0]
                position.description = pos[1]
                position.start_date = UTC.localize( datetime.strptime(pos[2], DATETIME_FORMAT))
                position.end_date = UTC.localize( datetime.strptime(pos[3], DATETIME_FORMAT))
                position.user = user
                position.save()

    def create_candidate_users(self, *args, **options):
        print("Loading users...")
        for row in DictReader(open('./userprofile_data.csv')):
            django_user = DjangoUser.objects.create_user(
                first_name='',
                is_staff=False,
                is_superuser=False,
                last_name='',
                username=row['Username'],)
            django_user.set_password(row['Password'])
            django_user.save()