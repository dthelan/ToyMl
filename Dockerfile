FROM toyml:latest

WORKDIR /ToyML
COPY . /ToyML

RUN pip install -r requirements.txt

WORKDIR src

RUN python build_model.py -t train.csv -m Basic_RF.joblib

ENV FlASK_APP = app.py

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD flask run