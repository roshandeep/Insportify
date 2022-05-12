from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import random
import string


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.username) + text_type(timestamp) + text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


class PassTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(''.join(random.choice(string.ascii_lowercase) for i in range(5)))
        )

    def check_token(self, user, token):
        return user.password_reset_token == token;


pass_reset_code = PassTokenGenerator()
