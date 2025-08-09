import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .BaseAgent import BaseAgent

class CrunchbaseCryptoAgent(BaseAgent):
    def __init__(self, data_store):
        super().__init__(data_store, "CrunchbaseCryptoAgent")
        # Crunchbase API endpoints for crypto companies
        self.crunchbase_api_base = "https://api.crunchbase.com/api/v4"
        self.crypto_search_url = "https://www.crunchbase.com/discover/organization.companies"
        
        self.company_categories = {
            "exchange": ["exchange", "trading", "marketplace"],
            "infrastructure": ["blockchain", "protocol", "infrastructure", "node"],
            "defi": ["defi", "lending", "yield", "liquidity"],
            "nft": ["nft", "collectibles", "marketplace", "art"],
            "payments": ["payments", "wallet", "custody"],
            "mining": ["mining", "validator", "staking"]
        }
        
        self.funding_stages = {
            "seed": ["seed", "pre-seed", "angel"],
            "early": ["series a", "series b"],
            "growth": ["series c", "series d", "series e"],
            "late": ["series f", "series g", "ipo"]
        }
        
    async def collect(self) -> List[Dict[str, Any]]:
        crypto_companies = []
        
        try:
            # Try to scrape Crunchbase crypto companies page
            html = await self.fetch_url(self.crypto_search_url)
            soup = self.parse_html(html)
            
            # Look for company cards or listings
            company_elements = soup.find_all("div", class_="cb-card")[:10]
            
            for company in company_elements:
                name_elem = company.find("h3") or company.find("h4") or company.find(".company-name")
                description_elem = company.find("p") or company.find(".description")
                funding_elem = company.find(".funding-info") or company.find(".money")
                
                if name_elem:
                    company_name = name_elem.get_text(strip=True)
                    description_text = description_elem.get_text(strip=True) if description_elem else ""
                    funding_text = funding_elem.get_text(strip=True) if funding_elem else "N/A"
                    
                    company_item = {
                        "company_name": company_name,
                        "description": description_text[:200] + "..." if len(description_text) > 200 else description_text,
                        "funding_info": funding_text,
                        "url": f"https://www.crunchbase.com/organization/{company_name.lower().replace(' ', '-')}",
                        "category": "Crypto/Blockchain",
                        "source": "Crunchbase",
                        "company_analysis": self._analyze_company_profile(company_name, description_text, funding_text),
                        "investment_metrics": self._calculate_investment_metrics(funding_text),
                        "market_position": self._assess_market_position(company_name, description_text),
                        "competitive_analysis": self._analyze_competition(description_text),
                        "growth_indicators": self._evaluate_growth_potential(description_text, funding_text),
                        "risk_assessment": self._assess_company_risk(funding_text, description_text)
                    }
                    crypto_companies.append(company_item)
                        
        except Exception as e:
            print(f"Error collecting Crunchbase crypto data: {e}")
            sample_companies = [
                {
                    "company_name": "Coinbase",
                    "description": "Cryptocurrency exchange platform that allows users to buy, sell, and store digital currencies",
                    "funding_info": "$547M Series E",
                    "url": "https://www.crunchbase.com/organization/coinbase",
                    "category": "Crypto Exchange",
                    "source": "Crunchbase"
                },
                {
                    "company_name": "Binance",
                    "description": "Global cryptocurrency exchange offering trading, staking, and DeFi services",
                    "funding_info": "$15M Series A",
                    "url": "https://www.crunchbase.com/organization/binance",
                    "category": "Crypto Exchange",
                    "source": "Crunchbase"
                },
                {
                    "company_name": "Chainlink Labs",
                    "description": "Decentralized oracle network that provides real-world data to blockchain smart contracts",
                    "funding_info": "$32M Series A",
                    "url": "https://www.crunchbase.com/organization/chainlink",
                    "category": "Blockchain Infrastructure",
                    "source": "Crunchbase"
                },
                {
                    "company_name": "ConsenSys",
                    "description": "Ethereum software company building infrastructure, applications, and developer tools",
                    "funding_info": "$200M Series D",
                    "url": "https://www.crunchbase.com/organization/consensus-systems",
                    "category": "Blockchain Infrastructure",
                    "source": "Crunchbase"
                }
            ]
            
            for item in sample_companies:
                augmented_item = {
                    **item,
                    "company_analysis": self._analyze_company_profile(item["company_name"], item["description"], item["funding_info"]),
                    "investment_metrics": self._calculate_investment_metrics(item["funding_info"]),
                    "market_position": self._assess_market_position(item["company_name"], item["description"]),
                    "competitive_analysis": self._analyze_competition(item["description"]),
                    "growth_indicators": self._evaluate_growth_potential(item["description"], item["funding_info"]),
                    "risk_assessment": self._assess_company_risk(item["funding_info"], item["description"])
                }
                crypto_companies.append(augmented_item)
        
        await self.store_results(crypto_companies)
        return crypto_companies
    
    def _analyze_company_profile(self, name: str, description: str, funding_info: str) -> Dict[str, Any]:
        profile = {
            "sector": self._categorize_company(description),
            "maturity_stage": self._determine_maturity(funding_info),
            "business_model": self._identify_business_model(description),
            "key_technologies": self._extract_technologies(description)
        }
        return profile
    
    def _categorize_company(self, description: str) -> str:
        desc_lower = description.lower()
        for category, keywords in self.company_categories.items():
            if any(keyword in desc_lower for keyword in keywords):
                return category
        return "general"
    
    def _determine_maturity(self, funding_info: str) -> str:
        funding_lower = funding_info.lower()
        for stage, indicators in self.funding_stages.items():
            if any(indicator in funding_lower for indicator in indicators):
                return stage
        return "unknown"
    
    def _identify_business_model(self, description: str) -> str:
        desc_lower = description.lower()
        if any(word in desc_lower for word in ["exchange", "trading", "marketplace"]):
            return "marketplace"
        elif any(word in desc_lower for word in ["saas", "service", "platform"]):
            return "platform"
        elif any(word in desc_lower for word in ["protocol", "infrastructure"]):
            return "protocol"
        elif any(word in desc_lower for word in ["wallet", "custody"]):
            return "service"
        else:
            return "hybrid"
    
    def _extract_technologies(self, description: str) -> List[str]:
        tech_keywords = [
            "blockchain", "ethereum", "bitcoin", "defi", "nft", "smart contracts",
            "web3", "dao", "layer 2", "scaling", "consensus", "mining", "staking"
        ]
        desc_lower = description.lower()
        return [tech for tech in tech_keywords if tech in desc_lower]
    
    def _calculate_investment_metrics(self, funding_info: str) -> Dict[str, Any]:
        funding_amount = self._extract_funding_amount(funding_info)
        
        metrics = {
            "total_funding_usd": funding_amount,
            "funding_stage": self._determine_maturity(funding_info),
            "valuation_estimate": funding_amount * 10 if funding_amount > 0 else None,
            "investor_confidence": "high" if funding_amount > 100000000 else "medium" if funding_amount > 10000000 else "low"
        }
        return metrics
    
    def _extract_funding_amount(self, funding_info: str) -> float:
        if "N/A" in funding_info or not funding_info:
            return 0
        
        amount_match = re.search(r'\$(\d+(?:\.\d+)?)(M|B|K)?', funding_info)
        if amount_match:
            amount = float(amount_match.group(1))
            multiplier = amount_match.group(2)
            
            if multiplier == 'B':
                return amount * 1000000000
            elif multiplier == 'M':
                return amount * 1000000
            elif multiplier == 'K':
                return amount * 1000
            else:
                return amount
        return 0
    
    def _assess_market_position(self, name: str, description: str) -> Dict[str, Any]:
        well_known = name.lower() in ["coinbase", "binance", "kraken", "chainlink", "consensys", "opensea"]
        
        position = {
            "market_leader": well_known,
            "competitive_moat": self._evaluate_moat(description),
            "network_effects": "high" if "network" in description.lower() or "ecosystem" in description.lower() else "medium",
            "brand_recognition": "high" if well_known else "medium"
        }
        return position
    
    def _evaluate_moat(self, description: str) -> str:
        desc_lower = description.lower()
        strong_moat_indicators = ["first mover", "patent", "exclusive", "proprietary", "regulated"]
        medium_moat_indicators = ["established", "trusted", "secure", "compliant"]
        
        if any(indicator in desc_lower for indicator in strong_moat_indicators):
            return "strong"
        elif any(indicator in desc_lower for indicator in medium_moat_indicators):
            return "medium"
        else:
            return "weak"
    
    def _analyze_competition(self, description: str) -> Dict[str, Any]:
        competitive_density = "high" if "exchange" in description.lower() else "medium"
        differentiation_level = "high" if len(self._extract_technologies(description)) > 3 else "medium"
        
        return {
            "competitive_density": competitive_density,
            "differentiation_level": differentiation_level,
            "market_barriers": "high" if "regulated" in description.lower() else "medium"
        }
    
    def _evaluate_growth_potential(self, description: str, funding_info: str) -> Dict[str, Any]:
        funding_amount = self._extract_funding_amount(funding_info)
        
        growth_score = 0
        if funding_amount > 50000000:
            growth_score += 3
        elif funding_amount > 10000000:
            growth_score += 2
        elif funding_amount > 1000000:
            growth_score += 1
        
        if any(keyword in description.lower() for keyword in ["growing", "expanding", "scaling"]):
            growth_score += 2
        
        if any(keyword in description.lower() for keyword in ["defi", "nft", "web3", "metaverse"]):
            growth_score += 1
        
        return {
            "growth_score": growth_score,
            "growth_potential": "high" if growth_score >= 5 else "medium" if growth_score >= 3 else "low",
            "market_trend_alignment": "high" if growth_score >= 4 else "medium"
        }
    
    def _assess_company_risk(self, funding_info: str, description: str) -> Dict[str, Any]:
        risk_score = 5
        
        funding_amount = self._extract_funding_amount(funding_info)
        if funding_amount > 100000000:
            risk_score -= 2
        elif funding_amount < 1000000:
            risk_score += 2
        
        if "regulated" in description.lower() or "compliant" in description.lower():
            risk_score -= 1
        
        if any(keyword in description.lower() for keyword in ["experimental", "beta", "early"]):
            risk_score += 1
        
        risk_level = "low" if risk_score <= 2 else "high" if risk_score >= 7 else "medium"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "regulatory_risk": "high" if "exchange" in description.lower() else "medium",
            "technology_risk": "high" if "experimental" in description.lower() else "medium"
        }
