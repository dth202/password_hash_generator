import crypt
import string
import os

def check_contains(input, letters):
    return any(char in letters for char in input)

def get_requirements():
    requirements = ''
    if os.environ['MINIMUM_LENGTH']:
        requirements += "<li>Minimum Length: {min_length}</li>".format(min_length=os.environ['MINIMUM_LENGTH'])
    if os.environ['MAXIMUM_LENGTH']:
        requirements += "<li>Maximum Length: {max_length}</li>".format(max_length=os.environ['MAXIMUM_LENGTH'])
    if os.environ['REQUIRE_NUMBER']:
        requirements += "<li>Complexity: Password needs at least one number.</li>"
    if os.environ['REQUIRE_UPPERCASE']:
        requirements += "<li>Complexity: Password needs at least one uppercase character.</li>"
    if os.environ['REQUIRE_LOWERCASE']:
        requirements += "<li>Complexity: Password needs at least one lowercase character.</li>"
    if os.environ['REQUIRE_SPECIAL_CHAR']:
        requirements += "<li>Complexity: Password needs at least one special character.</li>"
    return requirements

def do_validate_password(input):
    # Verify Password requirments
    errors = ''
    if ( os.environ['MINIMUM_LENGTH'] and len(input) < os.environ['MINIMUM_LENGTH'] ) or ( os.environ['MAXIMUM_LENGTH'] and len(input) > os.environ['MAXIMUM_LENGTH'] ):
        errors += "<li>Length: Password needs to be between {min_length} and {max_length} characters in length.</li>".format(min_length=os.environ['MINIMUM_LENGTH'])
    if os.environ['REQUIRE_NUMBER'] and not check_contains(input, string.digits):
        errors += "<li>Complexity: Password needs at least one number.</li>"
    if os.environ['REQUIRE_UPPERCASE'] and not check_contains(input, string.ascii_uppercase):
        errors += "<li>Complexity: Password needs at least one uppercase character.</li>"
    if os.environ['REQUIRE_LOWERCASE'] and not check_contains(input, string.ascii_lowercase):
        errors += "<li>Complexity: Password needs at least one lowercase character.</li>"
    if os.environ['REQUIRE_SPECIAL_CHAR'] and not check_contains(input, string.punctuation + '#'):
        errors += "<li>Complexity: Password needs at least one special character.</li>"
    return errors



def do_passwdsalt(password):
    return crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))

