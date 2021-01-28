FROM python:3.8-alpine
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

WORKDIR /ToyML
ADD . /ToyML

RUN pip install -r requirements.txt

WORKDIR src

RUN python build_model.py -t train.csv -m Basic_RF.joblib

CMD python app.py -m Basic_RF.joblib