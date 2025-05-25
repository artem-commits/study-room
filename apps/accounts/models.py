from django.db import models
from django.contrib.auth.models import AbstractUser

from study_app.settings import DEFAULT_USER_AVATAR


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    This model adds additional fields for user profile information and avatar management.
    It inherits all the standard Django user fields and adds custom fields for enhanced functionality.

    Attributes:
        avatar (ImageField): User's profile picture, stored in users/%Y/%m/%d/ directory.
        birth_date (DateField): User's date of birth, optional.
    """

    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True,
                               verbose_name="Пользовательский аватар")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    @property
    def get_avatar_url(self):
        """
        Get the URL of the user's avatar.

        Returns:
            str: The URL of the user's avatar if it exists, otherwise returns the default avatar URL.
        """
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return DEFAULT_USER_AVATAR
