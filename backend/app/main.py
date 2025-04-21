from fastapi import FastAPI
from endpoints import test  # Remove the dot

app = FastAPI()

app.include_router(test.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)