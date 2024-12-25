from typing import Optional
from db_utils import users_collection, songs_collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId


class User(BaseModel):
    name: str
    password: str
    playlists: Optional[list[dict[str, list[str]]]]

class Song(BaseModel):
    name: str
    artists: list[str]
    spotify_id: str

class Playlist(BaseModel):
    name: str
    users: list[str]
    songs: list[str]


app = FastAPI()


def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

########## Users API ##########
@app.get("/users/{name}")
async def get_user(name: str):
    """Get a specific user by name."""
    user = users_collection.find_one({"name": name})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_object(user)


@app.get("/users")
async def list_users():
    """Get all users."""
    users = list(users_collection.find())
    if not users:
        return []
    return [serialize_object(user) for user in users]


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


########## Songs API ##########
@app.get("/songs")
async def get_all_songs():
    songs = songs_collection.find()
    if not songs:
        return []
    return [serialize_object(song) for song in songs]

@app.post("/songs/add")
async def add_song(user: str, playlist: str, spotify_id: str):
    song = songs_collection.find_one({"spotify_id": spotify_id})

    if song:
        return {"message": "song already exists"}
    
    songs_collection.insert_one


########## Playlist API ##########
@app.get("/my_playlists")
async def get_my_playlists(user_name: str):
    user = get_user(user_name)

    return user["playlists"]

@app.post("/playlist/create")
async def create_playlist(user_name: str, playlist_name: str):
    user: dict = users_collection.find_one({"name": user_name})

    user_playlists: list[dict[str, str]] = user['playlists']
    user_playlists.append({playlist_name: []})

    user["playlists"] = user_playlists
    users_collection.update_one({"name": user_name}, user)

    return {"message": "Playlist created successfully", "playlist": playlist_name}