from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
import uuid
import os

def profile_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('media', 'profiles', filename)

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    alternative_email = models.EmailField(blank=True, null=True, unique=True)
    registration_no = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    year_of_study = models.IntegerField(null=True, blank=True)
    linkedin = models.URLField(
        blank=True,
        null=True,
        verbose_name="LinkedIn Profile")

    LEADERSHIP_CHOICES = (
        ('Patron', 'Patron'),
        ('President', 'President'),
        ('Deputy President', 'Deputy President'),
        ('Project Coordinator', 'Project Coordinator'),
        ('Secretary General', 'Secretary General'),
        ('Treasurer', 'Treasurer'),
        ('Organizing Secretary', 'Organizing Secretary'),
        ('Publicity Secretary', 'Publicity Secretary'),
        ('Deputy Publicity Secretary', 'Deputy Publicity Secretary'),
        ('Welfare secretary', 'Welfare Secretary'),
    )

    leadership_role = models.CharField(
        max_length=50,
        choices=LEADERSHIP_CHOICES,
        blank=True,
        null=True)
    profile_image = models.ImageField(
        upload_to=profile_image_file_path, null=True, blank=True)
    is_member = models.BooleanField(default=False, verbose_name="Is Member")
    readonly_fields = ['last_login']
    bio = models.TextField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        if self.leadership_role:
            # Check if another user already has the same leadership role
            existing_user_with_role = User.objects.filter(
                leadership_role=self.leadership_role).exclude(
                pk=self.pk).first()
            if existing_user_with_role:
                raise ValidationError(
                    # flake8: noqa
                    {'leadership_role': 'This role is already assigned to another user.'})
