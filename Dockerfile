FROM python:3

MAINTAINER Mike "mike@skylake.me"

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /
COPY ./src/ /

CMD ["python", "prestation2caldav.py"]