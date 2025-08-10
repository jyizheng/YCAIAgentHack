#!/usr/bin/env python3
import asyncio
from agents.CryptoNewsAgent import CryptoNewsAgent
from agents.CryptoMarketAgent import CryptoMarketAgent
from agents.CrunchbaseCryptoAgent import CrunchbaseCryptoAgent
from agents.YCInvestmentAgent import YCInvestmentAgent
from data_store import DataStore

async def test_investment_analysis():
    data_store = DataStore()
    company_name = "Coinbase"
    
    try:
        # Initialize agents
        news_agent = CryptoNewsAgent(data_store)
        market_agent = CryptoMarketAgent(data_store)
        crunchbase_agent = CrunchbaseCryptoAgent(data_store)
        yc_agent = YCInvestmentAgent(data_store)
        
        print(f"Testing investment analysis for {company_name}...")
        
        # Collect data
        print("Collecting news data...")
        news_data = await news_agent.collect()
        print(f"Collected {len(news_data)} news items")
        
        print("Collecting market data...")
        market_data = await market_agent.collect()
        print(f"Collected {len(market_data)} market items")
        
        print("Collecting company data...")
        company_data = await crunchbase_agent.collect()
        print(f"Collected {len(company_data)} company items")
        
        # Perform analysis
        print("Performing YC investment analysis...")
        analysis = await yc_agent.analyze_investment(
            company_name,
            news_data[:3],
            market_data[:3],
            company_data[:3]
        )
        
        print("\n=== INVESTMENT ANALYSIS RESULTS ===")
        print(f"Company: {analysis['company_name']}")
        print(f"Decision: {analysis['investment_decision']}")
        print(f"Investment Amount: ${analysis['recommended_investment']:,}")
        print(f"Equity Stake: {analysis['equity_stake']}%")
        print(f"Overall Score: {analysis['overall_score']}/10")
        print(f"Risk Score: {analysis['risk_score']}/10")
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_investment_analysis())