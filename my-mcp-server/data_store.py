import json
from datetime import datetime
from typing import Dict, List, Any
from threading import Lock

class DataStore:
    def __init__(self):
        self.data = {}
        self.lock = Lock()
        
    def store_data(self, agent_name: str, data: List[Dict[str, Any]]):
        with self.lock:
            if agent_name not in self.data:
                self.data[agent_name] = []
            
            entry = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            self.data[agent_name].append(entry)
            
            if len(self.data[agent_name]) > 100:
                self.data[agent_name] = self.data[agent_name][-100:]
    
    def get_data_by_agent(self, agent_name: str) -> List[Dict[str, Any]]:
        with self.lock:
            if agent_name in self.data and self.data[agent_name]:
                return self.data[agent_name][-1]["data"]
            return []
    
    def get_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        with self.lock:
            result = {}
            for agent_name, entries in self.data.items():
                if entries:
                    result[agent_name] = entries[-1]["data"]
            return result
    
    def get_historical_data(self, agent_name: str = None, limit: int = 10) -> Dict[str, Any]:
        with self.lock:
            if agent_name:
                if agent_name in self.data:
                    return {agent_name: self.data[agent_name][-limit:]}
                return {agent_name: []}
            else:
                result = {}
                for name, entries in self.data.items():
                    result[name] = entries[-limit:]
                return result