from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session
from src.digital_twin import DigitalTwin, ProcessState
from src.database import SessionLocal, MachineReading
import uuid

app = FastAPI(title="Industrial Digital Twin Platform")
twin = DigitalTwin()

class StateUpdate(BaseModel):
    machine_id: str = Field(..., min_length=1, max_length=50, description="Unique machine identifier")
    temperature: float = Field(..., ge=0, le=150, description="Temperature in Celsius")
    pressure: float = Field(..., ge=0, le=1000, description="Pressure in PSI")
    vibration: float = Field(..., ge=0, le=10, description="Vibration amplitude")
    power_consumption: float = Field(..., ge=0, description="Power consumption in watts")

    model_config = {
        "json_schema_extra": {
            "example": {
                "machine_id": "robot_001",
                "temperature": 75.5,
                "pressure": 100.2,
                "vibration": 0.5,
                "power_consumption": 150.0
            }
        }
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/update_state")
async def update_state(state: StateUpdate, db: Session = Depends(get_db)):
    """Update the state of a machine in the digital twin"""
    process_state = ProcessState(
        machine_id=state.machine_id,
        temperature=state.temperature,
        pressure=state.pressure,
        vibration=state.vibration,
        power_consumption=state.power_consumption,
        timestamp=pd.Timestamp.now()
    )
    
    twin.update_state(process_state)
    
    db_reading = MachineReading(
        id=str(uuid.uuid4()),
        **state.dict(),
        timestamp=process_state.timestamp
    )
    db.add(db_reading)
    db.commit()
    
    return {"status": "success", "timestamp": process_state.timestamp}

@app.get("/maintenance/{machine_id}")
async def get_maintenance_prediction(machine_id: str):
    """
    Get maintenance prediction for a specific machine
    """
    prediction = twin.predict_maintenance(machine_id)
    return {"machine_id": machine_id, "maintenance_needed": bool(prediction < 0)}

@app.get("/machine/{machine_id}/history")
async def get_machine_history(machine_id: str):
    """
    Get historical data for a specific machine
    """
    if machine_id not in twin.historical_data:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    history = twin.historical_data[machine_id]
    return {
        "machine_id": machine_id,
        "data_points": len(history),
        "history": [vars(state) for state in history]
    }

@app.get("/machines")
async def list_machines():
    """
    List all machines in the digital twin
    """
    return {
        "machines": list(twin.historical_data.keys()),
        "total_count": len(twin.historical_data)
    }

@app.delete("/machine/{machine_id}")
async def delete_machine_data(machine_id: str):
    """
    Delete all data for a specific machine
    """
    if machine_id not in twin.historical_data:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    del twin.historical_data[machine_id]
    return {"status": "success", "message": f"Deleted all data for machine {machine_id}"}

@app.get("/")
async def root():
    """Root endpoint for the Digital Twin Platform"""
    return {
        "status": "online",
        "title": "Industrial Digital Twin Platform",
        "documentation": "/docs",
        "available_endpoints": [
            "/update_state",
            "/maintenance/{machine_id}",
            "/machine/{machine_id}/history",
            "/machines"
        ]
    }