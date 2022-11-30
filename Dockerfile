# python:alpine is 3.{latest}
FROM python:alpine

LABEL maintainer="Dallas Harris"

# Default ENV values
# ENV PORT=5000
# ENV URI_BASE=/
# ENV DEBUG=False
# ENV HOST=0.0.0.0
# ENV VALIDATE_PASSWORD=False
# ENV MINIMUM_LENGTH=0
# ENV REQUIRE_NUMBER=False
# ENV REQUIRE_UPPERCASE=False
# ENV REQUIRE_LOWERCASE=False
# ENV REQUIRE_SPECIAL_CHAR=False

RUN pip install flask

COPY app /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["genhash.py"]
