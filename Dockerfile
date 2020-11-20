# python:alpine is 3.{latest}
FROM python:alpine

LABEL maintainer="Dallas Harris"

RUN pip install flask

COPY app /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app.py"]
