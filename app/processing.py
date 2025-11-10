import hashlib
import string
import os
import secrets
import base64

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
    if ( os.environ['MINIMUM_LENGTH'] and len(input) < int(os.environ['MINIMUM_LENGTH']) ) or ( os.environ['MAXIMUM_LENGTH'] and len(input) > int(os.environ['MAXIMUM_LENGTH']) ):
        errors += "<li>Length: Password needs to be between {min_length} and {max_length} characters in length.</li>".format(min_length=os.environ['MINIMUM_LENGTH'],max_length=os.environ['MAXIMUM_LENGTH'])
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
    # Generate hash using hashlib with SHA-512
    # Format: $6$salt$hash (similar to crypt SHA-512 format)
    salt = base64.b64encode(secrets.token_bytes(16)).decode('utf-8').rstrip('=')
    hash_result = f"$6${salt}${hashlib.sha512((salt + password).encode()).hexdigest()}"
    
    while hash_result.endswith('.'):
        salt = base64.b64encode(secrets.token_bytes(16)).decode('utf-8').rstrip('=')
        hash_result = f"$6${salt}${hashlib.sha512((salt + password).encode()).hexdigest()}"
    
    return hash_result

