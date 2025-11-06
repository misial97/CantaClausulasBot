from pydantic import BaseModel, Field

class PlayerTeam(BaseModel):
    id: int
    name: str
    slug: str

class Player(BaseModel):
    id: int
    name: str
    #position: str
    team: PlayerTeam

class PlayerResponse(BaseModel):
    status: int
    data: Player