
# Live on Render:
https://opd-token-allocation-engine.onrender.com


# Backend for this Assignment

# Assignment:
Build a backend system for hospital OPD token allocation that can stretch or shrink with demand.

## OPD Token Allocation Engine

# Problem Overview
Here’s the gist: we need a backend service that handles OPD token allocation for hospitals. Doctors work in set time slots, each with a cap on how many patients they can see. Patients want tokens through all sorts of channels—online bookings, walk-ins, paid priority, follow-ups, emergencies. The system needs to juggle real-life situations like last-minute emergencies, cancellations, and making sure nobody books beyond the limit.

# Design Approach
- Tokens are given out per slot, with strict limits—no squeezing in extra patients.
- Every request gets a priority, so the system knows who goes first.
- If there’s no room, extra requests go on a waitlist.
- It all runs in memory, which keeps things straightforward.
- The logic for giving out tokens lives separately from the API stuff, so the code stays tidy and easy to work with.

# Prioritization Logic
Every token request gets a score:
- Emergency: 100
- Paid Priority: 80
- Follow-up: 60
- Online Booking: 40
- Walk-in: 20

If a slot fills up, and someone with a higher priority comes in, they bump the lowest-priority person onto the waitlist.

## Edge Cases Handled
- Slots never go over capacity.
- Emergencies can always get in.
- If someone cancels, the system finds the next person in line.
- When a spot opens up, the waitlist moves up.

# Simulation
We stress-tested the system for a whole OPD day using Swagger UI:
- 3 doctors
- Multiple time slots
- Bookings from every source
- Emergencies popping up
- Cancellations

The results? The system stuck to priorities and handled changes smoothly.

# Tech Stack Used: 
- Python
- FastAPI
- Uvicorn

# How to run:
```bash
uvicorn app.main:app --reload
```
