FROM python:3.12

RUN mkdir /mathema_plus

WORKDIR /mathema_plus

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

EXPOSE 8888
