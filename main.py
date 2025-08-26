from fastapi import FastAPI
from auth_routes import router as auth_router
from notes_routes import router as notes_router

app = FastAPI(title="Notes API")

app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/")
def read_root():
    return {"message": "Notes API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
