from fastapi import FastAPI

app = FastAPI(title="Open Manus AI Agent")

@app.get("/")
def root():
    return {"message": "Open Manus AI Agent backend is running."}
