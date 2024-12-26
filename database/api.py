from inspect import stack
from json import dumps
from logging import getLogger
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from pymongo.synchronous.mongo_client import MongoClient


class User(BaseModel):
    name: str
    password: str
    playlists: list[dict[str, list[str]]]  # List of playlist IDs


class Playlist(BaseModel):
    name: str
    owner: str
    shared_users: List[str] = []  # List of user IDs
    songs: List[str] = []  # List of song IDs


app = FastAPI()
logger = getLogger('uvicorn.error')

client: MongoClient = MongoClient("mongodb://localhost:27017/")
db: Database = client["mydatabase"]

users_collection: Collection = db["users"]
songs_collection: Collection = db["songs"]
playlists_collection: Collection = db["playlists"]


def format_log(message: dict):
    filename = stack()[0].filename.split("/")[-1]
    func = stack()[1].function
    log = {"filename": filename, "function": func, "message": message}
    return logger.info(log)


def serialize_object(obj) -> dict:
    obj["_id"] = str(obj["_id"])
    return obj


def serialize_user(user) -> dict:
    user["_id"] = str(user["_id"])
    user["playlists"] = [serialize_object(playlist) for playlist in user["playlists"]]
    return user


def get_all_playlists() -> list[dict]:
    playlists = list(playlists_collection.find())
    if not playlists:
        return []
    return [serialize_object(playlist) for playlist in playlists]


def get_all_users():
    users = list(users_collection.find())
    if not users:
        return []
    return [serialize_user(user) for user in users]


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users")
async def list_users():
    """Get all users."""
    all_users = get_all_users()
    format_log({"all users": all_users})
    return all_users


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

    format_log({"new user": new_user})
    format_log({"updated users": get_all_users()})
    return {"message": "User created successfully", "user": new_user}


@app.get("/users/{user_name}", response_model=User)
async def read_user(user_name: str):
    user = users_collection.find_one({"name": user_name})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)


@app.put("/users/{user_name}", response_model=User)
async def update_user_password(user_name: str, password: str):
    user = users_collection.find_one({"name": user_name})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    format_log({"user": user})
    user['password'] = password
    result = users_collection.update_one({"name": user_name}, {"$set": user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    format_log({"updated users": get_all_users()})
    return serialize_user(user)


@app.delete("/users/{user_name}")
async def delete_user(user_name: str):
    result = users_collection.delete_one({"name": user_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@app.get("/my_playlists")
async def get_my_playlists(user_name: str):
    user = users_collection.find_one({"name": user_name})
    format_log({"user": user})
    return [serialize_object(playlist) for playlist in user["playlists"]]


@app.post("/playlists/create")
async def create_playlist(playlist_name: str, user_name: str):
    """Create a new playlist and store it in the MongoDB collection."""
    playlist = playlists_collection.find_one({"name": playlist_name})
    if playlist:
        raise HTTPException(status_code=400, detail="Playlist already exists")

    user = users_collection.find_one({"name": user_name})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_playlist = Playlist(name=playlist_name, owner=user_name).model_dump()
    playlists_collection.insert_one(new_playlist)

    all_playlists = dumps(get_all_playlists())
    format_log({"all playlists": all_playlists})

    if not user['playlists']:
        user['playlists'] = []

    user['playlists'].append(new_playlist)
    users_collection.update_one({"name": user_name}, {"$set": user})

    all_users = dumps(get_all_users())
    format_log({"all users": all_users})

    return {
        "message": "Playlist created successfully",
        "playlist": serialize_object(new_playlist),
        "user": serialize_user(user)}


@app.get("/playlists/{playlist_name}")
async def read_playlist(playlist_name: str):
    playlist = playlists_collection.find_one({"name": playlist_name})
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return serialize_object(playlist)


@app.delete("/playlists/{playlist_name}")
async def delete_playlist(playlist_name: str):
    result = playlists_collection.delete_one({"name": playlist_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return {"message": "Playlist deleted successfully"}
