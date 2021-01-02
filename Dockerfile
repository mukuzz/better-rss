FROM python:3.8-slim-buster

ENV TZ Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /opt/better-rss/data
COPY requirements.txt /opt/better-rss
WORKDIR /opt/better-rss
RUN pip install -r requirements.txt
COPY . /opt/better-rss

RUN python manage.py migrate

EXPOSE 80

CMD python manage.py runserver 0:80