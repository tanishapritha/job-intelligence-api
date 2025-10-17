from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "welcome"}

@app.get("/items")
async def items():
    return {"message": "welcome to items"}