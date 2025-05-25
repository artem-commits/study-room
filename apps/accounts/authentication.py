from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows login by email and password.

    This backend extends Django's ModelBackend to provide email-based authentication.
    It allows users to log in using their email address instead of username.

    Methods:
        authenticate: Authenticates a user based on email and password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on email and password.

        Args:
            request: The current request object.
            username (str, optional): The email address to authenticate with.
            password (str, optional): The password to authenticate with.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The authenticated user if credentials are valid, None otherwise.
        """
        if username is None:
            username = kwargs.get(UserModel.EMAIL_FIELD)
        if username is None or password is None:
            return None
        try:
            user = UserModel._default_manager.get(email__iexact=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
