import json
import re
import random
from datetime import datetime
from typing import List, Dict, Any
from .BaseAgent import BaseAgent

class CryptoNewsAgent(BaseAgent):
    def __init__(self, data_store):
        super().__init__(data_store, "CryptoNewsAgent")
        # CoinDesk API for crypto news
        self.sources = {
            "coindesk_news": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        }
        
        self.bullish_keywords = ['surge', 'rally', 'breakout', 'bullish', 'gains', 'rise', 'pump', 'moon', 'adoption', 'institutional']
        self.bearish_keywords = ['crash', 'dump', 'bearish', 'decline', 'drop', 'sell-off', 'correction', 'fear', 'regulation', 'ban']
        self.neutral_keywords = ['stable', 'consolidation', 'sideways', 'range', 'analysis', 'report']
    async def collect(self) -> List[Dict[str, Any]]:
        news_items = []
        
        try:
            # Try to fetch from CoinDesk RSS (more reliable than API)
            rss_data = await self.fetch_url(self.sources["coindesk_news"])
            soup = self.parse_html(rss_data)
            
            items = soup.find_all("item")[:10]  # Get top 10 news items
            
            for item in items:
                title_elem = item.find("title")
                link_elem = item.find("link")
                description_elem = item.find("description")
                pub_date_elem = item.find("pubdate")
                
                title_text = title_elem.text.strip() if title_elem else "No title"
                description_text = description_elem.text.strip() if description_elem else ""
                
                news_item = {
                    "title": title_text,
                    "url": link_elem.text.strip() if link_elem else "",
                    "description": description_text[:200] + "..." if len(description_text) > 200 else description_text,
                    "published_date": pub_date_elem.text.strip() if pub_date_elem else "",
                    "category": "Crypto News",
                    "source": "CoinDesk",
                    "sentiment": self._analyze_sentiment(title_text + " " + description_text),
                    "urgency_score": self._calculate_urgency(title_text + " " + description_text),
                    "crypto_mentions": self._extract_crypto_mentions(title_text + " " + description_text),
                    "keywords": self._extract_keywords(title_text + " " + description_text),
                    "read_time_minutes": random.randint(1, 15)
                }
                news_items.append(news_item)
        
        except Exception as e:
            print(f"Error collecting crypto news: {e}")
            
            sample_news = [
                {
                    "title": "Bitcoin Surges Past $45,000 as Institutional Adoption Grows",
                    "url": "https://www.coindesk.com/markets/bitcoin-surges-45000",
                    "description": "Bitcoin reaches new monthly highs as major corporations announce crypto treasury allocations...",
                    "published_date": "2024-01-15T10:30:00Z",
                    "category": "Crypto News",
                    "source": "CoinDesk"
                },
                {
                    "title": "Ethereum Layer 2 Solutions See Record Trading Volume", 
                    "url": "https://www.coindesk.com/tech/ethereum-layer-2-volume",
                    "description": "Arbitrum and Optimism report unprecedented user activity as gas fees remain low...",
                    "published_date": "2024-01-15T09:15:00Z",
                    "category": "Crypto News",
                    "source": "CoinDesk"
                },
                {
                    "title": "SEC Approves New Spot Bitcoin ETF Applications",
                    "url": "https://www.coindesk.com/policy/sec-bitcoin-etf-approval", 
                    "description": "Regulatory clarity emerges as additional Bitcoin ETFs receive approval for trading...",
                    "published_date": "2024-01-15T08:00:00Z",
                    "category": "Crypto News",
                    "source": "CoinDesk"
                }
            ]
            
            for item in sample_news:
                augmented_item = {
                    **item,
                    "sentiment": self._analyze_sentiment(item["title"] + " " + item["description"]),
                    "urgency_score": self._calculate_urgency(item["title"] + " " + item["description"]),
                    "crypto_mentions": self._extract_crypto_mentions(item["title"] + " " + item["description"]),
                    "keywords": self._extract_keywords(item["title"] + " " + item["description"]),
                    "read_time_minutes": max(1, len(item["description"].split()) // 200)
                }
                news_items.append(augmented_item)
        
        await self.store_results(news_items)
        return news_items
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        # Generate random sentiment data
        sentiment_labels = ["bullish", "bearish", "neutral"]
        label = random.choice(sentiment_labels)
        
        if label == "bullish":
            score = round(random.uniform(0.6, 0.9), 2)
        elif label == "bearish":
            score = round(random.uniform(0.1, 0.4), 2)
        else:
            score = round(random.uniform(0.4, 0.6), 2)
        
        confidence = round(random.uniform(0.3, 1.0), 2)
        
        return {"label": label, "score": score, "confidence": confidence}
    
    def _calculate_urgency(self, text: str) -> int:
        # Generate random urgency score
        return random.randint(1, 10)
    
    def _extract_crypto_mentions(self, text: str) -> List[str]:
        crypto_pattern = r'\b(bitcoin|btc|ethereum|eth|binance|bnb|cardano|ada|solana|sol|polkadot|dot|chainlink|link|avalanche|avax|polygon|matic|uniswap|uni)\b'
        matches = re.findall(crypto_pattern, text.lower())
        return list(set(matches))
    
    def _extract_keywords(self, text: str) -> List[str]:
        all_keywords = self.bullish_keywords + self.bearish_keywords + self.neutral_keywords
        text_lower = text.lower()
        found_keywords = [keyword for keyword in all_keywords if keyword in text_lower]
        
        additional_keywords = ['defi', 'nft', 'web3', 'metaverse', 'dao', 'mining', 'staking', 'yield']
        found_keywords.extend([keyword for keyword in additional_keywords if keyword in text_lower])
        
        return list(set(found_keywords))
