from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class AparnaOnlyBackend(BaseBackend):
    """
    Authenticate only the fixed credentials:
    username: 'aparna', password: 'password'.

    On success, returns a (possibly auto-created) user instance from the
    configured AUTH_USER_MODEL. No other credentials are accepted.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username == 'aparna' and password == 'password':
            User = get_user_model()
            user, _created = User.objects.get_or_create(username='aparna')
            # Ensure the user is active for login purposes
            if getattr(user, 'is_active', True) is False:
                user.is_active = True
                user.save(update_fields=['is_active'])
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

