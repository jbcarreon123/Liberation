from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


@dataclass
class Icon:
    name: str
    id: int
    chance: int | None = None


@dataclass
class Icons:
    lock: Icon
    unlock: Icon
    public: Icon
    private: Icon
    add_members: Icon
    set_user_limit: Icon
    set_permissions: Icon
    set_vc_name: Icon
    set_slowmode: Icon
    set_voice_region: Icon
    set_bitrate: Icon
    disband: Icon
    change_who_can_see: Icon
    change_who_can_make: Icon
    allowed: Icon
    inherit: Icon
    disallowed: Icon
