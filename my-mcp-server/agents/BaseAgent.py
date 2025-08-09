import asyncio
import aiohttp
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class BaseAgent(ABC):
    def __init__(self, data_store, name: str):
        self.data_store = data_store
        self.name = name
        self.last_collection_time = None
        self.last_item_count = 0
        self.status = "idle"
        
    @abstractmethod
    async def collect(self) -> List[Dict[str, Any]]:
        pass
    
    async def fetch_url(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                return await response.text()
    
    def parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')
    
    async def store_results(self, data: List[Dict[str, Any]]):
        self.data_store.store_data(self.name, data)
        self.last_collection_time = datetime.now().isoformat()
        self.last_item_count = len(data)
        self.status = "success"
    
    async def run_collection(self) -> List[Dict[str, Any]]:
        try:
            self.status = "collecting"
            data = await self.collect()
            await self.store_results(data)
            return data
        except Exception as e:
            self.status = f"error: {str(e)}"
            raise
