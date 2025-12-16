from urllib import request

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional,List
from uuid import UUID,uuid4
from fastapi import HTTPException
import random

from pydantic_core.core_schema import none_schema

app = FastAPI()
class CreateRoomRequest(BaseModel):
    name:str

rooms={}

@app.post("/room/create")
def create_room(request:"CreateRoomRequest" ):
    room_id = str(uuid4())[:6]
    player_id = str(uuid4())
    rooms[room_id]={'status':'WAITING',
                       'players': {}
    }
    rooms[room_id]["players"][player_id] = {
        "name":request.name,
        "role":None,
        "score":0


    }
    return {
        "message":"Room created",
        "roomId":room_id,
        "playerId":player_id
    }
class JoinRoomRequest(BaseModel):
    room_id: str
    name: str

@app.post("/room/join")
def join_room(request:JoinRoomRequest):
    if request.room_id not in rooms:
        raise HTTPException(status_code=404,detail="Room not found")
    if len(rooms[request.room_id]["players"])>=4:
        raise HTTPException(status_code=409,detail="Room full")


    player_id =str(uuid4())
    rooms[request.room_id]["players"][player_id]={
        "name":request.name,
        "role":None,
        "score":0

    }
    return{
        "message":"Room joined",
        "roomId":request.room_id,
        "playerId":player_id


    }

@app.get("/room/players/{room_id}")
def get_players(room_id:str):
    if room_id not in rooms:
        raise HTTPException(status_code=404,detail="Room not found")
    allplayers=rooms[room_id]["players"]
    namesonly=[]
    for playerdata in allplayers.values():
        namesonly.append(playerdata["name"])
    return namesonly


@app.post("/room/assign/{room_id}")
def assign_roles(room_id:str):
    if room_id not in rooms:
        raise HTTPException(status_code=404,detail="Room not found")

    if len(rooms[room_id]["players"])<4:
        raise HTTPException(status_code=409,detail="4 players needed to start the game")
    roles = ['Raja', 'Mantri', 'Chor','Sipahi']


    random.shuffle(roles)
    for pid,role in zip(rooms[room_id]["players"],roles):
        rooms[room_id]["players"][pid]["role"] = role
        if role=='Mantri':
            rooms[room_id]["mantri_id"]=pid

    rooms[room_id]["status"] = "GUESSING"

    return {"message": "Roles assigned"}

@app.get("/role/me/{room_id}/{player_id}")
def display_roles(room_id:str,player_id:str):
    if room_id not in rooms:
        raise HTTPException(status_code=404,detail="Room not found")
    roles=rooms[room_id]["players"][player_id]["role"]
    return roles

class MakeTheGuess (BaseModel):
    room_id: str
    player_id: str
    suspect_id: str


@app.post("/guess")
def MakeGuess(request:MakeTheGuess):
    if request.room_id not in rooms:
        raise HTTPException(status_code=404,detail="Room not found")
    if request.player_id != rooms[request.room_id]["mantri_id"]:
        raise HTTPException(status_code=401,detail="Someone other than Mantri has made the guess")
    suspects_role=rooms[request.room_id]["players"][request.suspect_id]["role"]

    if suspects_role=='Chor':
        print('Mantri won the game')
        mantri_won=True
    else:
        print('Chor won the game')
        mantri_won=False

    for player_id in rooms[request.room_id]["players"]:
        role=rooms[request.room_id]["players"][player_id]["role"]
        if role=='Raja':
            rooms[request.room_id]["players"][player_id]["score"]=1000
        elif role=='Sipahi':
            rooms[request.room_id]["players"][player_id]["score"]=500
        elif role=='Mantri':
            if mantri_won:
                rooms[request.room_id]["players"][player_id]["score"]=800
            else:
                rooms[request.room_id]["players"][player_id]["score"]=0
        elif role=='Chor':
            if mantri_won:
                rooms[request.room_id]["players"][player_id]["score"]=0
            else:
                rooms[request.room_id]["players"][player_id]["score"]=800

    rooms[request.room_id]["status"]="FINISHED"

    return {
        "message":"Game over",
        "mantri_won":mantri_won,
        "suspects_role":suspects_role,



    }


















if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8650)



