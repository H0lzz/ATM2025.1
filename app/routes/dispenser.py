from fastapi import APIRouter, HTTPException, Body

router = APIRouter(prefix="/dispenser", tags=["dispenser"])

current_strategy = {"denomination": 100}

@router.post("/set-strategy")
def set_dispenser_strategy(denomination: int = Body(...)):
    if denomination not in (20, 100):
        raise HTTPException(status_code=400, detail="Somente valores de 20 ou 100 são aceitos")
    current_strategy["denomination"] = denomination
    return {"message": f"Estratégia de dispensador atualizada para ${denomination}."}

@router.get("/strategy")
def get_dispenser_strategy():
    return {"current_strategy": current_strategy["denomination"]}
