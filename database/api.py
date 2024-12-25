from typing import List

from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from pymongo.synchronous.mongo_client import MongoClient


class User(BaseModel):
    name: str
    password: str
    playlists: dict[str, list[str]]  # List of playlist IDs


class Song(BaseModel):
    name: str
    artists: List[str]
    spotify_id: str


class Playlist(BaseModel):
    name: str
    users: List[str]  # List of user IDs
    songs: List[str]  # List of song IDs


app = FastAPI()

client: MongoClient = MongoClient("mongodb://localhost:27017/")
db: Database = client["mydatabase"]

users_collection: Collection = db["users"]
songs_collection: Collection = db["songs"]
playlists_collection: Collection = db["playlists"]


def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


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


@app.get("/users/{user_name}", response_model=User)
async def read_user(user_name: str):
    user = users_collection.find_one({"name": user_name})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_object(user)


@app.put("/users/{user_name}", response_model=User)
async def update_user_password(user_name: str, password: str):
    user = users_collection.find_one({"name": user_name})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user['password'] = password
    result = users_collection.update_one({"name": user_name}, {"$set": user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_object(user)


@app.delete("/users/{user_name}")
async def delete_user(user_name: str):
    result = users_collection.delete_one({"name": user_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@app.get("/songs")
async def get_all_songs():
    songs = songs_collection.find()
    if not songs:
        return []
    return [serialize_object(song) for song in songs]


@app.post("/songs/create", response_model=Song)
async def create_song(song: Song):
    """Create a new user and store it in the MongoDB collection."""
    # Check if user already exists
    if users_collection.find_one({"spotify_id": song['spotify_id']}):
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert the new user
    new_song = song.model_dump()
    users_collection.insert_one(new_song)

    # Return the created user
    return {"message": "User created successfully", "song": serialize_object(new_song)}


@app.get("/songs/{song_spotify_id}", response_model=Song)
async def read_song(song_spotify_id: str):
    song = songs_collection.find_one({"spotify_id": song_spotify_id})
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return serialize_object(song)


@app.put("/songs/{song_spotify_id}", response_model=Song)
async def update_song(song_spotify_id: str, song: Song):
    song_dict = song.model_dump()
    result = songs_collection.update_one({"spotify_id": song_spotify_id}, {"$set": song_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Song not found")
    return serialize_object(song_dict)


@app.delete("/songs/{song_spotify_id}")
async def delete_song(song_spotify_id: str):
    result = songs_collection.delete_one({"spotify_id": song_spotify_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"message": "Song deleted successfully"}


@app.get("/my_playlists")
async def get_my_playlists(user_name: str):
    user = users_collection.find_one({"name": user_name})

    return user["playlists"]


@app.post("/playlists/create", response_model=Playlist)
async def create_playlist(playlist: Playlist, user_name: str):
    """Create a new playlist and store it in the MongoDB collection."""
    # Check if user already exists
    user: User = users_collection.find_one({"name": user_name})
    if not user:
        raise HTTPException(status_code=400, detail="User isn't exists")

    # Check if playlist already exists
    if playlist['name'] in user['playlists']:
        raise HTTPException(status_code=400, detail="Playlist already exists")

    # Insert the new user
    new_playlist = playlist.model_dump()
    user['playlists'] = {"playlists": user['playlists'].append(new_playlist)}
    playlists_collection.insert_one(new_playlist)

    # Return the created user
    return {"message": "Playlist created successfully", "playlist": serialize_object(new_playlist)}


@app.get("/playlists/{playlist_id}", response_model=Playlist)
async def read_playlist(playlist_id: str):
    playlist = playlists_collection.find_one({"_id": ObjectId(playlist_id)})
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    playlist["_id"] = str(playlist["_id"])
    return playlist


@app.put("/playlists/{playlist_id}", response_model=Playlist)
async def update_playlist(playlist_id: str, playlist: Playlist):
    playlist_dict = playlist.dict()
    result = playlists_collection.update_one({"_id": ObjectId(playlist_id)}, {"$set": playlist_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Playlist not found")
    playlist_dict["_id"] = playlist_id
    return playlist_dict


@app.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: str):
    result = playlists_collection.delete_one({"_id": ObjectId(playlist_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return {"message": "Playlist deleted successfully"}
