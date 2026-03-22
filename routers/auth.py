from fastapi import FastAPI, APIRouter

router = APIRouter()


@router.get("/auth")
async def auth():
    return {"user": "authentication"}

