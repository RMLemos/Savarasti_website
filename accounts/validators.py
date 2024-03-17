from collections import defaultdict

from django.core.exceptions import ValidationError

class UserProfileValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_country()
        self.clean_interests()
        self.clean_bio()

    def clean_country(self):
        country = self.data.get('country')

        if len(country) < 5:
            self.errors['country'].append('Must have at least 5 chars.')

        return country

    def clean_interests(self):
        interests = self.data.get('interests')

        if len(interests) < 5:
            self.errors['interests'].append('Must have at least 5 chars.')

        return interests
    

    def clean_bio(self):
        bio = self.data.get('bio')

        if len(bio) < 5:
            self.errors['bio'].append('Must have at least 5 chars.')

        return bio