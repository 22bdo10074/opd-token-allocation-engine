from typing import Dict, List
from app.models import Doctor, Slot, Token

# In-memory storage (temporary database)

doctors: Dict[str, Doctor] = {}
slots: Dict[str, Slot] = {}
tokens: Dict[str, Token] = {}

# slot_id -> list of token_ids (waitlisted)
waitlists: Dict[str, List[str]] = {}
from app.models import Doctor, Slot

# Seed Doctors
doctors["D1"] = Doctor(doctor_id="D1", name="Dr. Sharma")
doctors["D2"] = Doctor(doctor_id="D2", name="Dr. Mehta")
doctors["D3"] = Doctor(doctor_id="D3", name="Dr. Khan")

# Seed Slots
slots["S1"] = Slot(
    slot_id="S1",
    doctor_id="D1",
    start_time="09:00",
    end_time="10:00",
    max_capacity=3,
    active_capacity=3
)

slots["S2"] = Slot(
    slot_id="S2",
    doctor_id="D2",
    start_time="10:00",
    end_time="11:00",
    max_capacity=2,
    active_capacity=2
)

slots["S3"] = Slot(
    slot_id="S3",
    doctor_id="D3",
    start_time="11:00",
    end_time="12:00",
    max_capacity=2,
    active_capacity=2
)
