# Copyright (c) 2025 Miguel Sierra
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

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