import json
from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):
    help = 'Create multiple users and add them to the database'

    def handle(self, *args, **kwargs):
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)

        for user_info in user_data:
            User.objects.create(
                username=user_info['username'],
                password=user_info['password'],
                email=user_info['email'],
                first_name=user_info['first_name'],
                last_name=user_info['last_name'],
                alternative_email=user_info['alternative_email'],
                registration_no=user_info['registration_no'],
                phone_number=user_info['phone_number'],
                year_of_study=user_info['year_of_study'],
                bio=user_info['bio']
            )
            self.stdout.write(self.style.SUCCESS(
                f'Successfully added user: {user_info["username"]}'))
