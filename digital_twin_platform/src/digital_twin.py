from dataclasses import dataclass
from typing import Dict, List
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

@dataclass
class ProcessState:
    machine_id: str
    temperature: float
    pressure: float
    vibration: float
    power_consumption: float
    timestamp: pd.Timestamp

class DigitalTwin:
    def __init__(self):
        self.historical_data: Dict[str, List[ProcessState]] = {}
        self.anomaly_detector = IsolationForest(contamination=0.1)
    
    def update_state(self, state: ProcessState):
        if state.machine_id not in self.historical_data:
            self.historical_data[state.machine_id] = []
        self.historical_data[state.machine_id].append(state)
    
    def predict_maintenance(self, machine_id: str) -> float:
        if machine_id not in self.historical_data:
            return 0.0
        
        data = pd.DataFrame([vars(x) for x in self.historical_data[machine_id]])
        return self.anomaly_detector.fit_predict(data[['temperature', 'pressure', 'vibration', 'power_consumption']])