# Copyright (c) 2025 Miguel Sierra
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import zoneinfo


MADRID_TZ = zoneinfo.ZoneInfo("Europe/Madrid")


class Team(BaseModel):
    id: int
    name: str
    icon: str


class ClauseEntry(BaseModel):
    player: int
    from_: Team = Field(alias="from")
    to: Team
    amount: int
    type: Literal["clause"]


class Movement(BaseModel):
    type: Literal["transfer"]
    title: str
    content: List[ClauseEntry]
    date: int # epoch seconds
    fixed: bool
    author: Optional[str] = None
    @property
    def date_dt(self) -> datetime:
        # Fecha en horario de Madrid
        return datetime.fromtimestamp(self.date, tz=MADRID_TZ)


class MovementsResponse(BaseModel):
    status: int
    data: List[Movement]