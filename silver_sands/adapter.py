from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError


class UsernameMaxAdapter(DefaultAccountAdapter):

    def clean_username(self, username):
        if len(username) > 30:
            raise ValidationError('Username must be less than 30 characters \
                in length')
        return DefaultAccountAdapter.clean_username(self, username)

    def clean_email(self, email):
        if len(email) > 100:
            raise ValidationError('Email must be less than 100 characters \
                in length.')
        return DefaultAccountAdapter.clean_email(self, email)
