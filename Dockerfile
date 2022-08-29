FROM python:3.10-alpine

COPY . /app/

RUN pip3 install -r ./app/requirements.txt

WORKDIR app

ENTRYPOINT ["python3", "bot.py"]