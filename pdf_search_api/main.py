from fastapi import FastAPI
from controllers.search_controller import router as search_router
from controllers.auth_controller import router as auth_router

app = FastAPI(title="PDF Search API (Minimal)")

app.include_router(search_router)
app.include_router(auth_router)

@app.get("/")
def health():
    return {"status": "ok"}
