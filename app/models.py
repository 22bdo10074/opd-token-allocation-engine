from enum import Enum
from pydantic import BaseModel
from typing import Optional


class TokenSource(str, Enum):
    ONLINE = "online"
    WALK_IN = "walk_in"
    PAID = "paid"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"


class TokenStatus(str, Enum):
    ALLOCATED = "allocated"
    WAITLISTED = "waitlisted"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    COMPLETED = "completed"


class Doctor(BaseModel):
    doctor_id: str
    name: str


class Slot(BaseModel):
    slot_id: str
    doctor_id: str
    start_time: str
    end_time: str
    max_capacity: int
    active_capacity: int


class Token(BaseModel):
    token_id: str
    patient_id: str
    doctor_id: str
    slot_id: str
    source: TokenSource
    priority_score: int
    status: TokenStatus
