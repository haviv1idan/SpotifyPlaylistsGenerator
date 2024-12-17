from functools import lru_cache
from pymongo.synchronous.mongo_client import MongoClient
from pymongo.synchronous.database import Database
from pymongo.synchronous.collection import Collection


client: MongoClient = MongoClient("mongodb://localhost:27017/")
db: Database = client["mydatabase"]

users_collection: Collection = db["users"]
songs_collection: Collection = db["songs"]

def insert_user(name, password):
    # Insert a user
    user = {"name": name, "password": password}
    result = users_collection.insert_one(user)
    print(f"User inserted with ID: {result.inserted_id}")

def insert_song(name, spotify_id, artists):
    # Insert a song
    song = {"name": name, "spotify_id": spotify_id, "artists": artists}
    result = songs_collection.insert_one(song)
    print(f"Song inserted with ID: {result.inserted_id}")

def get_all_users():
    # Get all users
    users = users_collection.find()
    for user in users:
        print(user)

def get_all_songs():
    # Get all songs
    songs = songs_collection.find()
    for song in songs:
        print(song)

def update_user_password(name, new_password):
    # Update a user's password
    result = users_collection.update_one(
        {"name": name},
        {"$set": {"password": new_password}}
    )
    if result.matched_count:
        print(f"Password for {name} updated.")
    else:
        print("User not found.")

def delete_user(name):
    # Delete a user
    result = users_collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"User {name} deleted.")
    else:
        print("User not found.")

def delete_song(spotify_id):
    # Delete a song
    result = songs_collection.delete_one({"spotify_id": spotify_id})
    if result.deleted_count:
        print(f"Song with ID {spotify_id} deleted.")
    else:
        print("Song not found.")

