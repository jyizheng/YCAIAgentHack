from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import asyncio
import threading
import time
from datetime import datetime
from data_store import DataStore
from agents.CryptoNewsAgent import CryptoNewsAgent
from agents.CryptoMarketAgent import CryptoMarketAgent
from agents.CrunchbaseCryptoAgent import CrunchbaseCryptoAgent
from agents.YCInvestmentAgent import YCInvestmentAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

data_store = DataStore()
agents = []

def initialize_agents():
    global agents
    agents = [
        CryptoNewsAgent(data_store),
        CryptoMarketAgent(data_store),
        CrunchbaseCryptoAgent(data_store)
    ]

def run_async_collection():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def collect():
        results = []
        for agent in agents:
            try:
                data = await agent.collect()
                results.append({
                    "agent": agent.name,
                    "status": "success",
                    "count": len(data)
                })
            except Exception as e:
                results.append({
                    "agent": agent.name,
                    "status": "error",
                    "error": str(e)
                })
        return results
    
    return loop.run_until_complete(collect())

def run_single_agent_collection(agent):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def collect_single():
        try:
            data = await agent.collect()
            return {
                "agent": agent.name,
                "status": "success",
                "data": data,
                "count": len(data)
            }
        except Exception as e:
            return {
                "agent": agent.name,
                "status": "error",
                "error": str(e),
                "data": []
            }
    
    return loop.run_until_complete(collect_single())

def background_collector():
    while True:
        try:
            results = run_async_collection()
            socketio.emit('update', {
                'timestamp': datetime.now().isoformat(),
                'results': results,
                'data': data_store.get_all_data()
            })
        except Exception as e:
            print(f"Background collection error: {e}")
        time.sleep(300)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/investment')
def investment_analysis():
    return render_template('investment_analysis.html')

@app.route('/api/data')
def get_data():
    return jsonify({
        'data': data_store.get_all_data(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/collect', methods=['POST'])
def trigger_collection():
    try:
        results = run_async_collection()
        return jsonify({
            'status': 'success',
            'results': results,
            'data': data_store.get_all_data()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/agents')
def get_agents_status():
    status = []
    for agent in agents:
        status.append({
            'name': agent.name,
            'last_collection': agent.last_collection_time,
            'items': agent.last_item_count,
            'status': agent.status
        })
    return jsonify({'agents': status})

@app.route('/api/crypto-news', methods=['POST'])
def get_crypto_news():
    try:
        crypto_news_agent = next((agent for agent in agents if agent.name == "CryptoNewsAgent"), None)
        if not crypto_news_agent:
            return jsonify({
                'status': 'error',
                'error': 'Crypto News agent not found'
            }), 404
        
        results = run_single_agent_collection(crypto_news_agent)
        return jsonify({
            'status': 'success',
            'agent': 'CryptoNewsAgent',
            'data': results['data'],
            'count': len(results['data']),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/crypto-market', methods=['POST'])
def get_crypto_market():
    try:
        crypto_market_agent = next((agent for agent in agents if agent.name == "CryptoMarketAgent"), None)
        if not crypto_market_agent:
            return jsonify({
                'status': 'error',
                'error': 'Crypto Market agent not found'
            }), 404
        
        results = run_single_agent_collection(crypto_market_agent)
        return jsonify({
            'status': 'success',
            'agent': 'CryptoMarketAgent',
            'data': results['data'],
            'count': len(results['data']),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/crunchbase-crypto', methods=['POST'])
def get_crunchbase_crypto():
    try:
        crunchbase_agent = next((agent for agent in agents if agent.name == "CrunchbaseCryptoAgent"), None)
        if not crunchbase_agent:
            return jsonify({
                'status': 'error',
                'error': 'Crunchbase Crypto agent not found'
            }), 404
        
        results = run_single_agent_collection(crunchbase_agent)
        return jsonify({
            'status': 'success',
            'agent': 'CrunchbaseCryptoAgent',
            'data': results['data'],
            'count': len(results['data']),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@socketio.on('connect')
def handle_connect():
    emit('connected', {
        'message': 'Connected to MCP Info Collector',
        'data': data_store.get_all_data()
    })

@socketio.on('request_update')
def handle_update_request():
    emit('update', {
        'timestamp': datetime.now().isoformat(),
        'data': data_store.get_all_data()
    })

@app.route('/api/investment-analysis', methods=['POST'])
def analyze_investment():
    try:
        data = request.get_json()
        company_name = data.get('company_name', '').strip()
        
        if not company_name:
            return jsonify({
                'status': 'error',
                'error': 'Company name is required'
            }), 400
        
        # Initialize YC Investment Agent
        yc_agent = YCInvestmentAgent(data_store)
        
        # Collect data from all agents for the company
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def collect_and_analyze():
            # Collect news data
            news_agent = CryptoNewsAgent(data_store)
            news_data = await news_agent.collect()
            
            # Collect market data
            market_agent = CryptoMarketAgent(data_store)
            market_data = await market_agent.collect()
            
            # Collect company data
            crunchbase_agent = CrunchbaseCryptoAgent(data_store)
            company_data = await crunchbase_agent.collect()
            
            # Filter relevant data for the company
            relevant_news = [item for item in news_data 
                           if company_name.lower() in item.get('title', '').lower() 
                           or company_name.lower() in item.get('description', '').lower()]
            
            relevant_market = [item for item in market_data 
                             if company_name.lower() in item.get('name', '').lower()
                             or company_name.lower() in item.get('crypto_id', '').lower()]
            
            relevant_company = [item for item in company_data 
                              if company_name.lower() in item.get('company_name', '').lower()]
            
            # If no specific data found, use general market data
            if not relevant_news:
                relevant_news = news_data[:5]  # Top 5 news items
            if not relevant_market:
                relevant_market = market_data[:3]  # Top 3 market items
            if not relevant_company:
                # Create synthetic company data
                relevant_company = [{
                    "company_name": company_name,
                    "description": f"Cryptocurrency/blockchain company operating in the digital asset space",
                    "funding_info": "Unknown",
                    "category": "Crypto/Blockchain",
                    "source": "User Input"
                }]
            
            # Perform YC investment analysis
            analysis = await yc_agent.analyze_investment(
                company_name,
                relevant_news,
                relevant_market,
                relevant_company
            )
            
            return {
                'news_data': relevant_news,
                'market_data': relevant_market,
                'company_data': relevant_company,
                'yc_analysis': analysis
            }
        
        result = loop.run_until_complete(collect_and_analyze())
        
        return jsonify({
            'status': 'success',
            **result
        })
        
    except Exception as e:
        print(f"Investment analysis error: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    initialize_agents()
    
    run_async_collection()
    
    collector_thread = threading.Thread(target=background_collector, daemon=True)
    collector_thread.start()
    
    socketio.run(app, debug=True, host='127.0.0.1', port=8888, allow_unsafe_werkzeug=True)
