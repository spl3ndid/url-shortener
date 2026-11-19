import os
import secrets
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="URL Shortener")
urls: dict[str, str] = {}

class ShortenRequest(BaseModel):
    url:str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/shorten", status_code=201)
def shorten(body: ShortenRequest):
    code = secrets.token_hex(4)
    urls[code] = body.url
    return {"code": code, "short": f"/{code}"}

@app.get("/{code}")
def redirect(code: str):
    url = urls.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="NotFound")
    return RedirectResponse(url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",3000))
    uvicorn.run(app, host="0.0.0.0", port = port)

