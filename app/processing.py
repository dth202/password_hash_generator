import crypt
import string

def check_contains(input, letters):
    return any(char in letters for char in input)

def do_validate_password(input):
    # Verify Password requirments
    #
    errors = ''
    if len(input) < 8:
        errors += "<li>Length: Password needs to be at least 8 characters in length.</li>"
    if not check_contains(input, string.digits):
        errors += "<li>Complexity: Password needs at least one number.</li>"
    if not check_contains(input, string.ascii_uppercase):
        errors += "<li>Complexity: Password needs at least one uppercase character.</li>"
    if not check_contains(input, string.ascii_lowercase):
        errors += "<li>Complexity: Password needs at least one lowercase character.</li>"
    if not check_contains(input, string.punctuation + '#'):
        errors += "<li>Complexity: Password needs at least one special character.</li>"
    return errors


def do_passwdsalt(password):
    return crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))

