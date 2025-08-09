#!/usr/bin/env python3
import asyncio
import json
import sys
from typing import Any, Dict, List
from datetime import datetime
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from agents.CryptoNewsAgent import CryptoNewsAgent
from agents.CrunchbaseCryptoAgent import CrunchbaseCryptoAgent
from agents.CryptoMarketAgent import CryptoMarketAgent
from data_store import DataStore

class MCPInfoServer:
    def __init__(self):
        self.server = Server("info-collector")
        self.data_store = DataStore()
        self.agents = []
        self.scheduler = AsyncIOScheduler()
        self.initialize_agents()
        self.setup_handlers()
        self.schedule_data_collection()
        
    def initialize_agents(self):
        self.agents.append(CryptoNewsAgent(self.data_store))
        self.agents.append(CrunchbaseCryptoAgent(self.data_store))
        self.agents.append(CryptoMarketAgent(self.data_store))
        print(f"Initialized {len(self.agents)} agents", file=sys.stderr)
        
    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="collect_all",
                    description="Trigger all agents to collect data",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                types.Tool(
                    name="get_latest_data",
                    description="Get the latest collected data from all agents",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent": {
                                "type": "string",
                                "description": "Optional: specific agent name to get data from",
                            },
                        },
                    },
                ),
                types.Tool(
                    name="get_agent_status",
                    description="Get status of all agents",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            if name == "collect_all":
                result = await self.collect_all()
            elif name == "get_latest_data":
                result = self.get_latest_data(arguments.get("agent"))
            elif name == "get_agent_status":
                result = self.get_agent_status()
            else:
                raise ValueError(f"Unknown tool: {name}")
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def collect_all(self) -> Dict[str, Any]:
        results = []
        for agent in self.agents:
            try:
                print(f"Collecting data from {agent.name}...", file=sys.stderr)
                data = await agent.collect()
                results.append({
                    "agent": agent.name,
                    "status": "success",
                    "items_collected": len(data),
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error collecting from {agent.name}: {e}", file=sys.stderr)
                results.append({
                    "agent": agent.name,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        return {"collection_results": results}
    
    def get_latest_data(self, agent_name: str = None) -> Dict[str, Any]:
        if agent_name:
            data = self.data_store.get_data_by_agent(agent_name)
        else:
            data = self.data_store.get_all_data()
        return {"data": data, "timestamp": datetime.now().isoformat()}
    
    def get_agent_status(self) -> Dict[str, Any]:
        status = []
        for agent in self.agents:
            status.append({
                "name": agent.name,
                "last_collection": agent.last_collection_time,
                "items_collected": agent.last_item_count,
                "status": agent.status,
            })
        return {"agents_status": status}
    
    def schedule_data_collection(self):
        self.scheduler.add_job(
            self.collect_all,
            'interval',
            minutes=15,
            id='collect_data',
            replace_existing=True
        )
        print("Data collection scheduled every 15 minutes", file=sys.stderr)
    
    async def run(self):
        self.scheduler.start()
        await self.collect_all()
        
        # Run the MCP server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                {}
            )

async def main():
    server = MCPInfoServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
