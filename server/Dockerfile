FROM python

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /server/app
COPY ./migrations /server/migrations
COPY ./run.py /server/run.py
COPY ./run.sh /server/run.sh

EXPOSE 5000

CMD bash run.sh
