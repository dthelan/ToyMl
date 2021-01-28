FROM python:3.8

WORKDIR /ToyML
ADD . /ToyML

RUN pip install -r requirements.txt

WORKDIR src

RUN python build_model.py -t train.csv -m Basic_RF.joblib

CMD python app.py -m Basic_RF.joblib