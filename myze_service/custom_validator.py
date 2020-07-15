from cerberus import Validator
import re

def valid_email(email):
        if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$', email):
            return True
        else:
            return False

class CustomValidator(Validator):
    def _validate_email(self, email, field, value):
        if email and not valid_email(value):
            self._error(field, "Must be an email")
