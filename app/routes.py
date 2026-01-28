from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models import TokenSource, Token
from app.allocator import allocate_token, cancel_token
from app.storage import tokens, slots
router = APIRouter()
class CreateTokenRequest(BaseModel):
    patient_id: str
    doctor_id: str
    slot_id: str
    source: TokenSource
@router.post("/tokens", response_model=Token)
def create_token(request: CreateTokenRequest):
    try:
        token = allocate_token(
            patient_id=request.patient_id,
            doctor_id=request.doctor_id,
            slot_id=request.slot_id,
            source=request.source
        )
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.post("/tokens/{token_id}/cancel")
def cancel(token_id: str):
    if token_id not in tokens:
        raise HTTPException(status_code=404, detail="Token not found")

    cancel_token(token_id)
    return {"status": "cancelled"}
@router.get("/slots/{slot_id}/tokens")
def get_slot_tokens(slot_id: str):
    if slot_id not in slots:
        raise HTTPException(status_code=404, detail="Slot not found")

    return [
        t for t in tokens.values()
        if t.slot_id == slot_id
    ]
