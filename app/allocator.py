import uuid
from typing import Optional

from app.models import Token, TokenSource, TokenStatus
from app.storage import slots, tokens, waitlists
def get_priority(source: TokenSource) -> int:
    if source == TokenSource.EMERGENCY:
        return 100
    if source == TokenSource.PAID:
        return 80
    if source == TokenSource.FOLLOW_UP:
        return 60
    if source == TokenSource.ONLINE:
        return 40
    if source == TokenSource.WALK_IN:
        return 20
    return 0
def find_lowest_priority_token(slot_id: str) -> Optional[Token]:
    slot_tokens = [
        t for t in tokens.values()
        if t.slot_id == slot_id and t.status == TokenStatus.ALLOCATED
    ]

    if not slot_tokens:
        return None

    return min(slot_tokens, key=lambda t: t.priority_score)
def allocate_token(
    patient_id: str,
    doctor_id: str,
    slot_id: str,
    source: TokenSource
) -> Token:

    slot = slots.get(slot_id)
    if not slot:
        raise ValueError("Invalid slot")

    priority = get_priority(source)

    allocated_tokens = [
        t for t in tokens.values()
        if t.slot_id == slot_id and t.status == TokenStatus.ALLOCATED
    ]

    # Case 1: Slot has capacity
    if len(allocated_tokens) < slot.active_capacity:
        token = Token(
            token_id=str(uuid.uuid4()),
            patient_id=patient_id,
            doctor_id=doctor_id,
            slot_id=slot_id,
            source=source,
            priority_score=priority,
            status=TokenStatus.ALLOCATED
        )
        tokens[token.token_id] = token
        return token

    # Case 2: Slot full → try reallocation
    lowest = find_lowest_priority_token(slot_id)

    if lowest and priority > lowest.priority_score:
        lowest.status = TokenStatus.WAITLISTED
        waitlists.setdefault(slot_id, []).append(lowest.token_id)

        token = Token(
            token_id=str(uuid.uuid4()),
            patient_id=patient_id,
            doctor_id=doctor_id,
            slot_id=slot_id,
            source=source,
            priority_score=priority,
            status=TokenStatus.ALLOCATED
        )
        tokens[token.token_id] = token
        return token

    # Case 3: Cannot allocate → waitlist
    token = Token(
        token_id=str(uuid.uuid4()),
        patient_id=patient_id,
        doctor_id=doctor_id,
        slot_id=slot_id,
        source=source,
        priority_score=priority,
        status=TokenStatus.WAITLISTED
    )
    tokens[token.token_id] = token
    waitlists.setdefault(slot_id, []).append(token.token_id)
    return token
def cancel_token(token_id: str):
    token = tokens.get(token_id)
    if not token:
        return

    token.status = TokenStatus.CANCELLED

    slot_waitlist = waitlists.get(token.slot_id, [])
    if slot_waitlist:
        next_token_id = slot_waitlist.pop(0)
        next_token = tokens[next_token_id]
        next_token.status = TokenStatus.ALLOCATED
