# python:alpine is 3.{latest}
FROM python:alpine

LABEL maintainer="Dallas Harris"

# Default ENV values
ENV TITLE_STR="Password Hash Generator"
ENV SUBTITLE_STR="created by Dallas Harris"
ENV PROJECT_REPO="https://github.com/dth202/password_hash_generator"
ENV BANNER="This utility returns a SHA512 hash for the string you enter below."
ENV SERVICE_PORT=5000
ENV URI_BASE=/
ENV DEBUG=False
ENV HOST=0.0.0.0
ENV VALIDATE_PASSWORD=True
ENV MINIMUM_LENGTH=8
ENV MAXIMUM_LENGTH=99
ENV REQUIRE_NUMBER=True
ENV REQUIRE_UPPERCASE=True
ENV REQUIRE_LOWERCASE=True
ENV REQUIRE_SPECIAL_CHAR=True

RUN apk add --no-cache libcrypt && \
    pip install flask waitress

COPY app /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["genhash.py"]
