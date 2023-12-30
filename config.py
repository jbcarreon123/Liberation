from dataclasses import dataclass
from typing import Dict, Any
from disnake import ActivityType


@dataclass
class Presence:
    Type: str
    Name: str
    State: int
    Url: str = ""


@dataclass
class Config:
    Token: str
    Prefix: str
    Presence: Presence
