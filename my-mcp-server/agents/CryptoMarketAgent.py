import json
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
                    crypto_data = data[crypto_id]
                    price_usd = crypto_data.get("usd", 0)
                    change_24h = crypto_data.get("usd_24h_change", 0)
                    volume_24h = crypto_data.get("usd_24h_vol", 0)
                    market_cap = crypto_data.get("usd_market_cap", 0)
                    
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
            sample_prices = [
                {
                    "crypto_id": "bitcoin",
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "price_usd": 45000.00,
                    "market_cap": 880000000000,
                    "volume_24h": 25000000000,
                    "change_24h": 2.5,
                    "source": "Sample Data"
                },
                {
                    "crypto_id": "ethereum",
                    "name": "Ethereum",
                    "symbol": "ETH",
                    "price_usd": 2800.00,
                    "market_cap": 340000000000,
                    "volume_24h": 15000000000,
                    "change_24h": 1.8,
                    "source": "Sample Data"
                },
                {
                    "crypto_id": "binancecoin",
                    "name": "BNB",
                    "symbol": "BNB",
                    "price_usd": 310.00,
                    "market_cap": 47000000000,
                    "volume_24h": 800000000,
                    "change_24h": -0.5,
                    "source": "Sample Data"
                }
            ]
            
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
        momentum = "bullish" if change_24h > 2 else "bearish" if change_24h < -2 else "neutral"
        volatility = "high" if abs(change_24h) > 10 else "medium" if abs(change_24h) > 5 else "low"
        
        return {
            "momentum": momentum,
            "volatility": volatility,
            "trend_strength": min(10, abs(change_24h)),
            "volume_analysis": "high" if volume > 10000000000 else "medium" if volume > 1000000000 else "low"
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
        strength_score = 0
        
        if change_24h > 0:
            strength_score += min(5, change_24h)
        else:
            strength_score += max(-5, change_24h)
        
        if volume > 10000000000:
            strength_score += 2
        elif volume > 1000000000:
            strength_score += 1
            
        if market_cap > 100000000000:
            strength_score += 1
            
        return {
            "score": strength_score,
            "label": "strong" if strength_score > 5 else "weak" if strength_score < -2 else "moderate"
        }
    
    def _estimate_support_resistance(self, price: float, change_24h: float) -> Dict[str, float]:
        volatility_factor = abs(change_24h) / 100
        price_range = price * volatility_factor
        
        return {
            "support": round(price - price_range, 2),
            "resistance": round(price + price_range, 2),
            "current": price
        }
    
    def _calculate_risk_score(self, change_24h: float, volume: float) -> Dict[str, Any]:
        risk_score = 0
        
        risk_score += min(5, abs(change_24h) / 2)
        
        if volume < 1000000000:
            risk_score += 2
        
        risk_level = "high" if risk_score > 7 else "medium" if risk_score > 4 else "low"
        
        return {
            "score": round(risk_score, 1),
            "level": risk_level
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
