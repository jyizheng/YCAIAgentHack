# MCP Information Collector

A Model Context Protocol (MCP) server with multiple agents that collect information from various websites and display results on a web interface.

## Features

- **MCP Server**: Implements the Model Context Protocol with tools for data collection
- **Multiple Agents**: 
  - NewsAgent: Collects top stories from HackerNews
  - WeatherAgent: Fetches weather data for major cities
  - TechTrendsAgent: Gets trending repositories from GitHub
- **Web Dashboard**: Real-time web interface to view collected data
- **Automated Collection**: Scheduled data collection every 15 minutes

## Installation

1. Clone or download the project files
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the MCP Server

The MCP server provides tools that can be called by MCP clients:

```bash
python server.py
```

Available MCP tools:
- `collect_all`: Trigger all agents to collect data
- `get_latest_data`: Get the latest collected data from all agents
- `get_agent_status`: Get status of all agents

### Running the Web Interface

Launch the web dashboard:

```bash
python web_app.py
```

Then open http://127.0.0.1:8888 in your browser to view the dashboard.

### Testing Data Collection

You can also test the data collection functionality directly:

```bash
python simple_server.py
```

This will collect data from all agents and display the results in JSON format.

## Project Structure

```
my-mcp-server/
├── server.py              # Main MCP server
├── web_app.py             # Flask web application
├── data_store.py          # Data storage management
├── requirements.txt       # Python dependencies
├── agents/
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── news_agent.py      # HackerNews agent
│   ├── weather_agent.py   # Weather data agent
│   └── tech_trends_agent.py # GitHub trends agent
├── templates/
│   └── index.html         # Web dashboard HTML
└── static/
    ├── css/
    │   └── style.css      # Dashboard styles
    └── js/
        └── app.js         # Dashboard JavaScript
```

## Agents

### NewsAgent
Collects top stories from HackerNews API, including:
- Title and URL
- Score and author
- Number of comments

### WeatherAgent
Fetches current weather data for major cities using wttr.in API:
- Temperature and feels-like temperature
- Weather description
- Humidity, wind speed, visibility
- UV index and pressure

### TechTrendsAgent
Scrapes GitHub trending repositories:
- Repository name and URL
- Description and programming language
- Star count

## Web Dashboard

The web interface provides:
- Real-time data updates via WebSocket
- Manual refresh capability
- Agent status monitoring
- Responsive design with modern UI

## Development

To extend the system:

1. Create new agents by inheriting from `BaseAgent`
2. Implement the `collect()` method to return structured data
3. Register the agent in both `server.py` and `web_app.py`
4. Update the web interface to display the new data type

## Notes

- The system includes fallback sample data if web scraping fails
- Data is stored in memory and limited to the last 100 entries per agent
- The web interface automatically refreshes every 5 minutes via scheduled collection
