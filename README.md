# Media Server

- Creating a media server for my home use
- Tech stack:
  - Backend: Flask + Jinja
  - Frontend: HTML, CSS & JavaScript + Bootstrap
  - Database: SQLite3

Things to clean up:

- status_403/404, etc. ok
- return status
- APIs change to POST/PUT/DELETE?
- clean up home.html to only have one search and a filter button?

## Deployment Steps

## Features

### Movies

For movies, you need to manually copy the movies to the server via `scp` or other methods.

1. Copy the movies via `scp`

```sh
# /path/to/file - assuming the file is in a Windows machine
# ~ - the remote_username's path
# 192.168.1.1 is the server/the remote username's machine ip address
scp /path/to/file remote_username@192.168.1.1:~
```

2. In the application, log in as an admin and add the movie details
