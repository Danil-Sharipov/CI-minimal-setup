FROM python:3.9-slim-bullseye AS build-env

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r /app/model/requirements.txt --target /packages
WORKDIR /app

FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
COPY --from=build-env /packages /packages
ENV PYTHONPATH=/packages
WORKDIR /app
EXPOSE 5000
CMD ["model/main.py"]

