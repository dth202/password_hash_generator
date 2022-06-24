# python:alpine is 3.{latest}
FROM python:alpine

LABEL maintainer="Dallas Harris"

ENV PORT=5000
ENV URI_BASE=/
ENV DEBUG=false
ENV HOST=0.0.0.0
ENV VALIDATE_PASSWORD=false
ENV MINIMUM_LENGTH=0
ENV REQUIRE_NUMBERS=false
ENV REQUIRE_UPPERCASE=false
ENV REQUIRE_LOWERCASE=false
ENV REQUIRE_SPECIAL_CHAR=false

RUN pip install flask

COPY app /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app.py"]
