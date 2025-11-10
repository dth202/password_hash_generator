#import hashlib
import string
import os
import secrets
import base64
import ctypes
import logging


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

log = logging.getLogger(__name__)

# Load crypt library once at module level
# In Alpine Linux, crypt is part of musl libc
try:
    _libc = ctypes.CDLL("libc.musl-x86_64.so.1")
    _crypt = _libc.crypt
    _crypt.restype = ctypes.c_char_p
    log.info("Successfully loaded musl libc")
except Exception as e:
    log.error(f"Failed to load libc: {e}")
    _crypt = None
    exit(1)

def check_contains(input, letters):
    return any(char in letters for char in input)

def get_requirements():
    log.info("Starting get_requirements() ...")
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
        
    log.info("get_requirements complete. passing results to caller...")
    log.debug("Password requirements: %s" % requirements)
    return requirements

def do_validate_password(input):
    # Verify Password requirments
    log.info("starting do_validate_password() ...")
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
    
    log.info("do_validate_password complete. passing results to caller...")
    log.debug("Password validation errors: %s" % errors)
    return errors



def do_passwdsalt(password):
    
    # Logging
    log.info("Starting do_passwdsalt() ...")
    log.debug("Password: %s" % password)
    
    if _crypt is None:
        log.error("libc is not available!")
        raise RuntimeError("libc library not loaded")
    
    # Using ctypes to call crypt from musl libc (Alpine Linux)
    log.debug("Setting salt")
    salt = base64.b64encode(secrets.token_bytes(16), altchars=b"./").rstrip(b"=")
    log.debug("Finished setting salt")
    log.debug("salt: %s" % salt.decode())
    
    log.debug("Generating hash_result...")
    hash_result = _crypt(password.encode(), b"$6$"+salt).decode()
    log.debug("Finished setting hash_result...")
    
    log.debug("starting while loop to check for '.' at end of hash...")
    while hash_result.endswith('.'):
        log.info("Hash ends with '.', regenerating salt and hash...")
        salt = base64.b64encode(secrets.token_bytes(16), altchars=b"./").rstrip(b"=")
        hash_result = _crypt(password.encode(), b"$6$"+salt).decode()
    log.debug("while loop complete")
    
    
    log.info("Finished do_passwdsalt(). Returning value to caller.")
    log.debug("Generated hash: %s" % hash_result)
    return hash_result

