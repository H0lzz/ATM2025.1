from fastapi import APIRouter, HTTPException, Body
from typing import Optional

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/auth/biometric")
def authenticate_biometric(account_number: int = Body(...), biometric_token: Optional[str] = Body(None), pin: Optional[int] = Body(None)):
    if account_number >= 1000:
        raise HTTPException(status_code=403, detail="Conta não é administrativa")

    biometric_success = biometric_token == "VALID_BIOMETRIC"
    if biometric_success:
        return {"status": "authenticated", "method": "biometric"}

    if pin == 1234:
        return {"status": "authenticated", "method": "pin"}

    raise HTTPException(status_code=401, detail="Falha na autenticação biométrica e PIN inválido")
