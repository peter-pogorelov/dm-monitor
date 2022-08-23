FROM python:3.7.9
LABEL Maintainer="pogorelov.pg@parma.ru"

WORKDIR /usr/app/src
ADD ./ /usr/app/src

RUN pip install -r requirements.txt

CMD [ "python", "app.py"]