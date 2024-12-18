from db_utils import users_collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class User(BaseModel):
    name: str
    password: str


app = FastAPI()


def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{name}")
async def get_user(name: str):
    """Get a specific user by name."""
    user = users_collection.find_one({"name": name})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)


@app.get("/users")
async def list_users():
    """Get all users."""
    users = list(users_collection.find())
    if not users:
        return []
    return [serialize_user(user) for user in users]


@app.post("/users/create")
async def create_user(user: User):
    """Create a new user and store it in the MongoDB collection."""
    # Check if user already exists
    if users_collection.find_one({"name": user.name}):
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert the new user
    new_user = user.model_dump()
    result = users_collection.insert_one(new_user)

    # Return the created user
    new_user["_id"] = str(result.inserted_id)
    return {"message": "User created successfully", "user": new_user}
