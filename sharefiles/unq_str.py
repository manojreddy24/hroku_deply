#generate tokens for passwords

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

class unqstr(PasswordResetTokenGenerator):
    def hash_values(self,user,timestamp):
        return (
        text_type(user.pk) + text_type(timestamp) 
        # text_type(user.profile.signup_confirmation)
        )

generate_unq = unqstr()