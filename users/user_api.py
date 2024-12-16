from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from users_utils import read_users, write_users

class User(BaseModel):
    name: str
    password: str


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{name}")
async def get_user(name: str):
    """Get a specific user by name."""
    users = read_users()
    user = next((u for u in users if u["name"] == name), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users")
async def list_users():
    """Get all users."""
    users = read_users()
    return users

@app.post("/users/create")
async def create_user(user: User):
    """Create a new user and store it in the JSON file."""
    users = read_users()

    # Check if user already exists
    if any(u["name"] == user.name for u in users):
        raise HTTPException(status_code=400, detail="User already exists")

    # Add the new user
    new_user = user.model_dump()
    users.append(new_user)
    write_users(users)

    return {"message": "User created successfully", "user": new_user}