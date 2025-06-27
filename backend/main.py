"""FastAPI application entry point for Codex Booster."""

from fastapi import FastAPI

app = FastAPI(title="Codex Booster")

# TODO: include routers for agents and authentication

@app.get("/")
async def root():
    return {"message": "Codex Booster API"}
