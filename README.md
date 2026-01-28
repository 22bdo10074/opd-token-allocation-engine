# OPD Token Allocation Engine

## Problem Overview
This project implements a backend service for allocating OPD tokens in a hospital.
Doctors operate in fixed time slots with limited capacity. Patients can request tokens
from multiple sources such as online booking, walk-ins, paid priority, follow-ups,
and emergencies.

The system dynamically handles real-world scenarios like emergency insertions,
cancellations, and capacity limits.

---

## Design Approach
- Slot-based allocation with hard capacity limits
- Priority-driven decision making
- Waitlist mechanism for overflow handling
- In-memory data store for simplicity and clarity

The core allocation logic is separated from API handling to keep the system clean
and maintainable.

---

## Prioritization Logic
Each token source is mapped to a priority score:

- Emergency: 100
- Paid Priority: 80
- Follow-up: 60
- Online Booking: 40
- Walk-in: 20

When a slot is full, a higher-priority request can replace a lower-priority token,
which is then moved to the waitlist.

---

## Edge Cases Handled
- Slot capacity enforcement (no overflow)
- Emergency token insertion
- Automatic reallocation on cancellation
- Waitlist promotion when capacity becomes available

---

## Simulation
A full OPD day was simulated using Swagger UI with:
- 3 doctors
- Multiple time slots
- Mixed booking sources
- Emergency insertions
- Cancellations

The simulation demonstrates correct prioritization and dynamic reallocation.

---

## Tech Stack
- Python
- FastAPI
- Uvicorn

---

## How to Run
```bash
uvicorn app.main:app --reload
