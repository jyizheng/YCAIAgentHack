import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { NewsAgent } from './agents/newsAgent.js';
import { WeatherAgent } from './agents/weatherAgent.js';
import { TechTrendsAgent } from './agents/techTrendsAgent.js';
import { DataStore } from './dataStore.js';
import cron from 'node-cron';

class MCPInfoServer {
  constructor() {
    this.server = new Server(
      {
        name: "info-collector",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );
    
    this.dataStore = new DataStore();
    this.agents = [];
    this.initializeAgents();
    this.setupTools();
    this.scheduleDataCollection();
  }

  initializeAgents() {
    this.agents.push(new NewsAgent(this.dataStore));
    this.agents.push(new WeatherAgent(this.dataStore));
    this.agents.push(new TechTrendsAgent(this.dataStore));
    
    console.error("Initialized agents:", this.agents.map(a => a.name));
  }

  setupTools() {
    this.server.setRequestHandler("tools/list", async () => ({
      tools: [
        {
          name: "collect_all",
          description: "Trigger all agents to collect data",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
        {
          name: "get_latest_data",
          description: "Get the latest collected data from all agents",
          inputSchema: {
            type: "object",
            properties: {
              agent: {
                type: "string",
                description: "Optional: specific agent name to get data from",
              },
            },
          },
        },
        {
          name: "get_agent_status",
          description: "Get status of all agents",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
      ],
    }));

    this.server.setRequestHandler("tools/call", async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case "collect_all":
          return await this.collectAll();
        case "get_latest_data":
          return this.getLatestData(args.agent);
        case "get_agent_status":
          return this.getAgentStatus();
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  async collectAll() {
    const results = [];
    for (const agent of this.agents) {
      try {
        console.error(`Collecting data from ${agent.name}...`);
        const data = await agent.collect();
        results.push({ agent: agent.name, status: "success", itemsCollected: data.length });
      } catch (error) {
        console.error(`Error collecting from ${agent.name}:`, error);
        results.push({ agent: agent.name, status: "error", error: error.message });
      }
    }
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(results, null, 2),
        },
      ],
    };
  }

  getLatestData(agentName) {
    const data = agentName 
      ? this.dataStore.getDataByAgent(agentName)
      : this.dataStore.getAllData();
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(data, null, 2),
        },
      ],
    };
  }

  getAgentStatus() {
    const status = this.agents.map(agent => ({
      name: agent.name,
      lastCollection: agent.lastCollectionTime,
      itemsCollected: agent.lastItemCount || 0,
      status: agent.status || "idle",
    }));
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(status, null, 2),
        },
      ],
    };
  }

  scheduleDataCollection() {
    cron.schedule('*/15 * * * *', async () => {
      console.error("Scheduled data collection started...");
      await this.collectAll();
    });
    console.error("Data collection scheduled every 15 minutes");
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("MCP Info Collector Server started");
    
    await this.collectAll();
  }
}

const server = new MCPInfoServer();
server.start().catch(console.error);