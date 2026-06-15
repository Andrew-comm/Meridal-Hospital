# accounts/decorators.py

from django.contrib.auth.decorators import user_passes_test


def role_required(role):

    return user_passes_test(
        lambda u: u.role == role
    )