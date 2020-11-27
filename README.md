# Better RSS

Build Image
```
docker build -t better-rss .
```
Run server
```
docker run -d --restart unless-stopped --name better-rss -v better-rss-data:/opt/better-rss/data -p 9901:80 better-rss
```
Add feeds
```
docker exec -it better-rss python manage.py addFeed
```

All feeds will be refreshed periodically according to there refresh intervals through a cron job.
Access feeds throug `localhost:9901/feed/<feed-short-name>`

Access refresh logs through
```
docker exec better-rss cat data/refresh-log
```