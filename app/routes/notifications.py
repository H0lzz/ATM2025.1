from fastapi import APIRouter, HTTPException, Body

router = APIRouter(prefix="/notify", tags=["notifications"])

@router.post("")
def send_notification(account_number: int = Body(...), type: str = Body(...), amount: float = Body(...)):
    if type not in ("withdraw", "deposit"):
        raise HTTPException(status_code=400, detail="Tipo de transação inválido")

    message = f"Notificação: Transação '{type}' no valor de ${amount:.2f} realizada na conta {account_number}."
    print(message)
    return {"message": message, "status": "sent"}
