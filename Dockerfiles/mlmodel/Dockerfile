FROM python:3.9-slim-bullseye

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
  
CMD python3 model/main.py

EXPOSE 5000