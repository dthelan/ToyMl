FROM python:3.8-slim-buster

WORKDIR /ToyML
COPY . /ToyML

RUN pip install -r requirements.txt

WORKDIR src

RUN python build_model.py -t train.csv -m Basic_RF.joblib

RUN flask db init
RUN flask db migrate -m "Initial migration."
RUN flask db upgrade

CMD flask run --host=0.0.0.0