FROM python:3.8-slim-buster

ENV TZ Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /opt/better-rss/data
COPY requirements.txt /opt/better-rss
WORKDIR /opt/better-rss
RUN pip install -r requirements.txt
COPY . /opt/better-rss

RUN python -c "import nltk;nltk.download('punkt')" && \
    python manage.py migrate && \
    apt-get update && apt-get install --no-install-recommends -y cron && \
    rm -rf /var/lib/apt/lists/* && \
    echo '*/5 * * * * root /usr/local/bin/python /opt/better-rss/manage.py refreshFeeds && echo "$(date)" >> /opt/better-rss/data/refresh-log' > /etc/cron.d/refresh-feeds

EXPOSE 80

CMD cron && \
    python manage.py runserver 0:80