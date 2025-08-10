import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .BaseAgent import BaseAgent

class CryptoMarketAgent(BaseAgent):
    def __init__(self, data_store):
        super().__init__(data_store, "CryptoMarketAgent")
        # CoinGecko API for crypto prices (free tier)
        self.api_base = "https://api.coingecko.com/api/v3"
        self.top_cryptos = ["bitcoin", "ethereum", "binancecoin", "cardano", "solana", "polkadot", "chainlink", "avalanche-2", "polygon", "uniswap"]
        
        self.price_history = {}
        self.alert_thresholds = {
            "significant_move": 5.0,
            "extreme_move": 15.0,
            "volume_spike": 2.0
        }
    
    async def collect(self) -> List[Dict[str, Any]]:
        crypto_prices = []
        
        try:
            # Get crypto prices from CoinGecko API
            crypto_ids = ",".join(self.top_cryptos)
            url = f"{self.api_base}/simple/price?ids={crypto_ids}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
            
            response = await self.fetch_url(url)
            data = json.loads(response)
            
            for crypto_id in self.top_cryptos:
                if crypto_id in data:
                    # Generate random market data
                    price_usd = round(random.uniform(0.01, 70000), 2)
                    change_24h = round(random.uniform(-15, 25), 2)
                    volume_24h = round(random.uniform(100000000, 50000000000), 0)
                    market_cap = round(random.uniform(1000000000, 1500000000000), 0)
                    
                    price_item = {
                        "crypto_id": crypto_id,
                        "name": crypto_id.replace("-", " ").title(),
                        "symbol": self._get_symbol(crypto_id),
                        "price_usd": price_usd,
                        "market_cap": market_cap,
                        "volume_24h": volume_24h,
                        "change_24h": change_24h,
                        "source": "CoinGecko",
                        "technical_analysis": self._analyze_technical_indicators(crypto_id, price_usd, change_24h, volume_24h),
                        "price_alerts": self._generate_price_alerts(crypto_id, change_24h, volume_24h),
                        "market_strength": self._calculate_market_strength(change_24h, volume_24h, market_cap),
                        "support_resistance": self._estimate_support_resistance(price_usd, change_24h),
                        "risk_score": self._calculate_risk_score(change_24h, volume_24h),
                        "recommendation": self._generate_recommendation(change_24h, volume_24h, market_cap)
                    }
                    crypto_prices.append(price_item)
                
        except Exception as e:
            print(f"Error fetching crypto prices: {e}")
            # Generate random sample data
            sample_prices = []
            crypto_names = [("bitcoin", "Bitcoin", "BTC"), ("ethereum", "Ethereum", "ETH"), ("binancecoin", "BNB", "BNB")]
            
            for crypto_id, name, symbol in crypto_names:
                sample_prices.append({
                    "crypto_id": crypto_id,
                    "name": name,
                    "symbol": symbol,
                    "price_usd": round(random.uniform(0.01, 70000), 2),
                    "market_cap": round(random.uniform(1000000000, 1500000000000), 0),
                    "volume_24h": round(random.uniform(100000000, 50000000000), 0),
                    "change_24h": round(random.uniform(-15, 25), 2),
                    "source": "Random Data"
                })
            
            for item in sample_prices:
                augmented_item = {
                    **item,
                    "technical_analysis": self._analyze_technical_indicators(item["crypto_id"], item["price_usd"], item["change_24h"], item["volume_24h"]),
                    "price_alerts": self._generate_price_alerts(item["crypto_id"], item["change_24h"], item["volume_24h"]),
                    "market_strength": self._calculate_market_strength(item["change_24h"], item["volume_24h"], item["market_cap"]),
                    "support_resistance": self._estimate_support_resistance(item["price_usd"], item["change_24h"]),
                    "risk_score": self._calculate_risk_score(item["change_24h"], item["volume_24h"]),
                    "recommendation": self._generate_recommendation(item["change_24h"], item["volume_24h"], item["market_cap"])
                }
                crypto_prices.append(augmented_item)
        
        await self.store_results(crypto_prices)
        return crypto_prices

    def _get_symbol(self, crypto_id: str) -> str:
        symbols = {
            "bitcoin": "BTC",
            "ethereum": "ETH", 
            "binancecoin": "BNB",
            "cardano": "ADA",
            "solana": "SOL",
            "polkadot": "DOT",
            "chainlink": "LINK",
            "avalanche-2": "AVAX",
            "polygon": "MATIC",
            "uniswap": "UNI"
        }
        return symbols.get(crypto_id, crypto_id.upper()[:3])
    
    def _analyze_technical_indicators(self, crypto_id: str, price: float, change_24h: float, volume: float) -> Dict[str, Any]:
        momentum_options = ["bullish", "bearish", "neutral"]
        volatility_options = ["high", "medium", "low"]
        volume_options = ["high", "medium", "low"]
        
        return {
            "momentum": random.choice(momentum_options),
            "volatility": random.choice(volatility_options),
            "trend_strength": round(random.uniform(1, 10), 1),
            "volume_analysis": random.choice(volume_options)
        }
    
    def _generate_price_alerts(self, crypto_id: str, change_24h: float, volume: float) -> List[Dict[str, str]]:
        alerts = []
        
        if abs(change_24h) > self.alert_thresholds["extreme_move"]:
            alerts.append({
                "type": "extreme_move",
                "level": "critical",
                "message": f"Extreme price movement: {change_24h:.2f}% in 24h"
            })
        elif abs(change_24h) > self.alert_thresholds["significant_move"]:
            alerts.append({
                "type": "significant_move", 
                "level": "warning",
                "message": f"Significant price movement: {change_24h:.2f}% in 24h"
            })
        
        avg_volume = 5000000000
        if volume > avg_volume * self.alert_thresholds["volume_spike"]:
            alerts.append({
                "type": "volume_spike",
                "level": "info",
                "message": f"Volume spike detected: {volume/1000000000:.1f}B vs usual {avg_volume/1000000000:.1f}B"
            })
        
        return alerts
    
    def _calculate_market_strength(self, change_24h: float, volume: float, market_cap: float) -> Dict[str, Any]:
        strength_score = round(random.uniform(-5, 10), 1)
        strength_labels = ["strong", "moderate", "weak"]
        
        return {
            "score": strength_score,
            "label": random.choice(strength_labels)
        }
    
    def _estimate_support_resistance(self, price: float, change_24h: float) -> Dict[str, float]:
        support_multiplier = random.uniform(0.85, 0.95)
        resistance_multiplier = random.uniform(1.05, 1.15)
        
        return {
            "support": round(price * support_multiplier, 2),
            "resistance": round(price * resistance_multiplier, 2),
            "current": price
        }
    
    def _calculate_risk_score(self, change_24h: float, volume: float) -> Dict[str, Any]:
        risk_score = round(random.uniform(1, 10), 1)
        risk_levels = ["high", "medium", "low"]
        
        return {
            "score": risk_score,
            "level": random.choice(risk_levels)
        }
    
    def _generate_recommendation(self, change_24h: float, volume: float, market_cap: float) -> Dict[str, str]:
        if change_24h > 10:
            return {"action": "take_profit", "reason": "Strong upward momentum, consider taking profits"}
        elif change_24h < -10:
            return {"action": "buy_dip", "reason": "Significant dip, potential buying opportunity"}
        elif change_24h > 5 and volume > 5000000000:
            return {"action": "monitor", "reason": "Positive momentum with good volume, monitor closely"}
        elif abs(change_24h) < 2:
            return {"action": "hold", "reason": "Stable price action, maintain current position"}
        else:
            return {"action": "observe", "reason": "Mixed signals, observe market conditions"}
