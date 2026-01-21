# Media Server

- Creating a media server for my home use
- Tech stack:
  - Backend: Flask + Jinja
  - Frontend: HTML, CSS & JavaScript + Bootstrap
  - Database: SQLite3

## Deployment Steps

Shows the steps on how I deploy in my Ubuntu server

1. Install uv - [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
2. Do a git clone (`git clone`, might change to github actions in the future)
3. Install the requirements:
    - if `uv` is installed, run `uv sync`
    - otherwise, run `python -m pip install -r requirements.txt`
4. After installing the dependencies,
    - Create .env file
    - Create `instance` folder
    - Inside `__init__.py`, change 'development' to 'production'
    - Update `app = Flask(__name__, instance_path=instance_path)`
    - DEBUG and TESTING set to False in config.py
    - Since this is production, we need to create instance path in a different location
    - change the db.py -> to schema_staging.sql (where there are no dummy data)
    - change the name of the file from schema_dev.sql to schema_staging.sql
    - initialise the database
    - install waitress (as per tutorial)
    - uv install waitress

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
