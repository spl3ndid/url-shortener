import os
import secrets
from contextlib import asynccontextmanager

import psycopg
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "shortener")
DB_USER = os.environ.get("DB_USER", "shortener")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


def get_conn():
    return psycopg.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create the table if it doesn't exist
    with get_conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS urls (code TEXT PRIMARY KEY, url TEXT NOT NULL)"
        )
    yield


app = FastAPI(title="URL Shortener", lifespan=lifespan)


class ShortenRequest(BaseModel):
    url: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten", status_code=201)
def shorten(body: ShortenRequest):
    code = secrets.token_hex(4)
    with get_conn() as conn:
        conn.execute("INSERT INTO urls (code, url) VALUES (%s, %s)", (code, body.url))
    return {"code": code, "short": f"/{code}"}


@app.get("/{code}")
def redirect(code: str):
    with get_conn() as conn:
        row = conn.execute("SELECT url FROM urls WHERE code = %s", (code,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Not found")
    return RedirectResponse(row[0])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
