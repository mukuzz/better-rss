# Better RSS

## Install
Build Image
```
docker build -t better-rss .
```
Run server
```
docker run -d --restart unless-stopped --name better-rss -v better-rss-data:/opt/better-rss/data -p 9901:80 better-rss
```
## Usage

- Get better feed: `http://localhost:9901/?feedUrl=<feedUrl>`
- Clear cache: `http://localhost:9901/clear`