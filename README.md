# Linux password hash generator

A Web application that will generate a sha-512 password hash. 

There are several best practice checks:
- Password needs to be at least 8 characters in length
- Password needs at least one number
- Password needs at least one uppercase character.
- Password needs at least one lowercase character.
- Password needs at least one special character.

# Background/Use Case

There are several cases where Linux applications use PAM for password management even though the user never actually logs into a commandline (e.g. SFTP Users, DB2 users) I needed a simple process to allow users to set their password without the need to login to the server. This started out as a python script that I would run on my desktop and users would come enter their password at my desk manually then I would set the password hash using a CMS like saltstack. This provided some challanges for remote workers though and this simple python script evolved into a flask application and hosted on an internal docker server behind an nginx load balancer.

Now users are able to go to the website, generate a password hash, and send it to me. I could then push their password out to all required servers. 

# Simple Python Flask App

This image sets up a simple python flask app and exposes it on port 5000. 


## Credit where credit is due

This was inspired by jcdemo/flaskapp. Thank him for unknowingly providing a template for this project.


## Simple usage
```
docker run -d dth202/password_hash_generator
```

## Advanced Usage
```
docker run \
  --name genhash \
  -d \
  -v genhash_app:/app \
  --restart always \
  dth202/password_hash_generator
```

## Environment Variables

### Password Requirements
VALIDATE_PASSWORD=true
MINIMUM_LENGTH=8
MAXIMUM_LENGTH=NONE
REQUIRE_NUMBER=True
REQUIRE_UPPERCASE=True
REQUIRE_LOWERCASE=True
REQUIRE_SPECIAL_CHAR=True

### Debug
DEBUG=False

### APP parameters
HOST=0.0.0.0
PORT=5000
URI_BASE=/

### Display Options




## Volume

The volume is not necessary unless you want to modify the application without contributing to the project.

## License

This is free to use/distribute. However feel free to contribute if you feel like there is more functionality you would like to implement.

## Changelog

2021/04/20 - Added this line to force new build with latest alpine image.

