# URL Shortener
 
A small URL shortener API built with **FastAPI** and **PostgreSQL**, packaged with **Docker** and run with **Docker Compose**. Send it a long URL, get back a short code, and visit the code to be redirected.
 
The project demonstrates how to containerize a real application: environment-based configuration, a database with persistent storage, and a one-command setup.
 
## Features
 
- `POST /shorten` creates a short code for a URL
- `GET /{code}` redirects to the original URL
- `GET /health` reports that the app is running
- Interactive API docs at `/docs` (provided by FastAPI)
- Data stored in PostgreSQL and kept in a Docker volume, so it survives container restarts and removal
- All configuration comes from environment variables
## Tech stack
 
- Python 3.12, FastAPI, Uvicorn
- PostgreSQL 16 (via `psycopg`)
- Docker and Docker Compose
## Quick start
 
Requires [Docker](https://docs.docker.com/get-docker/) with the Compose plugin.
 
```bash
git clone https://github.com/spl3ndid/url-shortener.git
cd url-shortener
 
# create a settings file from the template, then set a database password in it
cp .env.example .env
 
docker compose up --build
```
 
The app is then available at `http://localhost:3000`. Open `http://localhost:3000/docs` to try the API in the browser.
 
## Usage
 
Create a short URL:
 
```bash
curl -X POST localhost:3000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```
 
Example response:
 
```json
{"code": "9354f9b8", "short": "/9354f9b8"}
```
 
Follow a short code by replacing `9354f9b8` with the code returned by the request above:
 
```bash
curl -i localhost:3000/9354f9b8
```
 
```
HTTP/1.1 307 Temporary Redirect
location: https://example.com
```
 
Opening `http://localhost:3000/<code>` in a browser redirects to the original URL.
 
## API
 
| Method | Path       | Description                                | Success response        |
|--------|------------|--------------------------------------------|-------------------------|
| GET    | `/health`  | Health check                               | `200` `{"status":"ok"}` |
| POST   | `/shorten` | Body: `{"url": "..."}`; returns a new code | `201` with the code     |
| GET    | `/{code}`  | Redirects to the stored URL                | `307` redirect          |
 
An unknown code returns `404`.
 
## Configuration
 
Settings are read from environment variables. When running with Docker Compose, they are supplied by the `.env` file.
 
| Variable      | Default     | Description                                  |
|---------------|-------------|----------------------------------------------|
| `PORT`        | `3000`      | Port the app listens on inside the container |
| `DB_HOST`     | `localhost` | Database host (Compose sets this to `db`)    |
| `DB_PORT`     | `5432`      | Database port                                |
| `DB_NAME`     | `shortener` | Database name                                |
| `DB_USER`     | `shortener` | Database user                                |
| `DB_PASSWORD` | *(empty)*   | Database password                            |
 
The `.env` file is git-ignored so credentials are never committed. `.env.example` lists the variables that need to be set.
 
## Data persistence
 
PostgreSQL stores its files in a named Docker volume (`pgdata`), which lives outside the container. Containers can be removed and recreated without losing data:
  
## Project structure
 
```
url-shortener/
├── main.py              # FastAPI app and database code
├── requirements.txt     # Python dependencies
├── Dockerfile           # image for the app
├── docker-compose.yml   # app + PostgreSQL + volume
├── .env.example         # template for settings (copy to .env)
├── .dockerignore        # files Docker leaves out of the image
└── .gitignore           # files Git leaves out of the repo
```
 
